from abc import ABC, abstractmethod
from typing import Any

from aidial_client.types.chat import ToolParam
from aidial_sdk.chat_completion import Stage, Message, ToolCall, Response


class BaseTool(ABC):

    @abstractmethod
    async def execute(self, tool_call: ToolCall, stage: Stage, response: Response) -> Message:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        pass

    @property
    def schema(self) -> ToolParam:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
