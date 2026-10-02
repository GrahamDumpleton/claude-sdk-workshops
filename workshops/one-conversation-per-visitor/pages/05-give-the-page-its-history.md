---
title: Give the page its history back
requires: [verify:history-in-place, verify:history-served]
---

# Give the page its history back

A page that has just loaded needs to be told what was said before.
Something has to have kept that, and something already does.

The SDK writes every session to a file as it goes, called a
transcript: each message, each tool call and each result, in order.
The files are kept under your home directory, filed by the directory
the agent worked in. That record is what lets a session be picked up
again later, and it means the server need not keep a copy of the
conversation for itself. It can read the transcript.

## A route for what was said

`get_session_messages()` reads a transcript and returns its messages.
The route below takes a conversation id from the address, as in
`/history/` followed by the id, and returns what was said as a list of
who spoke and the text.

A transcript holds more than was said: tool requests and their results
are in it too. The route keeps the blocks of text and leaves the rest.
A message from the user is sometimes plain text and sometimes a list of
blocks, so it handles both.

```{editor-insert}
:id: import-messages
:title: Import the function that reads a transcript
:path: app.py
:match: get_session_info,
:position: after
:save: false
    get_session_messages,
```

```{editor-insert}
:id: add-history
:title: Add a route for what was said
:path: app.py
:match: @app.get("/status")
@app.get("/history/{conversation}")
def history(conversation: UUID):
    said = []
    for message in get_session_messages(str(conversation), directory=str(WORKSPACE)):
        content = message.message["content"]
        blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content
        for block in blocks:
            if block["type"] == "text":
                said.append({"role": message.type, "text": block["text"]})
    return said



```

This route reads a file and calls nothing, so it is declared with a
plain `def`. FastAPI runs such a function on a thread of its own, out
of the way of the routes that are streaming.

```{verify}
:id: history-in-place
:label: The server restarted with a route for what was said
:substrate: script
:script: checks/history_in_place.py
:trigger: after:add-history
```

## The page asks for it

The last lines of {open}`page.html` become a function that runs as the
page loads. It asks the server what has been said in this conversation
and shows it, and only then looks in the address for a question.

It also saves you a run. If the question in the address has already
been asked in this conversation, it is not asked again, so reloading
the page does not repeat it.

```{editor-replace}
:id: restore-history
:title: Show what was said when the page loads
:path: page.html
:regex: true
:match: ^// A question in the address[\s\S]*?^if \(asked\) send\(asked\)\.catch\(failed\);$
async function start() {
  // Show what has been said in this conversation so far.
  const said = await (await fetch("/history/" + conversation)).json();
  for (const item of said) add(item.role, item.text);

  // A question in the address, as in /?ask=When+do+we+open, is asked as the
  // page loads, unless this conversation has been asked it already.
  const asked = params.get("ask");
  if (asked && !said.some((item) => item.role === "user" && item.text === asked)) await send(asked);
}

start().catch(failed);
```

Load the page again, with nothing to ask.

```{url-open}
:id: reload-chat
:title: Load the chat again
:url: http://127.0.0.1:{{ server_port }}/
:pane: chat
:label: Chat
:area: chat
```

Both exchanges are back, and no model was called to put them there.
Look at what did it, because the server restarted a moment ago, when
`app.py` was saved. The client that held this conversation went with
the old server process. The page's id was in the browser, and what was
said was on disk, and those two were enough.

```{verify}
:id: history-served
:label: The server can say what was said in the conversation
:substrate: script
:script: checks/history_served.py
:trigger: after:reload-chat
```
