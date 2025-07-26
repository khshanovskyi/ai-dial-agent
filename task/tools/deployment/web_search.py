from typing import Any

from task.tools.deployment.base import DeploymentTool


class WebSearchTool(DeploymentTool):

    #TODO:
    # 1. Implement `deployment_name` method:
    #   - mark as `@property`
    #   - return deployment name "gemini-2.5-pro"
    # ---
    # 2. Override `tool_parameters` method:
    #   - mark as `@property`
    #   - return {"tools": [{"type":"static_function","static_function":{"name":"google_search","description":"Grounding with Google Search","configuration":{}}}],"temperature":0}
    # ---
    # 3. Implement `name` method:
    #   - mark as `@property`
    #   - return tool name "simple_calculator" (or another name, but it better to be self-descriptive)
    # ---
    # 4. Implement `description` method:
    #   - mark as `@property`
    #   - return tool description (what this tool do?). With such description LLM will have more context about this tool.
    # ---
    # 5. Implement `parameters` method:
    #   - mark as `@property`
    #   - returns dict with properties configuration according to Specification
    #         https://dialx.ai/dial_api#operation/sendChatCompletionRequest (-> tools -> function).
    #     Pay attention that we should have the `prompt` property name in schema (it is using as user message in the DeploymentTool)
    pass


#Sample of the properties configuration:
# {
#     "type": "object",
#     "properties": {
#         "prompt": {
#             "type": "string",
#             "description": "Your param description"
#         }
#     },
#     "required": [
#         "prompt"
#     ]
# }