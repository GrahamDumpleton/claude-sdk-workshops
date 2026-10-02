"""Two runs have been made, and each had a session of its own."""

from _server import fail, runs

found = runs(2)
first, second = found[-2]["session"], found[-1]["session"]

if first == second:
    fail("The last two runs report the same session, which query() does not do. Ask again with the action above.")

print(f"The sessions were {first[:8]} and {second[:8]}.")
