from typing import Optional, Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import CallToolResult, TextContent

from task.tools.mcp.mcp_tool_model import MCPToolModel


class MCPClient:
    """Handles MCP server connection and tool execution"""

    def __init__(self, ) -> None:
        self.session: Optional[ClientSession] = None
        self._streams_context = None
        self._session_context = None

    async def connect(self, mcp_server_url: str):
        """Connect to MCP server"""
        #TODO:
        # 1. Call `streamablehttp_client` method with `mcp_server_url` and assign to `self._streams_context`
        # 2. Call `await self._streams_context.__aenter__()` and assign to `read_stream, write_stream, _`
        # 3. Create `ClientSession(read_stream, write_stream)` and assign to `self._session_context`
        # 4. Call `await self._session_context.__aenter__()` and assign it to `self.session`
        # 5. Call `self.session.initialize()`
        # ---
        # Optional: Ping to MCP server to check the it is alive (method `send_ping`)


    async def get_tools(self) -> list[MCPToolModel]:
        """Get available tools from MCP server"""
        #TODO:
        # 1. Call `await self.session.list_tools()` and assign to `tools`
        # 2. Return list with MCPToolModel:
        #        [
        #             MCPToolModel(
        #                 name=tool.name,
        #                 description=tool.description,
        #                 parameters=tool.inputSchema,
        #             )
        #             for tool in tools.tools
        #         ]


    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        #TODO:
        # 1. Call `await self.session.call_tool(tool_name, tool_args)` and assign to `tool_result` variable
        # 2. Get `content` with index `0` from `tool_result` and assign to `content` variable
        # 3. If `isinstance(content, TextContent)` -> return content.text
        #    else -> return content
        raise
