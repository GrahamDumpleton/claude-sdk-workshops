"""The done event carries how full the context is, and the server has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ("await self.client.get_context_usage()", "Add how full the context is to the done event"),
    ('context=event["context"],', "Keep the figure with the run"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

print("The server restarted, and asks the client how full the context is after every turn.")
