---
title: A way to stop
requires: [verify:stop-in-place, verify:run-ended, verify:server-stopped]
---

# A way to stop

Approval is a say before something happens. The other control a
person wants is over a run that is already going: it has
misunderstood, or it is taking for ever, and they want it to stop.

A `ClaudeSDKClient` has a method for that. `await client.interrupt()`
stops the turn in progress. The run ends early with a result that says
so, and the conversation stays usable: the next message starts a new
turn in the same session.

## A route that interrupts

The page will say which conversation to stop, so the route takes the
conversation's id. If the server is holding that conversation, it
interrupts its client.

```{editor-insert}
:id: add-which
:title: Say what a request to stop looks like
:path: app.py
:match: class Answer(BaseModel):
:save: false
class Which(BaseModel):
    conversation: UUID



```

```{editor-insert}
:id: add-stop
:title: Add the route that interrupts a turn
:path: app.py
:match: @app.get("/history/{conversation}")
@app.post("/stop")
async def stop(which: Which):
    conversation = conversations.get(str(which.conversation))
    if conversation:
        await conversation.client.interrupt()
    return {"stopped": conversation is not None}



```

```{verify}
:id: stop-in-place
:label: The server restarted with a route that stops a turn
:substrate: script
:script: checks/stop_in_place.py
:trigger: after:add-stop
```

## A button for it

The page gets a Stop button beside Send, and one line that posts the
conversation's id to the route when it is pressed.

```{editor-insert}
:id: add-stop-button
:title: Add a Stop button to the page
:path: page.html
:match: <button>Send</button>
:position: after
  <button type="button" id="stop">Stop</button>
```

```{editor-insert}
:id: wire-stop-button
:title: Make the button call the route
:path: page.html
:match: async function start() {
document.getElementById("stop").onclick = () => post("/stop", {conversation});


```

## Stop a run

The request below gives the agent plenty to do: read every file in the
shop directory and write a paragraph about each. Once lines start
appearing in the chat, press **Stop**.

```{url-open}
:id: ask-everything
:title: Ask for a paragraph about every file
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Read+every+file+in+the+shop+directory+and+write+a+paragraph+about+each+one.
:pane: chat
:label: Chat
:area: chat
```

The run ended where it was. A tool line that was waiting for its
result stays dashed, and whatever had been written stays on the page.
The check's message says how the run ended: `error_during_execution`
is what an interrupted run reports, and `success` means it finished
before you pressed the button, in which case ask again and be quicker.

```{verify}
:id: run-ended
:label: The run ended, and the check says how
:substrate: script
:script: checks/run_ended.py
:timeout: 150s
:trigger: after:ask-everything
```

Type another message in the box. The conversation carries on: the
client that was interrupted is the one that answers.

## Stop the server

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
