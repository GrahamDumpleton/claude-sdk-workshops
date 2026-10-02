"""A run has been made in a conversation with the id chosen on the welcome page."""

import os

from _server import fail, runs

first = os.environ.get("FIRST_CONVERSATION", "")
found = [run for run in runs(1) if run["session"] == first]

if not found:
    fail("No run has been made under the id chosen on the welcome page. Start the conversation with the action above.")

if found[-1]["ended"] != "success":
    fail(f"The run ended with {found[-1]['ended']}. Ask again with the action above.")

print(f"The conversation is session {first[:8]}, and its transcript is on disk.")
