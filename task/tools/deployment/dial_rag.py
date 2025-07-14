from typing import Any

from task.tools.deployment.base import DeploymentTool


class DialRagTool(DeploymentTool):

    @property
    def deployment_name(self) -> str:
        return "dial-rag"

    @property
    def name(self) -> str:
        return "rag_search_tool"

    @property
    def description(self) -> str:
        return "Performs RAG search in text files and returns llm answer based on the search.Always used when user asks for information from attached files.Can perform search in multiple attachments."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "RAG search prompt"
                },
                "attachment_names": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of attachment names for RAG search. If not 100% confident which attachment to use - do not provide this parameter at all."
                }
            },
            "required": [
                "prompt",
                "attachment_names"
            ]
        }