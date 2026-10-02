"""A run has been made since the server restarted."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

print("A run was made, and its first event told the page which tools the agent has.")
