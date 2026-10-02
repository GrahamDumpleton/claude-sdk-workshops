"""The server returns what was said in the most recent conversation, read from its transcript."""

import os
from pathlib import Path

from _server import fail, get
from claude_agent_sdk import list_sessions

if "async function start()" not in Path("page.html").read_text():
    fail('page.html has not had the step "Show what was said when the page loads" applied.')

sessions = list_sessions(directory=os.getcwd(), include_worktrees=False)

if not sessions:
    fail("The SDK has no session for this directory. Go back a page and ask the two questions.")

said = get("/history/" + sessions[0].session_id)
speakers = {item["role"] for item in said}

if len(said) < 4 or speakers != {"user", "assistant"}:
    fail("The conversation has fewer than two exchanges in it. Go back a page and ask the two questions.")

print(f"The server returned {len(said)} pieces of text from the transcript of session {sessions[0].session_id[:8]}.")
