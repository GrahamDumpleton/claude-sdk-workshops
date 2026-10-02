"""A run has been made since the server restarted, and what it sent was recorded."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if not last.get("sent"):
    fail("The run's record has nothing for what was sent. Run the steps on this page again, in order.")

print(f"The turn sent the model {last['sent']} tokens over {last['turns']} turn(s).")
