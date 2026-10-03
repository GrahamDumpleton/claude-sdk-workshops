---
title: Tell the page about tools
requires: [verify:tools-in-place]
---

# Tell the page about tools

Two kinds of message carry the work of a run, and you have met both.

- When the model wants a tool, its reply holds a `ToolUseBlock`,
  inside an `AssistantMessage`. The block has the tool's `name`, the
  `input` the model wants to pass it, and an `id`. `events_for()`
  already looks for it, to send the page the bare `tool` event.

- When the SDK has run the tool, the result goes back to the model as
  a `ToolResultBlock`, inside a `UserMessage`, since it is sent to the
  model in the user's place. The block has the `tool_use_id` of the
  request it answers, and says whether the tool failed.

The server needs the names of the second pair.

```{editor-replace}
:id: import-blocks
:title: Import the result's message and block types
:path: app.py
:regex: true
:match: ^    StreamEvent,\n    ToolUseBlock,$
:save: false
    StreamEvent,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
```

## Fill out one event, and add another

The `tool` event gains the name, the input and the id of the request.
A result becomes a new event, `tool_result`, with the id of the
request it belongs to, whether it failed, and how big it was.

The result itself is not sent. It can be a whole file, the person in
the chat did not ask to see it, and its size says enough about what
the agent now has to work with.

```{editor-replace}
:id: fill-tool-event
:title: Say which tool was asked for
:path: app.py
:match: yield {"type": "tool"}
:save: false
yield {"type": "tool", "id": block.id, "name": block.name, "input": block.input}
```

```{editor-insert}
:id: add-result-event
:title: Send the page an event for each result
:path: app.py
:match: elif isinstance(message, ResultMessage):
:save: false
    elif isinstance(message, UserMessage) and isinstance(message.content, list):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                yield {
                    "type": "tool_result",
                    "id": block.tool_use_id,
                    "error": bool(block.is_error),
                    "size": len(str(block.content)),
                }
```

That is all the route needs. It already sends the page whatever
`events_for()` yields, so two new kinds of event travel down the
stream that was built for text.

## Keep the names of the tools

One more change, for the record the server keeps. Each turn starts a
list of the tools it called, `note()` adds to it as the `tool` events
go by, and the list goes into the run's entry in `/status`.

```{editor-insert}
:id: start-calls
:title: Start each turn with an empty list of calls
:path: app.py
:match: try:
:save: false
            self.calls = []
```

```{editor-replace}
:id: note-calls
:title: Keep the name of each tool a turn calls
:path: app.py
:regex: true
:match: ^        if event\["type"\] == "done":\n            runs\.append\(summary\(message, resumed=self\.resumed\)\)$
        if event["type"] == "tool":
            self.calls.append(event["name"])
        elif event["type"] == "done":
            runs.append(summary(message, resumed=self.resumed, calls=self.calls))
```

```{verify}
:id: tools-in-place
:label: The server restarted, and sends events for tool requests and results
:substrate: script
:script: checks/tools_in_place.py
:trigger: after:note-calls
```

The server is now sending an event the page does not know, and
fields on one it does. Nothing breaks: `send()` in {open}`page.html`
acts on the events it knows, uses the fields it knows, and passes over
the rest. A page and a server can be changed one at a time when
unknown events are ignored.
