"""The agent's options give it Write, and the server has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ("the notices directory.", "Tell the agent where notices go"),
    ('tools=["Read", "Glob", "Grep", "Write"],', "Give the agent the Write tool"),
    ('permission_mode="default",', "Give the agent the Write tool"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

print("The server restarted, and its agent has the Write tool under the standard rules.")
