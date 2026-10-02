---
title: Put the agent behind it
requires: [verify:agent-in-place, verify:agent-answered]
---

# Put the agent behind it

The route that answers a message is ordinary Python, so it can do
anything Python can, including run an agent. Four small changes to
{open}`app.py` put one there. The first three change nothing the
server does, and the file is saved once, by the last.

## The SDK

First the names the server needs from the SDK: `query()`, which runs
an agent once, the options it takes, and the message that ends a run.

```{editor-insert}
:id: add-imports
:title: Import the SDK
:path: app.py
:match: from fastapi import FastAPI
:save: false
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ResultMessage,
    query,
)
```

## What the agent is

Next the options, which say what this agent is: the smallest model, a
standing instruction that makes it the bookshop's assistant, and the
three tools that find and read files, `Read`, `Glob` and `Grep`. With
those it can look things up in the `shop` directory beside the server,
which holds the shop's documents, such as
{open}`shop/opening-hours.md`.

The options are made once, when the server starts, and used for every
message.

```{editor-insert}
:id: add-options
:title: Say what the agent is
:path: app.py
:match: started = time.time()
:save: false
OPTIONS = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "The shop's documents are in the shop directory. Answer from them, briefly, "
        "in plain text with no Markdown. Give the answer only: do not say what you "
        "are about to do."
    ),
    tools=["Read", "Glob", "Grep"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=10,
)


```

The agent's working directory is the directory the server was started
in, which is this workshop's own. Nothing in the options points it
anywhere else.

## What to keep of a run

A run ends with a `ResultMessage`, which says how it went. The
function below picks out what the server will keep of each one: the
session it ran in, how it ended, how many turns it took, how long, and
the reply. The route adds that to `runs`, the list `/status` reports.

```{editor-insert}
:id: add-summary
:title: Decide what to keep of each run
:path: app.py
:match: @app.get("/", response_class=HTMLResponse)
:save: false
def summary(result, **more):
    """What the server keeps about one run, with anything more it is handed."""
    return {
        "session": result.session_id,
        "ended": result.subtype,
        "turns": result.num_turns,
        "seconds": round(result.duration_ms / 1000, 1),
        "reply": result.result,
        **more,
    }



```

## The route

Last, the route itself. In place of the canned reply it runs the
agent, with the message from the page as the prompt.

```{editor-replace}
:id: replace-route
:title: Run the agent in the route
:path: app.py
:regex: true
:match: ^ +return \{"reply": f"You said.*$
    async for message in query(prompt=ask.message, options=OPTIONS):
        if isinstance(message, ResultMessage):
            result = message
    runs.append(summary(result))
    return {"reply": result.result}
```

That is the loop you have written before. `query()` hands back the
messages of the run as they happen, the route lets all but the last go
by, and the text of the result becomes the reply.

The route was already declared with `async def`, and that now matters.
A run takes seconds, and at each `await` inside it the server is free
to answer other requests. A server can be in the middle of many runs
at once.

The file was saved by that step, and uvicorn noticed: the terminal
says it detected a change and started the server again.

```{verify}
:id: agent-in-place
:label: The server restarted with the agent in the route
:substrate: script
:script: checks/agent_in_place.py
:trigger: after:replace-route
```

## Ask it something

The opening hours are in a file the model has never seen. Ask when
the shop closes on Saturday, and why then. This takes a few seconds,
and the page shows three dots until the whole reply is ready.

```{url-open}
:id: ask-saturday
:title: Ask when the shop closes on Saturday
:url: http://127.0.0.1:{{ server_port }}/?ask=When+does+the+shop+close+on+Saturday%2C+and+why+then%3F
:pane: chat
:label: Chat
:area: chat
```

The answer came out of `shop/opening-hours.md`. Between your message
and the reply, the agent ran its loop on the server: the model asked
for a file tool, the SDK ran it and sent back what it found, and the
model went on until it could answer. The page saw none of that. It
sent one request and got one response.

```{verify}
:id: agent-answered
:label: The agent read the shop's files and answered
:substrate: script
:script: checks/agent_answered.py
:timeout: 150s
:trigger: after:ask-saturday
```

```{hint}
:title: If the chat shows a status number in place of a reply
The route raised an error, and the terminal shows it. The most likely
cause is a run that could not reach the model. Go back to the welcome
page and run the login check again.
```
