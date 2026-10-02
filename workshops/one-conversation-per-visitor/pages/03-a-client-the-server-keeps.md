---
title: A client the server keeps
requires: [verify:client-in-place]
---

# A client the server keeps

Underneath, the SDK runs Claude Code as a separate process. `query()`
starts that process, runs one exchange and shuts it down. A
`ClaudeSDKClient` starts it and leaves it running, with one session
open inside it, and takes one message after another:
`await client.query(text)` sends a message, and
`client.receive_response()` hands back the messages of the reply.

So the server will keep a client for each conversation id, connected
for as long as the server runs. That takes six changes to
{open}`app.py`. The file is saved, and the server restarted, by the
last.

## What the server needs

First the names: from Python, and from the SDK. The client replaces
`query()`, which the server no longer calls.

```{editor-replace}
:id: python-imports
:title: Import what the server needs from Python
:path: app.py
:regex: true
:match: ^import time\nfrom pathlib import Path$
:save: false
import asyncio
import time
from dataclasses import replace
from pathlib import Path
```

```{editor-replace}
:id: sdk-imports
:title: Import the client from the SDK
:path: app.py
:regex: true
:match: ^    ResultMessage,\n    StreamEvent,\n    query,$
:save: false
    ClaudeSDKClient,
    ResultMessage,
    StreamEvent,
    get_session_info,
```

## Somewhere to keep them

The conversations go in a dictionary, with the id as the key. It is an
ordinary dictionary in the server's memory, there for as long as the
server process runs.

```{editor-replace}
:id: add-state
:title: Add a place to keep conversations
:path: app.py
:regex: true
:match: ^started = .*\nruns = .*$
:save: false
WORKSPACE = Path.cwd().resolve()  # the directory the server runs in, where the agent works
started = time.time()  # when this server process began
runs = []  # what the server has kept about each run since it started
conversations = {}  # conversation id -> the Conversation the server is holding
```

## A conversation

What the dictionary holds is an object of the class below, one for
each conversation. Read it in three parts.

**Making one.** The id the page chose becomes the id of the SDK's
session, through the `session_id` option. If the SDK already has a
session under that id, the `resume` option picks it up where it left
off. You will see why that matters on the last page. Either way the
options are a copy of `OPTIONS` with one field changed, and the client
is made from them.

**A turn.** `turn()` sends one message and reads the reply, turning
each message of the run into events with `events_for()`, as the route
did. It does not send the events to the page itself. It puts them on a
queue, a line that something else takes them off at the other end, and
it puts `None` last to say the turn is over. So a turn does not depend
on anybody listening. If the page goes away half way through a reply,
the turn still finishes, and the reply is still part of the
conversation.

**One at a time.** A session can take one message at a time. The lock,
`self.turns`, makes a second message wait until the first has been
answered.

Below the class, `conversation_for()` finds the conversation for an
id, and makes and connects one if the server is not holding it.

```{editor-insert}
:id: add-conversation
:title: Add the Conversation class
:path: app.py
:match: @app.get("/", response_class=HTMLResponse)
:save: false
class Conversation:
    """A conversation the server is holding: a connected client, and its turns kept in order."""

    def __init__(self, key):
        self.resumed = get_session_info(key, directory=str(WORKSPACE)) is not None
        options = replace(OPTIONS, resume=key) if self.resumed else replace(OPTIONS, session_id=key)
        self.client = ClaudeSDKClient(options=options)
        self.turns = asyncio.Lock()

    async def turn(self, text, listener):
        """Run one turn, putting each event of it on the listener's queue, and None when it is over."""
        async with self.turns:
            try:
                await self.client.query(text)
                async for message in self.client.receive_response():
                    for event in events_for(message):
                        self.note(event, message)
                        listener.put_nowait(event)
            finally:
                listener.put_nowait(None)

    def note(self, event, message):
        """Keep what the server wants to remember of one event of a turn."""
        if event["type"] == "done":
            runs.append(summary(message, resumed=self.resumed))


async def conversation_for(key):
    """Return the conversation with this id, connecting a client for it if the server holds none."""
    if key not in conversations:
        conversations[key] = Conversation(key)
        await conversations[key].client.connect()
    return conversations[key]



```

## The route

The route gets shorter. It finds the conversation, makes a queue to
listen on, starts the turn as a task of its own, and yields whatever
comes off the queue until the `None`.

`asyncio.create_task()` is what lets the turn outlive the request: the
task runs on the server's event loop, alongside the route and not
inside it. The task is kept on the conversation so that Python does
not discard it while it runs.

```{editor-replace}
:id: replace-route
:title: Hand each message to its conversation
:path: app.py
:regex: true
:match: ^    pieces = 0[\s\S]*?^            yield event$
:save: false
    conversation = await conversation_for(str(ask.conversation))
    listener = asyncio.Queue()
    conversation.running = asyncio.create_task(conversation.turn(ask.message, listener))
    while (event := await listener.get()) is not None:
        yield event
```

Last, `/status` reports how many conversations the server is holding.

```{editor-replace}
:id: status-counts
:title: Report how many conversations are held
:path: app.py
:match: return {"started": started, "runs": runs}
return {"started": started, "conversations": len(conversations), "runs": runs}
```

```{verify}
:id: client-in-place
:label: The server restarted with a client for each conversation
:substrate: script
:script: checks/client_in_place.py
:trigger: after:status-counts
```
