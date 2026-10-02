"""The turn limit is two, and the server has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

if "max_turns=2," not in Path("app.py").read_text():
    fail('app.py has not had the step "Lower the limit to two turns" applied, or was not saved.')

current()

print("The server restarted with a limit of two turns.")
