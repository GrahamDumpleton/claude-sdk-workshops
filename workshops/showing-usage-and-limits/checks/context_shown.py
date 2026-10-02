"""A run has been made since the server restarted, with a figure for how full its context is."""

from pathlib import Path

from _server import fail, runs

if "context ${event.context}% full" not in Path("page.html").read_text():
    fail('page.html has not had the step "Show how full the context is" applied.')

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if not isinstance(last.get("context"), (int, float)) or last["context"] <= 0:
    fail("The run's record has no figure for the context. Run the steps on this page again, in order.")

print(f"After that turn the conversation's context was {last['context']}% full.")
