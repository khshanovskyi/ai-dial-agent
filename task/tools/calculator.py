import json
from typing import Any

from aidial_sdk.chat_completion import ToolCall, Stage, Choice, Message, Role
from pydantic import StrictStr

from task.tools.base import BaseTool


class CalculatorTool(BaseTool):

    async def execute(self, tool_call: ToolCall, stage: Stage, choice: Choice, api_key: str) -> Message:
        #TODO:
        # Get arguments as dict (use `json.loads()`). The arguments path: tool_call -> function -> arguments
        arguments = None

        num1 = float(arguments["num1"])
        num2 = float(arguments["num2"])
        operation = arguments["operation"]

        if operation == "add":
            content = num1 + num2
        elif operation == "subtract":
            content = num1 - num2
        elif operation == "multiply":
            content = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                content = "Error: Division by zero"
            else:
                content = num1 / num2
        else:
            content = f"Error: Unknown operation '{operation}'"

        #TODO:
        # 1. Append `content` to `stage`. (We need it to show the execution result in stage for tool call)
        # 2. Return Message with:
        #   - role=Role.TOOL
        #   - content=StrictStr(content)
        #   - tool_call_id=StrictStr(tool_call.id) (Remember that we have to return tool call id, without it LLM will answer with error)

        return None

    @property
    def name(self) -> str:
        #TODO:
        # return tool name "simple_calculator" (or another name, but it better to be self descriptive)

    @property
    def description(self) -> str:
        #TODO:
        # return tool description (what this tool do?). With such description LLM will have more context about this tool.

    @property
    def parameters(self) -> dict[str, Any]:
        # You don't need to change here anything, just take a look at the configuration and compare that with tool
        # arguments in the `execute` method
        return {
            "type": "object",
            "properties": {
                "num1": {
                    "type": "number",
                    "description": "First operand"
                },
                "num2": {
                    "type": "number",
                    "description": "Second operand"
                },
                "operation": {
                    "type": "string",
                    "description": "Operation to perform",
                    "enum": ["add", "subtract", "multiply", "divide"]
                }
            },
            "required": ["num1", "num2", "operation"]
        }
