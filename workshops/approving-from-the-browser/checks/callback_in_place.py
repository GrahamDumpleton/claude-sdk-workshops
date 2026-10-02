"""app.py has the callback and everything it needs, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ("from uuid import UUID, uuid4", "Import a way to make ids"),
    ("    PermissionResultAllow,", "Import the two answers a callback can give"),
    ("questions = {}", "Add a place for questions that are waiting"),
    ("self.calls, self.answers, self.listener = [], [], listener", "Keep each turn's listener and answers"),
    ("calls=self.calls, answers=self.answers))", "Keep the answers with the run"),
    ("async def approve(self, tool_name, tool_input, context):", "Add the method that puts the question to the page"),
    ("replace(OPTIONS, can_use_tool=self.approve)", "Name the method as the conversation's callback"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the seven steps in order.')

current()

print("The server restarted. A call that needs approval is now put to the page, which cannot show it yet.")
