"""The page has a Stop button, and a run has ended since the server restarted. Says how it ended."""

from pathlib import Path

from _server import fail, runs

page = Path("page.html").read_text()

if 'id="stop"' not in page or 'post("/stop", {conversation})' not in page:
    fail("page.html has no working Stop button. Run the two steps under \"A button for it\".")

last = runs(1)[-1]

if last["ended"] == "success":
    print("The run ended with success: it finished before it was stopped. Ask again and press Stop sooner to see one interrupted.")
else:
    print(f"The run ended with {last['ended']} after {last['seconds']} seconds: it was stopped part way.")
