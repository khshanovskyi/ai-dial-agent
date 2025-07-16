import uvicorn

from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response

from task.llm_agent import LLMAgent
from task.tools.base import BaseTool
from task.tools.calculator import CalculatorTool
from task.tools.deployment.image_generation import ImageGenerationTool
from task.tools.deployment.web_search import WebSearchTool
from task.tools.mcp.mcp_client import MCPClient
from task.tools.mcp.mcp_tool import MCPTool

#TODO:
# STEP 1:
# Create system prompt for Agent:
#   - explain role
#   - provide guidelines of tools usage
#   - response format
# ---
# JFI: Prompt configuration is hard and time consuming task. For this case you are free to use LLM, but always check it,
# don't use it blindly!
SYSTEM_PROMPT = None


class SuperAgentApplication(ChatCompletion):

    def __init__(self):
        self.endpoint = "http://localhost:8080"
        self.api_version = "2025-01-01-preview"

        #TODO:
        # STEP 1:
        # Create list with tools and assign as `self.tools: list[BaseTool]`:
        #   - Add CalculatorTool (need to implement)


        #TODO:
        # STEP 1:
        # - Add WebSearchTool with `endpoint` and `api_version` (need to implement)
        # - Add ImageGenerationTool with `endpoint` and `api_version` (need to implement)


        #TODO:
        # STEP 3:
        # 1. Create MCPClient and assign as `self._mcp_client`
        # 2. Create `self._mcp_tools_loaded` variable with `False`


    async def _load_mcp_tools(self):
        #TODO:
        # STEP 3:
        # 1. Connect to MCP server, mcp_server_url="http://localhost:8010/mcp"
        # 2. With mcp client get tools and then append them to the `self.tools` as MCPTool. (The `get_tools()`
        #   returns a list with MCPToolModel that we need to pass when creating MCPTool from each model)
        pass

    async def chat_completion(
            self, request: Request, response: Response
    ) -> None:
        #TODO:
        # STEP 3:
        # If not `self._mcp_tools_loaded` then call `await self._load_mcp_tools()` and set `self._mcp_tools_loaded` as True


        #TODO:
        # STEP 1:
        # 2. Create `choice` (`with response.create_single_choice() as choice:`) and:
        #   - Create LLMAgent with:
        #       - endpoint=self.endpoint
        #       - api_version=self.api_version
        #       - system_prompt=SYSTEM_PROMPT
        #       - tools=self.tools
        #       - request=request
        #   - call `handle_request` on created agent with:
        #       - choice=choice
        #       - deployment_name="gpt-4o"
        #       - response=response
        #       - api_key=request.api_key
        raise


#TODO:
# STEP 1:
# 1. create DIALApp and assign it to `app` variable. (DIALApp extends FastAPI that is the main entrypoint to use FastAPI)
# 2. Create SuperAgentApplication and assign it to `agent_app` variable
# 3. Add chat completion to `app`:
#   - deployment_name="super-agent"
#   - impl=agent_app
# 4. Run it with uvicorn: `uvicorn.run(app, port=5030, host="0.0.0.0")`

