"""The stock list of Tidewater Books, offered as an MCP server.

Run as a program, this speaks the Model Context Protocol on its
standard input and output. Any MCP client can start it and use its
tools. Nothing here knows about Claude or the Agent SDK.
"""

import csv
from pathlib import Path

from mcp.types import ToolAnnotations

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:  # version 1 of the mcp package calls it FastMCP
    from mcp.server.fastmcp import FastMCP as MCPServer

STOCK_FILE = Path(__file__).parent / "shop" / "stock.csv"

READ_ONLY = ToolAnnotations(readOnlyHint=True)

server = MCPServer("tidewater-stock")


def load_stock():
    with STOCK_FILE.open(newline="") as handle:
        return list(csv.DictReader(handle))


@server.tool(annotations=READ_ONLY)
def check_stock(title: str) -> str:
    """Look up one book in the shop's stock list by its exact title.

    Returns the author, the stock code, the number of copies in stock
    and the shelf. It matches the whole title only: it cannot search by
    author, by subject or by part of a title.
    """
    wanted = title.strip().lower()
    for book in load_stock():
        if book["title"].lower() == wanted:
            return (
                f"{book['title']} by {book['author']}: stock code {book['stock_code']}, "
                f"{book['copies']} in stock, {book['shelf']}"
            )
    return f"No book with the title {title!r} is in the stock list."


@server.tool(annotations=READ_ONLY)
def books_by_author(author: str) -> str:
    """List every book in the shop's stock list by one author.

    Takes the author's name. Returns each title with its stock code and
    the number of copies in stock.
    """
    wanted = author.strip().lower()
    found = [
        f"{book['title']}: stock code {book['stock_code']}, {book['copies']} in stock"
        for book in load_stock()
        if book["author"].lower() == wanted
    ]
    return "\n".join(found) or f"No books by {author!r} are in the stock list."


if __name__ == "__main__":
    server.run()
