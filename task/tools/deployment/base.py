import json
from abc import ABC, abstractmethod

from openai import AsyncAzureOpenAI
from pydantic import StrictStr

from task.tools.base import BaseTool

from aidial_sdk.chat_completion import Stage, Message, Role, ToolCall, CustomContent, Choice

from task.utils.constants import CUSTOM_CONTENT
from task.utils.response import capture_attachments


class DeploymentTool(BaseTool, ABC):

    def __init__(self, endpoint: str, api_version: str, ):
        self.endpoint = endpoint
        self.api_version = api_version

    @property
    @abstractmethod
    def deployment_name(self) -> str:
        pass

    async def execute(self, tool_call: ToolCall, stage: Stage, choice: Choice, api_key: str) -> Message:
        client: AsyncAzureOpenAI = AsyncAzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=api_key,
            api_version=self.api_version,
        )

        arguments = json.loads(tool_call.function.arguments)
        prompt = arguments.get("prompt")
        del arguments["prompt"]

        config = {
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "model": self.deployment_name,
            "extra_body" : {
                "custom_fields": {
                    "configuration": {**arguments}
                }
            }
        }
        chunks = await client.chat.completions.create(**config)

        content = ''
        custom_content: CustomContent = CustomContent(attachments=[])
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta:
                    if delta.content:
                        stage.append_content(delta.content)
                        content += delta.content
                    if getattr(delta, CUSTOM_CONTENT, None):
                        custom_content_dict = getattr(delta, CUSTOM_CONTENT, None)
                        attachments = capture_attachments(custom_content_dict)
                        custom_content.attachments.extend(attachments)

                        for attachment in attachments:
                            stage.add_attachment(attachment)

        return Message(
            role=Role.TOOL,
            content=StrictStr(content),
            custom_content=custom_content,
            tool_call_id=StrictStr(tool_call.id),
        )
