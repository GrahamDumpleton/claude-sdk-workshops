"""app.py sends events for tool requests and results, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ("    ToolUseBlock,", "Import the message and block types"),
    ('yield {"type": "tool", "id": block.id', "Send the page an event for each request and result"),
    ("self.calls = []", "Start each turn with an empty list of calls"),
    ("calls=self.calls", "Keep the name of each tool a turn calls"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the four steps in order.')

current()

print("The server restarted, and sends the page an event for each tool request and result.")
