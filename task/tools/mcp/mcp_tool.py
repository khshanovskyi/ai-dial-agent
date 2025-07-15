import json
from typing import Any

from aidial_sdk.chat_completion import ToolCall, Stage, Choice, Message, Role
from pydantic import StrictStr

from task.tools.base import BaseTool
from task.tools.mcp.mcp_client import MCPClient
from task.tools.mcp.mcp_tool_model import MCPToolModel


class MCPTool(BaseTool):

    def __init__(self, client: MCPClient, mcp_tool_model: MCPToolModel):
        self._client = client
        self._mcp_tool_model = mcp_tool_model

    async def execute(self, tool_call: ToolCall, stage: Stage, choice: Choice, api_key: str) -> Message:
        arguments = json.loads(tool_call.function.arguments)

        content = await self._client.call_tool(self.name, arguments)

        stage.append_content(content)

        return Message(
            role=Role.TOOL,
            content=StrictStr(content),
            tool_call_id=StrictStr(tool_call.id),
        )

    @property
    def name(self) -> str:
        return self._mcp_tool_model.name

    @property
    def description(self) -> str:
        return self._mcp_tool_model.description

    @property
    def parameters(self) -> dict[str, Any]:
        return self._mcp_tool_model.parameters
