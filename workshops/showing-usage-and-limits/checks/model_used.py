"""A run has been made, since the server restarted, on the model the page chose."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if "sonnet" not in (last.get("model") or ""):
    fail(f"The run was on {last.get('model')}, not on Sonnet. Ask again with the action above.")

print(f"The turn ran on {last['model']} and sent it {last['sent']} tokens.")
