"""The server's list has the first conversation."""

import os

from _server import fail, get

first = os.environ.get("FIRST_CONVERSATION", "")
listed = {item["id"]: item["title"] for item in get("/conversations")}

if first not in listed:
    fail("The server's list does not have the first conversation. Go back a page and start it.")

print(f"The server lists {len(listed)} conversation(s). The first is titled: {listed[first]}")
