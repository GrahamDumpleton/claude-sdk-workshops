"""A run has been made, and it ended well."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

print(f"The run took {last['seconds']} seconds, and the page showed nothing until it was over.")
