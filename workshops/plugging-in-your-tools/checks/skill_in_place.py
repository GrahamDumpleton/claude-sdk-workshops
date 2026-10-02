"""The options name the skill, and the server has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ('"Write", "Skill"],', "Give the agent the Skill tool"),
    ('setting_sources=["project"],', "Read the project's settings, and name the skill"),
    ('skills=["refund-reply"],', "Read the project's settings, and name the skill"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

print("The server restarted with the skill named in the agent's options.")
