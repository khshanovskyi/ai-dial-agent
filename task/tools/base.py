from abc import ABC, abstractmethod
from typing import Any

from aidial_client.types.chat import ToolParam, FunctionParam
from aidial_sdk.chat_completion import Stage, Message, ToolCall, Choice


class BaseTool(ABC):
    """Base tool class"""

    @abstractmethod
    async def execute(self, tool_call: ToolCall, stage: Stage, choice: Choice, api_key: str) -> Message:
        """
        Execute tool call.

        :return: Message with tool execution result
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Tool name should be unique for each tool and self-descriptive.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Provides description of the tool that will give to LLM more context about the tool and how to use it.
        """
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """
        Provides tools parameters JSON Schema
        """
        pass

    @property
    def schema(self) -> ToolParam:
        """
        Collects tool JSON Schema according to the Specification:
        https://dialx.ai/dial_api#operation/sendChatCompletionRequest (-> tools -> function)
        """
        return ToolParam(
            type="function",
            function=FunctionParam(
                name=self.name,
                description=self.description,
                parameters=self.parameters
            )
        )
