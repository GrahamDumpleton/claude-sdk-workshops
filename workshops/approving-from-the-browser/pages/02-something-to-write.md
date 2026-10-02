---
title: Something to write
requires: [verify:write-in-place, verify:write-refused]
---

# Something to write

Start by giving the agent a job that changes something. The shop keeps
its notices as files in a directory called `notices`, and the staff
will ask the assistant to write them.

Two lines of the options in {open}`app.py` change.

The standing instruction gains a sentence saying where notices go.

```{editor-replace}
:id: prompt-notices
:title: Tell the agent where notices go
:path: app.py
:match: "are about to do."
:save: false
"are about to do. When you are asked for a notice, write it as a file in "
        "the notices directory."
```

And the agent gets the `Write` tool, with the permission mode named.
`permission_mode="default"` asks for the standard rules: reading
inside the working directory needs no approval, and a call that
changes something has to be approved by somebody.

```{editor-replace}
:id: add-write
:title: Give the agent the Write tool
:path: app.py
:match: tools=["Read", "Glob", "Grep"],
tools=["Read", "Glob", "Grep", "Write"],
    permission_mode="default",
```

```{verify}
:id: write-in-place
:label: The server restarted with an agent that has the Write tool
:substrate: script
:script: checks/write_in_place.py
:trigger: after:add-write
```

## Ask for a notice

Ask for a notice for the shop door, giving the opening hours.

```{url-open}
:id: ask-door
:title: Ask for a notice for the shop door
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Read+shop%2Fopening-hours.md+and+write+a+short+notice+for+the+shop+door+giving+the+opening+hours%2C+to+the+file+notices%2Fdoor.md.
:pane: chat
:label: Chat
:area: chat
```

The agent read the file, and that line turned solid. Then it asked for
`Write`, and that line turned red: the call failed. The agent says it
could not write the notice, or asks you for permission that you have
no way to give.

Nothing went wrong with the tool. The call needed approval, and the
server had nobody to ask, so the SDK refused it and told the model so
as the result of its request. The check confirms that the agent asked
and that no file was written.

```{verify}
:id: write-refused
:label: The agent asked to write, and nothing was written
:substrate: script
:script: checks/write_refused.py
:timeout: 150s
:trigger: after:ask-door
```

That refusal is the safe thing to happen, and it is no use to anyone.
The person who could say yes is looking at the chat. The server needs
a way to ask them.
