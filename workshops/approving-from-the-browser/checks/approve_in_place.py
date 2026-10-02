"""app.py has a route for the answer, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail, routes

source = Path("app.py").read_text()

for needed, step in [
    ("replace(OPTIONS, can_use_tool=self.approve)", "the steps of the page before this one"),
    ("class Answer(BaseModel):", "Say what an answer from the page looks like"),
    ('@app.post("/approve")', "Add the route that completes the future"),
]:
    if needed not in source:
        fail(f'app.py is missing "{step}", or was not saved. Run the steps in order.')

current()

if "/approve" not in routes():
    fail("The server has no route for the answer yet. Look in the server terminal for an error.")

print("The server restarted with the callback and a route for the answer.")
