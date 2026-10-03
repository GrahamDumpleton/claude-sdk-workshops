---
title: A way to stop
requires: [verify:stop-in-place, verify:page-marks-end, verify:run-ended, verify:server-stopped]
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

The page gets a Stop button beside Send. Pressing it posts the
conversation's id to the route, and notes that it did, for the end of
the run to read.

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
// Remember that this page asked for the stop, so the end of the run can say so.
let stopping = false;
document.getElementById("stop").onclick = () => {
  stopping = true;
  post("/stop", {conversation});
};


```

## Say where it ended

A run that is stopped ends where it was. The stream does not go quiet:
the SDK sends its result as it does for any run, and `events_for()`
turns it into the `done` event, whose `ended` says how. For a run that
finished it is `success`; for one that was interrupted it is
`error_during_execution`.

Without a word from the page, the chat would end on whatever was last:
a tool line still waiting for a result, or a sentence the model wrote
on its way to the next tool, either of which looks like more is
coming. So on a `done` that is not a success the page marks each line
still waiting as stopped, and adds a line saying that the run ended,
"Stopped" if this page asked for it, and otherwise how.

```{editor-replace}
:id: mark-ended
:title: Mark a run that did not finish
:path: page.html
:regex: true
:match: ^    \} else if \(event\.type === "done"\) \{\n      if \(!written\) reply\.remove\(\);$
    } else if (event.type === "done") {
      if (!written) reply.remove();
      if (event.ended !== "success") {
        // Mark each line still waiting for a result, and say where the run ended.
        for (const line of messages.querySelectorAll(".tool:not(.worked, .failed, .stopped)")) {
          line.classList.add("stopped");
          line.textContent += "\nstopped";
        }
        add("ended", stopping ? "Stopped" : "Ended: " + event.ended);
      }
      stopping = false;
```

```{verify}
:id: page-marks-end
:label: The page has a Stop button, and marks a run that did not finish
:substrate: contents
:trigger: after:mark-ended
contains page.html event.ended !== "success"
contains page.html stopping = true
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

The run ended where it was, and the last line in the chat says so.
Whatever had been written stays on the page above it. A tool line
still waiting for its result when the stop landed is dotted and says
so, though often there is none: a tool already running is let finish,
and it is the next request that is not made.
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
