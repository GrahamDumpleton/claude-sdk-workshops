"""A run has been made in the first conversation, opened by its id."""

import os

from _server import fail, runs

first = os.environ.get("FIRST_CONVERSATION", "")
deadline_runs = runs(1)
found = [run for run in deadline_runs if run["session"] == first]

if not found:
    fail("No run has been made in the first conversation since the server restarted. Open it with the action above.")

last = found[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

how = "was resumed from its transcript" if last["resumed"] else "was still held by the server"
print(f"Session {first[:8]} {how}, and answered in {last['turns']} turn(s).")
