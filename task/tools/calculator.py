import json
from typing import Any

from aidial_sdk.chat_completion import ToolCall, Stage, Choice, Message, Role
from pydantic import StrictStr

from task.tools.base import BaseTool


class CalculatorTool(BaseTool):

    #TODO:
    # Implement all the methods from `BaseTool`:
    # 1. Implement async `execute` method:
    #   1.1 Get arguments as dict (use `json.loads()`) and assign to `arguments` variable. The arguments path:
    #       tool_call -> function -> arguments
    #   1.2 Get required arguments and assign them to variables:
    #       - num1 = float(arguments["num1"])
    #       - num2 = float(arguments["num2"])
    #       - operation = arguments["operation"]
    #   1.3 Provide implementation with simple calculations: ["add", "subtract", "multiply", "divide"] (don't forget
    #       to handle `division by zero` case and case with unknown operation).
    #   1.4 Append calculation result to `stage`. (We need it to show the execution result in stage for tool call)
    #   1.5 Return Message with:
    #           - role=Role.TOOL
    #           - content=StrictStr(content)
    #           - tool_call_id=StrictStr(tool_call.id) (Remember that we have to return tool call id, without it LLM will answer with error)
    # ---
    # 2. Implement `name` method:
    #   - mark as `@property`
    #   - return tool name "simple_calculator" (or another name, but it better to be self-descriptive)
    # ---
    # 3. Implement `description` method:
    #   - mark as `@property`
    #   - return tool description (what this tool do?). With such description LLM will have more context about this tool.
    # ---
    # 4. Implement `parameters` method:
    #   - mark as `@property`
    #   - returns dict with properties configuration according to Specification
    #         https://dialx.ai/dial_api#operation/sendChatCompletionRequest (-> tools -> function).
    #     Pay attention that the `operation` type is `string` and it should have the `enum` with possible values: ["add", "subtract", "multiply", "divide"]



#Sample of the properties configuration:
# {
#     "type": "object",
#     "properties": {
#         "param1": {
#             "type": "number",
#             "description": "Your param description"
#         },
#         "param2": {
#             "type": "string",
#             "description": "Your param description",
#             "enum": [
#                 "val1",
#                 "val2",
#                 "val3"
#             ]
#         }
#     },
#     "required": [
#         "param1",
#         "param2"
#     ]
# }