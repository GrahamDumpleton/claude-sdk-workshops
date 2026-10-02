"""app.py has a route that branches a conversation, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail, routes

source = Path("app.py").read_text()

for needed, step in [
    ("    fork_session,", "Import the function that forks a session"),
    ('@app.post("/fork")', "Add a route that branches a conversation"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

if "/fork" not in routes():
    fail("The server has no route that branches yet. Look in the server terminal for an error.")

print("The server restarted with a route that branches a conversation.")
