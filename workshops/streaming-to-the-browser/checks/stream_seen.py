"""A run has been made since the server restarted, and its text left in more than one piece."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Run the command again.")

if last.get("pieces", 0) < 2:
    fail("The reply left the server in one piece. Run the steps on this page again, in order.")

print(f"The reply left the server as {last['pieces']} events of text.")
