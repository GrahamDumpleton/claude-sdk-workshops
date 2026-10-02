"""app.py has a route that stops a turn, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail, routes

source = Path("app.py").read_text()

for needed, step in [
    ("class Which(BaseModel):", "Say what a request to stop looks like"),
    ('@app.post("/stop")', "Add the route that interrupts a turn"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

if "/stop" not in routes():
    fail("The server has no route that stops a turn yet. Look in the server terminal for an error.")

print("The server restarted with a route that stops a turn.")
