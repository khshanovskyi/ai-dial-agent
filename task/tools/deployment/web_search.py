from typing import Any

from task.tools.deployment.base import DeploymentTool


class WebSearchTool(DeploymentTool):

    #TODO:
    # 1. Implement `deployment_name` method:
    #   - mark as `@property`
    #   - return deployment name "gemini-2.0-flash-exp-google-search" (or another deployment name with web search model)
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