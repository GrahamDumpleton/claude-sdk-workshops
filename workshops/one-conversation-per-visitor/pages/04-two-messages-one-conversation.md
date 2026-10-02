---
title: Two messages, one conversation
requires: [verify:first-turn, verify:second-turn]
---

# Two messages, one conversation

Try it. The first question starts a new conversation, with `new` in
the address, and asks when the shop opens on Saturday. The first
message of a conversation takes a moment longer than later ones,
because the server has a client to connect first.

```{url-open}
:id: ask-saturday
:title: Start a conversation and ask when the shop opens on Saturday
:url: http://127.0.0.1:{{ server_port }}/?new&ask=When+does+the+shop+open+on+Saturday%3F
:pane: chat
:label: Chat
:area: chat
```

```{verify}
:id: first-turn
:label: The server is holding a conversation, and it answered
:substrate: script
:script: checks/first_turn.py
:timeout: 150s
:trigger: after:ask-saturday
```

The second question means nothing on its own: "that day" is only a day
to someone who knows what was asked before.

```{url-open}
:id: ask-closing
:title: Ask when it closes that day
:url: http://127.0.0.1:{{ server_port }}/?ask=And+when+does+it+close+that+day%3F
:pane: chat
:label: Chat
:area: chat
```

The agent knew which day. The message went to the same client as the
first, into the session the first one opened, and the SDK sent the
model both exchanges. The check's message gives the session id of each
run: they are the same, and it is the id the page made up.

```{verify}
:id: second-turn
:label: Both messages ran in one session
:substrate: script
:script: checks/second_turn.py
:timeout: 150s
:trigger: after:ask-closing
```

Now look at the chat. It shows the second exchange and nothing of the
first. The step loaded the page afresh, and a page that has just
loaded has nothing on it.

So the two halves have changed places. In the first of these
workshops the page showed a conversation that the agent knew nothing
of. Here the agent remembers a conversation that the page has
forgotten.
