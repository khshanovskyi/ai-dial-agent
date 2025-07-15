from typing import Any

from task.tools.deployment.base import DeploymentTool


class WebSearchTool(DeploymentTool):

    @property
    def deployment_name(self) -> str:
        return "gemini-2.5-pro-preview-03-25-google-search"

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "Performs WEB search."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The search query or question to search for on the web"
                }
            },
            "required": ["prompt"]
        }