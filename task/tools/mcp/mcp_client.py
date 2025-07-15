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
        if self.session is not None:
            return  # Already connected

        self._streams_context = streamablehttp_client(mcp_server_url)
        read_stream, write_stream, _ = await self._streams_context.__aenter__()

        self._session_context = ClientSession(read_stream, write_stream)
        self.session: ClientSession = await self._session_context.__aenter__()

        await self.session.initialize()

        if not await self.session.send_ping():
            raise ValueError("MCP server connection failed")


    async def get_tools(self) -> list[MCPToolModel]:
        """Get available tools from MCP server"""

        tools = await self.session.list_tools()
        return [
            MCPToolModel(
                name=tool.name,
                description=tool.description,
                parameters=tool.inputSchema,
            )
            for tool in tools.tools
        ]

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        tool_result: CallToolResult = await self.session.call_tool(tool_name, tool_args)
        content = tool_result.content[0]

        if isinstance(content, TextContent):
            return content.text

        return content
