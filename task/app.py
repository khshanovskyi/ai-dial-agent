import uvicorn

from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response

from task.llm_agent import LLMAgent
from task.tools.base import BaseTool
from task.tools.deployment.dial_rag import DialRagTool
from task.tools.deployment.web_search import WebSearchTool

SYSTEM_PROMPT = """Your goal is to assist users with their tasks.
"""


class SuperAgentApplication(ChatCompletion):

    def __init__(self):
        self.endpoint = "http://localhost:8080"
        self.api_key = "dial_api_key"
        self.api_version = "2025-01-01-preview"

        self.tools: list[BaseTool] = [
            DialRagTool(
                endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
            ),
            WebSearchTool(
                endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
            )
        ]

    async def chat_completion(
            self, request: Request, response: Response
    ) -> None:
        with response.create_single_choice() as choice:
            await LLMAgent(
                endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
                system_prompt=SYSTEM_PROMPT,
                tools=self.tools,
                request=request
            ).handle_request(
                choice=choice,
                deployment_name="gpt-4o",
                # deployment_name="anthropic.claude-sonnet-4-20250514-v1:0",
                response=response
            )


app: DIALApp = DIALApp()
app.add_chat_completion(deployment_name="super-agent", impl=SuperAgentApplication())

if __name__ == "__main__":
    uvicorn.run(app, port=5030, host="0.0.0.0")
