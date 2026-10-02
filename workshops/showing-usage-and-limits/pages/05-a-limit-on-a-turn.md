---
title: A limit on a turn
requires: [verify:limit-in-place, verify:limit-reached, verify:limit-restored]
---

# A limit on a turn

One message can set off a great deal of work. An agent goes round its
loop for as long as the model keeps asking for tools, and a question
that sends it reading through everything it can reach will run, and
be paid for, until it is done.

`max_turns` is the option that bounds it. The options have had it all
along, set to ten, well above what any question here needs. To see
what happens when a run reaches the limit, turn it down to two.

```{editor-replace}
:id: lower-limit
:title: Lower the limit to two turns
:path: app.py
:match: max_turns=10,
max_turns=2,
```

```{verify}
:id: limit-in-place
:label: The server restarted with a limit of two turns
:substrate: script
:script: checks/limit_in_place.py
:trigger: after:lower-limit
```

Now ask for something that takes several steps: a fact from each of
the shop's four documents.

```{url-open}
:id: ask-four-documents
:title: Ask for a fact from each of the shop's documents
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Read+each+of+the+four+documents+in+the+shop+directory%2C+one+at+a+time%2C+and+give+one+fact+from+each.
:pane: chat
:label: Chat
:area: chat
```

The agent started on the job, and the run was ended before it could
answer. The line under the conversation says so:
`ended: error_max_turns`. That text is the `subtype` of the result,
which the server has been passing to the page in the `done` event
since the second of these workshops. Until now it was always
`success`.

```{verify}
:id: limit-reached
:label: The run was ended by the limit
:substrate: script
:script: checks/limit_reached.py
:timeout: 150s
:trigger: after:ask-four-documents
```

Notice what did not happen. Nothing raised an error on the server,
and the conversation is not broken. A turn that reaches the limit
ends with a result like any other, and the next message starts a new
turn with the count at nothing. The limit is on each turn, not on the
conversation.

## Put it back

Two is too low for an assistant that reads files. Put the limit back.

```{editor-replace}
:id: restore-limit
:title: Put the limit back to ten turns
:path: app.py
:match: max_turns=2,
max_turns=10,
```

```{verify}
:id: limit-restored
:label: The server restarted with the limit back at ten
:substrate: script
:script: checks/limit_restored.py
:trigger: after:restore-limit
```

## The other limits

A turn limit is one of several, and the application already has some
of the others.

| What is limited | Where |
| --- | --- |
| The steps one message can take | `max_turns`, in the options |
| What one message can cost | `max_budget_usd`, in the options, which ends a run with `error_max_budget_usd` |
| How long a question to the page can wait | `APPROVAL_SECONDS`, in `app.py` |
| Which models can be chosen | `MODELS`, in `app.py` |
| What the agent can do at all | `tools`, `allowed_tools` and the callback |

One it does not have is a limit on the conversations it holds. Each
is a process on the server, and this server keeps every one until it
stops. An application left running closes a conversation that has
been quiet for a while, and lets `conversation_for()` connect it
again from its transcript if its visitor comes back.
