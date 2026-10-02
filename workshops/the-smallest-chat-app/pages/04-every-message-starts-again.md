---
title: Every message starts again
requires: [quiz:follow-up, verify:two-sessions]
---

# Every message starts again

The chat looks like a conversation: your message, the reply, a box for
the next message. Before you send a second one, think about what the
server will do with it. The route is the same function, and it calls
`query()` again.

```{quiz}
:id: follow-up
question: The next message asks "What did I just ask you?". What does the agent have to go on when it answers?
options:
  - { text: "Both messages, because the server has kept the conversation", explanation: "The server keeps a summary of each run in `runs`, and never sends it to the agent." }
  - { text: "Only the new message, because each call to `query()` starts a new session", correct: true }
  - { text: "Both messages, because the model remembers what it was asked a moment ago", explanation: "A model keeps nothing between requests. It knows only what it is sent." }
explanation: "`query()` runs one exchange in a session of its own and ends. The second call was never sent what was said in the first."
```

Now send it.

```{url-open}
:id: ask-again
:title: Ask what you just asked
:url: http://127.0.0.1:{{ server_port }}/?ask=What+did+I+just+ask+you%3F
:pane: chat
:label: Chat
:area: chat
```

The agent has nothing to tell you. It is not being unhelpful: this is
the first message it has seen.

The check below reads what the server kept of the two runs, and its
message gives the session each ran in. They are different. A session
is the SDK's record of one conversation, and this application starts a
new one for every message.

```{verify}
:id: two-sessions
:label: The two messages ran in two sessions
:substrate: script
:script: checks/two_sessions.py
:timeout: 150s
:trigger: after:ask-again
```

The page made it look otherwise for a moment, because the step loaded
it afresh and the first exchange went from the screen. Had you typed
the second question in the box, both exchanges would be on the page,
one above the other, and the agent would still have known only the
second. What the page shows and what the agent is sent are separate
things, and so far nothing connects them.
