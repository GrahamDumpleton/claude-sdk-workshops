"""The done event carries what a turn used, and the server has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ('"written": usage.get("output_tokens", 0),', "Put what the turn used in the done event"),
    ('sent=event["sent"],', "Keep what was sent with the run"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

print("The server restarted, and its done event carries what the turn sent and wrote.")
