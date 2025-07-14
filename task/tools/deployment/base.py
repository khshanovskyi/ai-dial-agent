import json
from abc import ABC, abstractmethod

from openai import AsyncAzureOpenAI
from pydantic import StrictStr

from task.tools.base import BaseTool

from aidial_sdk.chat_completion import Stage, Message, Role, ToolCall


class DeploymentTool(BaseTool, ABC):

    def __init__(self, endpoint: str, api_key: str, api_version: str,):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_version = api_version

    @property
    @abstractmethod
    def deployment_name(self) -> str:
        pass

    async def execute(self, tool_call: ToolCall, stage: Stage) -> Message:
        client: AsyncAzureOpenAI = AsyncAzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version,
        )

        config = {
            "messages": [{"role": "user", "content": json.loads(tool_call.function.arguments).get("query")}],
            "stream": True,
            "model": self.deployment_name,
        }
        chunks = await client.chat.completions.create(**config)

        content=''
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    stage.append_content(delta.content)
                    content += delta.content


        return Message(
            role=Role.TOOL,
            content=StrictStr(content),
            tool_call_id=StrictStr(tool_call.id),
        )