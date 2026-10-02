"""The shop's tools are plugged in, and the server has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ("from shop_tools import shop_server", "Import the shop's tools"),
    ('mcp_servers={"shop": shop_server},', "Give the agent the tools, and approve the stock tool"),
    ("mcp__shop__check_stock", "Give the agent the tools, and approve the stock tool"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

if not Path("orders.db").exists():
    fail("The server did not build the orders database. Look in the server terminal for an error.")

print("The server restarted with the shop's tools plugged in, and built the orders database.")
