---
title: What a restart loses
requires: [verify:cleanup-in-place, verify:picked-up, verify:server-stopped]
---

# What a restart loses

A server does not run for ever. It is restarted to change its code,
as yours has been several times in this workshop, or because the
machine was. Everything in its memory goes: the dictionary of
conversations, and with it every client.

## Close them properly

So far the server has let its clients go without a word when it stops.
It should close them, so that each Claude Code process is shut down in
order. FastAPI calls a function of yours as the server starts and
stops, named in the `lifespan` argument: the part before `yield` runs
at the start, and the part after it at the end.

```{editor-insert}
:id: import-context
:title: Import what a lifespan function needs
:path: app.py
:match: from dataclasses import replace
:save: false
from contextlib import asynccontextmanager
```

```{editor-replace}
:id: add-lifespan
:title: Close every conversation when the server stops
:path: app.py
:regex: true
:match: ^app = FastAPI\(title="Tidewater Books chat"\)$


@asynccontextmanager
async def lifespan(app):
    """Run the server, and when it stops, close every conversation it holds."""
    yield
    for conversation in conversations.values():
        await conversation.client.disconnect()
    print(f"closed {len(conversations)} conversations")


app = FastAPI(title="Tidewater Books chat", lifespan=lifespan)
```

Saving that restarted the server once more, and the server that came
up is holding no conversations at all.

```{verify}
:id: cleanup-in-place
:label: The server restarted, and closes its conversations when it stops
:substrate: script
:script: checks/cleanup_in_place.py
:trigger: after:add-lifespan
```

## Carry on regardless

The first visitor knows nothing of this. Their page still has its id.
Ask the next question in the Chat tab, one that again only makes sense
as part of the conversation.

```{url-open}
:id: ask-sunday
:title: Ask about Sunday, in the first conversation
:url: http://127.0.0.1:{{ server_port }}/?ask=And+what+about+on+Sunday%3F
:pane: chat
:label: Chat
:area: chat
```

It answered as though nothing had happened. The server was not holding
a conversation for that id, so it made one, and this is where the two
lines at the top of the `Conversation` class come in. The SDK had a
transcript under that id, so the client was connected with `resume`,
and the session carried on from where it was. The run's entry in
`/status` has `resumed` set, which is what the check reads.

```{verify}
:id: picked-up
:label: The conversation was picked up from its transcript
:substrate: script
:script: checks/picked_up.py
:timeout: 150s
:trigger: after:ask-sunday
```

That is the answer to what a server should keep. In memory, only what
is live: a connected client for each conversation somebody is having
now, which can be closed and made again at any time. The conversation
itself is on disk, in the transcript, and belongs to no particular
process.

One limit comes with that. The transcript is a file on this machine. A
second server on another machine would not find it, which matters to
anyone running more than one. The SDK's documentation on
[session storage](https://code.claude.com/docs/en/agent-sdk/session-storage)
covers keeping transcripts somewhere every server can reach.

## Stop the server

Stop it, and watch the terminal: the function you added reports the
conversations it closed.

```{interrupt}
:id: stop-server
:title: Stop the server
:session: server
```

```{verify}
:id: server-stopped
:label: The server has stopped
:substrate: script
:script: checks/server_stopped.py
:trigger: after:stop-server
```

Press Finish below to end the workshop.
