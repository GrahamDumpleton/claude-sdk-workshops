"""A run has been made in which the agent asked to write, and no notice was written."""

from pathlib import Path

from _server import fail, runs

last = runs(1)[-1]

if "Write" not in last.get("calls", []):
    fail("The agent did not ask to write anything. Ask again with the action above.")

if Path("notices/door.md").exists():
    fail("notices/door.md exists, so something allowed the write. Delete the notices directory and ask again.")

print("The agent asked for Write, the call was refused, and no file was written.")
