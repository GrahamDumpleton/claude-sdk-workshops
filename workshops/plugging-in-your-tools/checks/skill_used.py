"""A run has been made that opened the skill and wrote the reference that only the skill has."""

from _server import fail, runs

last = runs(1)[-1]

if "Skill" not in last.get("calls", []):
    fail("The agent did not open the skill. Ask again with the action above.")

if "RF-3318-Q" not in (last["reply"] or ""):
    fail("The reply does not carry the returns desk reference from the skill. Ask again with the action above.")

print(f"The run called {', '.join(last['calls'])} and its reply carries the reference from the skill.")
