import json
from typing import Any

from aidial_sdk.chat_completion import ToolCall, Stage, Choice, Message, Role
from pydantic import StrictStr

from task.tools.base import BaseTool
from task.tools.mcp.mcp_client import MCPClient
from task.tools.mcp.mcp_tool_model import MCPToolModel


class MCPTool(BaseTool):

    pass

    #TODO:
    # Create constructor with:
    #   - client: MCPClient
    #   - mcp_tool_model: MCPToolModel

    #TODO:
    # Override async `execute` method (here we will call mcp tool via mcp `client`):
    #   1. Get arguments as dict (use `json.loads()`) and assign to `arguments` variable
    #   2. Call tool via `client` and assign result as `content` variable
    #   3. Append retrieved content to stage
    #   4. return Message:
    #       - role=Role.TOOL
    #       - content=StrictStr(content)
    #       - tool_call_id=StrictStr(tool_call.id)


    #TODO:
    # 1. Implement `name` method:
    #   - mark as `@property`
    #   - return `self._mcp_tool_model.name`
    # ---
    # 2. Implement `description` method:
    #   - mark as `@property`
    #   - return `self._mcp_tool_model.description`
    # ---
    # 3. Implement `parameters` method:
    #   - mark as `@property`
    #   - return `self._mcp_tool_model.parameters`

