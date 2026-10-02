"""app.py runs the agent in its chat route, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ("from claude_agent_sdk import", "Import the SDK"),
    ("OPTIONS = ClaudeAgentOptions(", "Say what the agent is"),
    ("def summary(", "Decide what to keep of each run"),
    ("query(prompt=ask.message", "Run the agent in the route"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the four steps in order.')

current()

print("The server restarted with the agent in the route.")
