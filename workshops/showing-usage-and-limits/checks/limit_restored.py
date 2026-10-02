"""The turn limit is back at ten, and the server has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

if "max_turns=10," not in Path("app.py").read_text():
    fail('app.py has not had the step "Put the limit back to ten turns" applied, or was not saved.')

current()

print("The server restarted with the limit back at ten turns.")
