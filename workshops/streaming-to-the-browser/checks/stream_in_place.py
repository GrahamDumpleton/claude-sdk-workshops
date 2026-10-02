"""app.py streams from its chat route, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail, routes

source = Path("app.py").read_text()

for needed, step in [
    ("include_partial_messages=True", "Ask for partial messages"),
    ("    StreamEvent,", "Import StreamEvent"),
    ("def events_for(", "Turn messages into events for the page"),
    ("from fastapi.sse import EventSourceResponse", "Import the response for a stream"),
    ("response_class=EventSourceResponse", "Yield the events from the route"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the five steps in order.')

current()

kinds = routes()["/chat"]["post"]["responses"]["200"]["content"]

if "text/event-stream" not in kinds:
    fail("The chat route does not answer with a stream of events. Run the last step again.")

print("The server restarted, and the chat route answers with a stream of events.")
