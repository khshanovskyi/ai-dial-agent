from abc import ABC, abstractmethod
from typing import Any

from aidial_client.types.chat import ToolParam, FunctionParam
from aidial_sdk.chat_completion import Stage, Message, ToolCall, Choice


class BaseTool(ABC):
    """Base tool class"""

    #TODO:
    # Create such methods:
    # 1. Create async `execute` method:
    #   - mark as `@abstractmethod`
    #   - Parameters:
    #       - tool_call: ToolCall
    #       - stage: Stage
    #       - choice: Choice
    #       - api_key: str
    #   - returns Message
    #   - Instead of implementation add `pass`
    # 2. Create `name` method:
    #   - mark as `@property`
    #   - mark as `@abstractmethod`
    #   - returns str
    #   - Instead of implementation add `pass`
    # 3. Create `description` method:
    #   - mark as `@property`
    #   - mark as `@abstractmethod`
    #   - returns str
    #   - Instead of implementation add `pass`
    # 4. Create `parameters` method:
    #   - mark as `@property`
    #   - mark as `@abstractmethod`
    #   - returns dict[str, Any]
    #   - Instead of implementation add `pass`
    # 5. Create `schema` method:
    #   - mark as `@property`
    #   - returns ToolParam
    #   - return ToolParam with such configuration:
    #       - type="function"
    #       - function=FunctionParam(name=self.name, description=self.description,  parameters=self.parameters)

