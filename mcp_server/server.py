import random

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="simple-mcp-server",
    host="0.0.0.0",
    port=8010,
    log_level="DEBUG"
)


@mcp.tool()
async def reverse_string(incoming: str) -> str:
    """Reverses the order of characters in a given text."""
    return incoming[::-1]


@mcp.tool()
async def random_num(start: int, stop: int) -> int:
    """Generate a random integer between start and stop (inclusive)"""
    return random.randint(start, stop)


@mcp.tool()
async def is_palindrome(text) -> bool:
    """
    Check if a string is a palindrome (reads the same forwards and backwards).
    Ignores case, spaces, and punctuation.
    """
    cleaned = ''.join(char.lower() for char in text if char.isalnum())

    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )
