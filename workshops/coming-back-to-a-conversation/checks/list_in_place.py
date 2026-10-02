"""app.py has a route that lists conversations, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail, routes

source = Path("app.py").read_text()

for needed, step in [
    ("    list_sessions,", "Import the function that lists sessions"),
    ('@app.get("/conversations")', "Add a route that lists the conversations"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

if "/conversations" not in routes():
    fail("The server has no route for the list yet. Look in the server terminal for an error.")

print("The server restarted with a route that lists conversations.")
