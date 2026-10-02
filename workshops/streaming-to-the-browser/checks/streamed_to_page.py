"""A second run has been made since the server restarted, and it too was streamed."""

from _server import fail, runs

last = runs(2)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if last.get("pieces", 0) < 2:
    fail("The reply left the server in one piece. Ask again with the action above.")

print(f"The page was sent {last['pieces']} events of text over {last['seconds']} seconds.")
