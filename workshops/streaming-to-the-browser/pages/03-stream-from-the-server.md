---
title: Stream from the server
requires: [verify:stream-in-place, verify:stream-seen]
---

# Stream from the server

Two things have to change on the server: what the SDK hands the route,
and what the route sends to the page.

## Ask the SDK for the pieces

The service that runs the model reports a reply as it is produced, as
a series of small events. By default the SDK gathers them up and hands
your code the finished message. One option changes that:
`include_partial_messages=True` passes each event on as well, wrapped
in a message of the type `StreamEvent`.

```{editor-insert}
:id: add-option
:title: Ask for partial messages
:path: app.py
:match: max_turns=10,
:save: false
    include_partial_messages=True,
```

The server needs the name `StreamEvent` to recognise those messages.

```{editor-insert}
:id: add-stream-event
:title: Import StreamEvent
:path: app.py
:match: query,
:save: false
    StreamEvent,
```

## Decide what the page is sent

A `StreamEvent` has an `event`, a dictionary. Most of them mark where
a reply or a block of it starts and stops. The ones that matter here
carry a `delta`, the next piece of the reply, and a delta of the type
`text_delta` holds a few words of text.

The page has no use for the SDK's messages as they are. The function
below turns each message of a run into what the page should be told
about it, as small dictionaries with a `type`. For now there are two:
`text`, with the next few words, and `done`, when the run has ended.
A message the page has no use for yields nothing.

```{editor-insert}
:id: add-events-for
:title: Turn messages into events for the page
:path: app.py
:match: @app.get("/", response_class=HTMLResponse)
:save: false
def events_for(message):
    """Turn one message of a run into the events the page is sent."""
    if isinstance(message, StreamEvent):
        delta = message.event.get("delta", {})
        if delta.get("type") == "text_delta":
            yield {"type": "text", "text": delta["text"]}
    elif isinstance(message, ResultMessage):
        yield {"type": "done", "ended": message.subtype, "seconds": round(message.duration_ms / 1000, 1)}



```

## A response that stays open

An ordinary response is sent whole: the route returns a value and
FastAPI sends it. For a stream the route has to send something, carry
on working, and send something more, down one response that stays open
until the run ends.

The web has a standard form for that, called server-sent events. The
response is text, and each event in it is a line beginning `data:`
followed by a blank line. FastAPI writes that form for you, given two
things: the route says `response_class=EventSourceResponse`, and its
function yields where it used to return. Each value yielded is sent at
once, as one event.

```{editor-insert}
:id: add-sse-import
:title: Import the response for a stream
:path: app.py
:match: from pydantic import BaseModel
:save: false
from fastapi.sse import EventSourceResponse
```

The new route runs the agent as before. For each message it yields
whatever `events_for()` makes of it, so a piece of text leaves for the
page the moment it arrives from the model. It also counts the pieces,
and adds the count to what the server keeps of the run.

```{editor-replace}
:id: replace-route
:title: Yield the events from the route
:path: app.py
:regex: true
:match: ^@app\.post\("/chat"\)[\s\S]*?return \{"reply": result\.result\}$
@app.post("/chat", response_class=EventSourceResponse)
async def chat(ask: Ask):
    pieces = 0
    async for message in query(prompt=ask.message, options=OPTIONS):
        for event in events_for(message):
            if event["type"] == "text":
                pieces += 1
            elif event["type"] == "done":
                runs.append(summary(message, pieces=pieces))
            yield event
```

That step saved the file, and the server restarted.

```{verify}
:id: stream-in-place
:label: The server restarted with a route that streams
:substrate: script
:script: checks/stream_in_place.py
:trigger: after:replace-route
```

## Look at the stream

The page cannot read this yet: it still expects one piece of JSON. So
look at the stream itself first. The command below sends a message to
the route with `curl`, a program that makes web requests from a
terminal, and prints the response as it arrives.

```{execute}
:id: curl-stream
:title: Send a message from the terminal
:session: client
:wait: prompt
:timeout: 120s
curl -sN -X POST http://127.0.0.1:{{ server_port }}/chat -H "Content-Type: application/json" -d '{"message": "Read shop/events.md and say in two sentences what is on this month."}'
```

Each `data:` line is one value the route yielded, written as JSON. The
lines came a few at a time while the model wrote, and the last is the
`done` event. That is everything the page will be sent.

```{verify}
:id: stream-seen
:label: The reply left the server in pieces
:substrate: script
:script: checks/stream_seen.py
:timeout: 150s
:trigger: after:curl-stream
```
