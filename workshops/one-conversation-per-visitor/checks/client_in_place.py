"""app.py keeps a client for each conversation, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ("import asyncio", "Import what the server needs from Python"),
    ("    ClaudeSDKClient,", "Import the client from the SDK"),
    ("conversations = {}", "Add a place to keep conversations"),
    ("class Conversation:", "Add the Conversation class"),
    ("conversation.turn(ask.message, listener)", "Hand each message to its conversation"),
    ('"conversations": len(conversations)', "Report how many conversations are held"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the six steps in order.')

found = current()

if "conversations" not in found:
    fail("The server that is running is not the new one. Look in the server terminal for an error.")

print("The server restarted, and is holding no conversations yet.")
