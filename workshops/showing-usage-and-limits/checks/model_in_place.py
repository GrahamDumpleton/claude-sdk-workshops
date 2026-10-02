"""app.py has a route that changes the model, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail, routes

source = Path("app.py").read_text()

for needed, step in [
    ('MODELS = ["haiku", "sonnet"]', "Name the models the page may choose"),
    ("class Choice(BaseModel):", "Say what a choice of model looks like"),
    ('@app.post("/model")', "Add the route that changes the model"),
    ('self.model = event["model"]', "Remember the model each turn ran on"),
    ("model=self.model,", "Keep the model with the run"),
    ('not block["text"].startswith("<")', "Leave the SDK's own notes out of what was said"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the six steps in order.')

current()

if "/model" not in routes():
    fail("The server has no route that changes the model yet. Look in the server terminal for an error.")

print("The server restarted with a route that changes the model.")
