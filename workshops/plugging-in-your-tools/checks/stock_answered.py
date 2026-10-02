"""A run has been made that called the stock tool and gave the stock code from the list."""

from _server import fail, runs

last = runs(1)[-1]

if "mcp__shop__check_stock" not in last.get("calls", []):
    fail("The agent did not use the stock tool. Ask again with the action above.")

if "TW-4471-K" not in (last["reply"] or ""):
    fail("The reply does not give the stock code from shop/stock.csv. Ask again with the action above.")

print(f"The run called {', '.join(last['calls'])} and gave the stock code from the list.")
