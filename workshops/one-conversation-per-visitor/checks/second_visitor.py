"""A run has been made, since the server restarted, in a session that is not the first visitor's."""

import os

from _server import fail, runs
from claude_agent_sdk import list_sessions

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Open the second visitor again with the action above.")

if last["resumed"]:
    fail("That run carried on an old conversation. Open the second visitor again with the action above.")

known = {session.session_id for session in list_sessions(directory=os.getcwd(), include_worktrees=False)}

if len(known) < 2:
    fail("The SDK has only one session for this directory. Go back and ask the first visitor's questions.")

print(f"The second visitor's session is {last['session'][:8]}, one of {len(known)} the SDK has for this directory.")
