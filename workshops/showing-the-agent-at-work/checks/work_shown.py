"""A run has been made, since the server restarted, that called at least one tool."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if not last.get("calls"):
    fail("The agent answered without using a tool. Ask again with the action above.")

print(f"The run called {', '.join(last['calls'])}, and the page was sent an event for each.")
