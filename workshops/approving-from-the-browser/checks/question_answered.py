"""A run has been made, since the server restarted, in which the page was asked and an answer came."""

from pathlib import Path

from _server import fail, runs

last = runs(1, wait=200)[-1]
answers = last.get("answers", [])

if not answers:
    fail("The agent did not ask to write a notice, so nothing was put to the page. Ask again with the action above.")

written = Path("notices/author-evening.md").exists()

if "allowed" in answers and not written:
    fail("The write was allowed and notices/author-evening.md is not there. Ask again with the action above.")

print(f"The page was asked, and the answer was: {', '.join(answers)}. The notice was {'written' if written else 'not written'}.")
