"""app.py has a route for what was said, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail, routes

source = Path("app.py").read_text()

for needed, step in [
    ("    get_session_messages,", "Import the function that reads a transcript"),
    ('@app.get("/history/{conversation}")', "Add a route for what was said"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

if "/history/{conversation}" not in routes():
    fail("The server has no route for what was said yet. Look in the server terminal for an error.")

print("The server restarted with a route for what was said.")
