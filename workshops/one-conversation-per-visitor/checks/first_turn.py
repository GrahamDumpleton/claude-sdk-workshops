"""A run has been made in a conversation the server is holding."""

from _server import fail, runs, status

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

held = status()["conversations"]

if held < 1:
    fail("The server is holding no conversation. Ask again with the action above.")

print(f"The server is holding {held} conversation, in session {last['session'][:8]}.")
