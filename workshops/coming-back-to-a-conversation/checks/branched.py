"""A run has been made in a branch of the first conversation, and the original does not have its question."""

import os

from _server import fail, get, runs

first = os.environ.get("FIRST_CONVERSATION", "")
last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Branch again with the action above.")

if last["session"] == first:
    fail("That run was in the first conversation itself, not in a branch. Branch again with the action above.")

question = "And when is story time?"
original = [item["text"] for item in get("/history/" + first)]
branch = [item["text"] for item in get("/history/" + last["session"])]

if question in original:
    fail("The question asked in the branch is in the original conversation, which a fork should leave alone.")

if question not in branch or len(branch) <= len(original):
    fail("The branch does not hold the original's history and the new question. Branch again with the action above.")

print(
    f"The branch is session {last['session'][:8]}, with {len(branch)} pieces of text. "
    f"The original, {first[:8]}, still has {len(original)}."
)
