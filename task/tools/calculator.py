import json
from typing import Any

from aidial_sdk.chat_completion import ToolCall, Stage, Choice, Message, Role
from pydantic import StrictStr

from task.tools.base import BaseTool


class CalculatorTool(BaseTool):

    async def execute(self, tool_call: ToolCall, stage: Stage, choice: Choice, api_key: str) -> Message:
        arguments = json.loads(tool_call.function.arguments)

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

        stage.append_content(f"**{content}**")

        return Message(
            role=Role.TOOL,
            content=StrictStr(content),
            tool_call_id=StrictStr(tool_call.id),
        )

    @property
    def name(self) -> str:
        return "simple_calculator"

    @property
    def description(self) -> str:
        return "Provides result of basic math calculations"

    @property
    def parameters(self) -> dict[str, Any]:
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
