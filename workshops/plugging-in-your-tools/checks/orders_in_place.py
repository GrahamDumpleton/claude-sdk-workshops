"""Both of the shop's tools are approved, and the server has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

if 'allowed_tools=["mcp__shop__check_stock", "mcp__shop__query_orders"],' not in source:
    fail('app.py has not had the step "Approve the orders tool as well" applied, or was not saved.')

current()

print("The server restarted with both of the shop's tools approved.")
