import random

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    #TODO:
    # Configure FastMCP server:
    #   - name="simple-mcp-server"
    #   - host="0.0.0.0"
    #   - port=8010
    #   - log_level="DEBUG"

)

#TODO:
# Create tools:
# 1. Create async `reverse_string` method:
#   - mark as `@mcp.tool()`
#   - Parameters:
#       - incoming: str
#   - returns str
#   - Documentation: Reverses the order of characters in a given text.
#   - Provide implementation for method
# 2. Create async `random_num` method:
#   - mark as `@mcp.tool()`
#   - Parameters:
#       - start: int
#       - stop: int
#   - returns int
#   - Documentation: Generate a random integer between start and stop (inclusive).
#   - Provide implementation for method
# 3. Create async `is_palindrome` method:
#   - mark as `@mcp.tool()`
#   - Parameters:
#       - text: str
#   - returns bool
#   - Documentation: Check if a string is a palindrome (reads the same forwards and backwards). Ignores case, spaces, and punctuation.
#   - Provide implementation for method


if __name__ == "__main__":
    pass
    #TODO:
    # Run mcp server with such configuration:
    #   - transport="streamable-http"
