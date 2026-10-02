---
title: What the agent has
requires: [verify:tool-list-in-place, verify:tools-listed]
---

# What the agent has

Before adding tools, make it possible to see them. A person using the
chat has no way to know what the assistant can do, and you are about
to change that three times.

The server is already told. Every run opens with a `SystemMessage` of
the subtype `init`, in which the SDK says what the session was given:
the model, the working directory and the names of its tools. The
server lets that message go by, as it once did the tool requests.

## An event for it

`events_for()` in {open}`app.py` gains a branch for the `init` message,
which becomes a `tools` event with the names and the model.

```{editor-insert}
:id: import-system-message
:title: Import SystemMessage
:path: app.py
:match: ToolResultBlock,
:save: false
    SystemMessage,
```

```{editor-insert}
:id: add-tools-event
:title: Tell the page what the session was given
:path: app.py
:match: elif isinstance(message, AssistantMessage):
    elif isinstance(message, SystemMessage) and message.subtype == "init":
        yield {"type": "tools", "names": message.data["tools"], "model": message.data["model"]}
```

## A line in the page

{open}`page.html` gets a line under its heading, and `send()` fills it
in when the event arrives.

```{editor-insert}
:id: add-tools-line
:title: Add a line for the tools under the heading
:path: page.html
:match: <main id="messages"></main>
<p id="tools"></p>
```

```{editor-insert}
:id: fill-tools-line
:title: Fill the line in when the event arrives
:path: page.html
:match: } else if (event.type === "tool") {
    } else if (event.type === "tools") {
      document.getElementById("tools").textContent = event.model + " with " + event.names.join(", ");
```

```{verify}
:id: tool-list-in-place
:label: The server restarted, and tells the page what the agent has
:substrate: script
:script: checks/tool_list_in_place.py
:trigger: after:fill-tools-line
```

## Ask something

Any question will do, since every run opens with the `init` message.
Ask when story time is.

```{url-open}
:id: ask-story-time
:title: Ask when story time is
:url: http://127.0.0.1:{{ server_port }}/?new&ask=When+is+story+time%3F
:pane: chat
:label: Chat
:area: chat
```

The line under the heading names the model and four tools: the three
that find and read files, and `Write`. That is the list in the
`tools` option, in the SDK's own order.

```{verify}
:id: tools-listed
:label: A run was made, and the page was told what it had
:substrate: script
:script: checks/tools_listed.py
:timeout: 150s
:trigger: after:ask-story-time
```
