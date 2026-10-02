"""A run has been made, since the server restarted, in a session resumed from its transcript."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if not last["resumed"]:
    fail("That run was in a new conversation. Ask again with the action above, which uses the first chat.")

print(f"Session {last['session'][:8]} was resumed from its transcript, and took {last['turns']} turn(s).")
