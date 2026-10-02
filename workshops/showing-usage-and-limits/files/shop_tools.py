"""Two tools for the shop's assistant: the stock list and the orders.

Both read and neither can change anything. The stock list is a file,
and the orders are a database opened read-only.
"""

import csv
import json
import sqlite3
from pathlib import Path

from claude_agent_sdk import ToolAnnotations, create_sdk_mcp_server, tool

STOCK = Path("shop/stock.csv")
DATABASE = Path("orders.db")


def build_database():
    """Make the orders database from the SQL file, as a real shop's would already exist."""
    DATABASE.unlink(missing_ok=True)
    connection = sqlite3.connect(DATABASE)
    connection.executescript(Path("data/orders.sql").read_text())
    connection.commit()
    connection.close()


@tool(
    "check_stock",
    "Look up one book in the shop's stock list by its exact title. Returns the "
    "author, the stock code, the number of copies in stock and the shelf. It "
    "matches the whole title only: it cannot search by author, by subject or by "
    "part of a title. If you do not have the exact title, ask for it.",
    {"title": str},
    annotations=ToolAnnotations(readOnlyHint=True),
)
async def check_stock(args):
    wanted = args["title"].strip().lower()
    with STOCK.open(newline="") as handle:
        for book in csv.DictReader(handle):
            if book["title"].lower() == wanted:
                text = (
                    f"{book['title']} by {book['author']}: stock code {book['stock_code']}, "
                    f"{book['copies']} in stock, {book['shelf']}"
                )
                break
        else:
            text = f"No book with the title {args['title']!r} is in the stock list."
    return {"content": [{"type": "text", "text": text}]}


@tool(
    "query_orders",
    "Run one SQL SELECT statement on the shop's orders database, which is SQLite, "
    "and return the rows. The database is read-only. Tables: "
    "customers(customer_id, name, tide_card: 1 for a member of the loyalty scheme, "
    "0 otherwise) and orders(order_id, customer_id, title, quantity, "
    "price_cents: the price of one copy in cents, ordered_on: the date as YYYY-MM-DD).",
    {"sql": str},
    annotations=ToolAnnotations(readOnlyHint=True),
)
async def query_orders(args):
    try:
        connection = sqlite3.connect(f"file:{DATABASE}?mode=ro", uri=True)
        try:
            cursor = connection.execute(args["sql"])
            columns = [column[0] for column in cursor.description or []]
            rows = cursor.fetchmany(50)
        finally:
            connection.close()
    except sqlite3.Error as error:
        return {
            "content": [{"type": "text", "text": f"The query failed: {error}"}],
            "is_error": True,
        }
    return {"content": [{"type": "text", "text": json.dumps({"columns": columns, "rows": rows})}]}


build_database()

shop_server = create_sdk_mcp_server(name="shop", version="1.0.0", tools=[check_stock, query_orders])
