import json
from abc import ABC, abstractmethod
from typing import Any

from aidial_client import AsyncDial
from pydantic import StrictStr

from task.tools.base import BaseTool

from aidial_sdk.chat_completion import Stage, Message, Role, ToolCall, CustomContent, Choice


class DeploymentTool(BaseTool, ABC):

    def __init__(self, endpoint: str, api_version: str, ):
        self.endpoint = endpoint
        self.api_version = api_version

    @property
    @abstractmethod
    def deployment_name(self) -> str:
        pass

    @property
    def tool_parameters(self) -> dict[str, Any]:
        return {}

    async def execute(self, tool_call: ToolCall, stage: Stage, choice: Choice, api_key: str) -> Message:
        client: AsyncDial = AsyncDial(
            base_url=self.endpoint,
            api_key=api_key,
            api_version=self.api_version,
        )

        arguments = json.loads(tool_call.function.arguments)
        prompt = arguments.get("prompt")
        del arguments["prompt"]
        chunks = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            deployment_name=self.deployment_name,
            extra_body={
                "custom_fields": {
                    "configuration": {**arguments}
                }
            },
            **self.tool_parameters,
        )

        content = ''
        custom_content: CustomContent = CustomContent(attachments=[])
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta:
                    if delta.content:
                        stage.append_content(delta.content)
                        content += delta.content
                    if delta.custom_content and delta.custom_content.attachments:
                        attachments = delta.custom_content.attachments
                        custom_content.attachments.extend(attachments)

                        for attachment in attachments:
                            stage.add_attachment(
                                type=attachment.type,
                                title=attachment.title,
                                data=attachment.data,
                                url=attachment.url,
                                reference_url=attachment.reference_url,
                                reference_type=attachment.reference_type,
                            )

        return Message(
            role=Role.TOOL,
            content=StrictStr(content),
            custom_content=custom_content,
            tool_call_id=StrictStr(tool_call.id),
        )
