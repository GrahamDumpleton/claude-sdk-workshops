"""A run has been made that queried the orders and named the customer the data gives."""

from _server import fail, runs

last = runs(1)[-1]

if "mcp__shop__query_orders" not in last.get("calls", []):
    fail("The agent did not query the orders. Ask again with the action above.")

if "Ottoline" not in (last["reply"] or ""):
    fail("The reply does not name the customer the orders give. Ask again with the action above.")

print(f"The run called {', '.join(last['calls'])} and named the customer the orders give.")
