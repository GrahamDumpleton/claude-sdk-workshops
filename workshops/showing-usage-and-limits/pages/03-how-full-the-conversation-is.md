---
title: How full the conversation is
requires: [verify:context-in-place, verify:context-shown]
---

# How full the conversation is

What a turn sent says what the turn cost. It does not say how much
room is left. A model can be sent only so much at once, an amount
called its context window, and a conversation fills it: every
message, every reply and every tool result stays in the conversation
and is sent again each time.

A connected client can say where a conversation stands.
`await client.get_context_usage()` reports what is in the context and
how full it is, as a percentage among other things. It answers from
what the SDK already knows, without calling the model.

## Ask after every turn

In `turn()`, when the `done` event is about to go to the page, the
server asks the client and adds the percentage to the event.

```{editor-insert}
:id: add-context
:title: Add how full the context is to the done event
:path: app.py
:match: self.note(event, message)
:save: false
                        if event["type"] == "done":
                            context = await self.client.get_context_usage()
                            event["context"] = round(context["percentage"], 1)
```

And keeps it with the run.

```{editor-insert}
:id: note-context
:title: Keep the figure with the run
:path: app.py
:match: sent=event["sent"],
:position: after
                    context=event["context"],
```

```{verify}
:id: context-in-place
:label: The server restarted, and reports how full the context is
:substrate: script
:script: checks/context_in_place.py
:trigger: after:note-context
```

The page adds it to its line.

```{editor-replace}
:id: show-context
:title: Show how full the context is
:path: page.html
:regex: true
:match: ^        `\$\{event\.seconds\}s, \$\{event\.sent\} tokens sent, \$\{event\.written\} written` \+\n        \(event\.ended === "success" \? "" : `, ended: \$\{event\.ended\}`\);$
        `${event.seconds}s, ${event.sent} tokens sent, ${event.written} written, ` +
        `context ${event.context}% full` + (event.ended === "success" ? "" : `, ended: ${event.ended}`);
```

## Ask again

A second question in the same conversation.

```{url-open}
:id: ask-knots
:title: Ask about another book
:url: http://127.0.0.1:{{ server_port }}/?ask=And+is+A+Field+Guide+to+Knots+in+stock%3F
:pane: chat
:label: Chat
:area: chat
```

The line now ends with how full the context is, and it is a small
number. A model's context window is large, and two questions about
books come nowhere near filling it.

```{verify}
:id: context-shown
:label: A turn was made, and how full its context is was reported
:substrate: script
:script: checks/context_shown.py
:timeout: 150s
:trigger: after:ask-knots
```

The figure only goes one way while a conversation lasts. It is the
one to watch in a chat that people leave open all day: a conversation
that has read a hundred files sends them all with every message. When
it nears the top, the SDK compacts the conversation on its own,
replacing the older part with a summary. A page that shows the figure
lets a person start a new conversation before it comes to that.
