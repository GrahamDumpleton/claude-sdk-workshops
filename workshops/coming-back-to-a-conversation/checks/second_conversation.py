"""A run has been made since the server restarted, and the server lists at least two conversations."""

from _server import fail, get, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if last["resumed"]:
    fail("That run carried on an old conversation. Ask again with the action above, which starts a new one.")

listed = get("/conversations")

if len(listed) < 2:
    fail("The server lists fewer than two conversations. Go back and have the first one.")

print(f"The server now lists {len(listed)} conversations.")
