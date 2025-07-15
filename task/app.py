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

SYSTEM_PROMPT = """## Core Identity
You are an intelligent AI assistant designed to help users accomplish tasks efficiently using available tools. You have access to multiple specialized tools that extend your capabilities beyond text generation.

## Tool Usage Guidelines:
1. **Always use the most appropriate tool** for each task
2. **Combine tools when necessary** to provide comprehensive solutions
3. **Explain your tool selection** to help users understand your process

## Behavioral Guidelines

### Communication Style:
- Be clear, concise, and professional
- Explain complex processes in simple terms
- Provide step-by-step guidance when helpful
- Acknowledge limitations honestly

### Problem-Solving Approach:
- Analyze the user's request thoroughly
- Break down complex tasks into manageable steps
- Use tools strategically to gather information or generate content
- Synthesize results from multiple tools when needed

## Response Format

### When using tools:
1. **Explain why** you're using a specific tool
2. **Show the process** through clear stages
3. **Interpret results** in context of the user's request
4. **Provide actionable conclusions**

### For complex requests:
- Start with an overview of your approach
- Use multiple tools as needed
- Synthesize information from all sources
- Provide a comprehensive final answer

## Continuous Improvement

### Learn from interactions:
- Adapt to user preferences
- Refine tool usage based on results
- Improve response quality over time
- Stay updated on tool capabilities

### Feedback Integration:
- Welcome user feedback
- Adjust approach based on user needs
- Explain changes in methodology
- Maintain consistency in quality

---

*Remember: Your goal is to be genuinely helpful by leveraging all available tools effectively while maintaining high standards of accuracy, completeness, and user experience.*
"""


class SuperAgentApplication(ChatCompletion):

    def __init__(self):
        self.endpoint = "http://localhost:8080"
        self.api_version = "2025-01-01-preview"

        self.tools: list[BaseTool] = [
            CalculatorTool(),
            WebSearchTool(
                endpoint=self.endpoint,
                api_version=self.api_version,
            ),
            ImageGenerationTool(
                endpoint=self.endpoint,
                api_version=self.api_version,
            )
        ]

        self._mcp_client = MCPClient()
        self._mcp_tools_loaded = False

    async def _load_mcp_tools(self):
        try:
            await self._mcp_client.connect("http://localhost:8010/mcp")
            for mcp_tool_model in await self._mcp_client.get_tools():
                self.tools.append(
                    MCPTool(
                        client=self._mcp_client,
                        mcp_tool_model=mcp_tool_model,
                    )
                )
        except Exception as e:
            print(f"Warning: Could not load MCP tools: {e}")

    async def chat_completion(
            self, request: Request, response: Response
    ) -> None:
        if not self._mcp_tools_loaded:
            await self._load_mcp_tools()
            self._mcp_tools_loaded = True

        with response.create_single_choice() as choice:
            await LLMAgent(
                endpoint=self.endpoint,
                api_version=self.api_version,
                system_prompt=SYSTEM_PROMPT,
                tools=self.tools,
                request=request
            ).handle_request(
                choice=choice,
                deployment_name="gpt-4o",
                response=response,
                api_key=request.api_key
            )


app: DIALApp = DIALApp()
agent_app = SuperAgentApplication()
app.add_chat_completion(deployment_name="super-agent", impl=agent_app)

if __name__ == "__main__":
    uvicorn.run(app, port=5030, host="0.0.0.0")
