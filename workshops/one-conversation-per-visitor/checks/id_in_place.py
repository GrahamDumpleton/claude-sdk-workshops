"""The page sends a conversation id, and the server restarted expecting one."""

from pathlib import Path

from _server import current, fail, get

page = Path("page.html").read_text()
source = Path("app.py").read_text()

for text, needed, step in [
    (page, 'localStorage.setItem("conversation", conversation);', "Give the page an id for its conversation"),
    (page, 'post("/chat", {conversation, message: text})', "Send the id with every message"),
    (source, "from uuid import UUID", "Import the UUID type"),
    (source, "    conversation: UUID", "Expect an id with every message"),
]:
    if needed not in text:
        fail(f'The step "{step}" has not been applied, or its file was not saved. Run the four steps in order.')

current()

fields = get("/openapi.json")["components"]["schemas"]["Ask"]["properties"]

if "conversation" not in fields:
    fail("The server does not expect an id with a message yet. Run the last step again.")

print("The page sends an id with every message, and the server refuses a message without one.")
