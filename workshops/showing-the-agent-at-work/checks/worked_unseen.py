"""A run has been made that took more than one turn."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if last["turns"] < 2:
    fail("The agent answered without using a tool. Ask again with the action above.")

print(f"The run took {last['turns']} turns and {last['seconds']} seconds, and the page showed three dots.")
