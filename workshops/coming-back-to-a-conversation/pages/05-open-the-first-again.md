---
title: Open the first again
requires: [verify:first-resumed]
---

# Open the first again

Opening a conversation from the list takes nothing but its id, so a
step on this page can do what a click in the list does. The first
conversation's id is the one chosen on the welcome page.

Open it by that id, and ask something that can only be answered from
what was said before.

```{url-open}
:id: ask-first-again
:title: Open the first conversation and ask what was said
:url: http://127.0.0.1:{{ server_port }}/?c={{ first_conversation }}&ask=What+was+the+first+thing+I+asked+you+in+this+conversation%3F
:pane: chat
:label: Chat
:area: chat
```

The first exchange came back on the page, from the transcript, and
then the agent answered from it.

The server was not holding that conversation. It restarted two pages
ago, when the route for the list was added, and the first conversation
had not been spoken to since. So `conversation_for()` made a
`Conversation` for the id, found that the SDK had a transcript under
it, and connected the client with `resume`. Coming back to an old
conversation and carrying on after a restart are the same thing to
the server: an id it is not holding, with a transcript behind it.

```{verify}
:id: first-resumed
:label: The first conversation was opened by its id, and answered
:substrate: script
:script: checks/first_resumed.py
:timeout: 150s
:trigger: after:ask-first-again
```

```{hint}
:title: What picking up an old conversation costs
The whole of the conversation so far is sent to the model with the
new message, as it is on every turn. A conversation resumed after a
week costs what its next turn would have cost at the time. What is
lost is the cache: for a few minutes after a request, a request that
begins the same way is charged less for the part that repeats, and a
conversation that has been left for longer starts again at the full
price.
```
