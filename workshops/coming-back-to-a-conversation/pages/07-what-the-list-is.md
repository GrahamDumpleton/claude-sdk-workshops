---
title: What the list is
requires: [quiz:whose-list, verify:server-stopped]
---

# What the list is

The chat can now show its conversations, open any of them and branch
one. Look at how little the server had to learn: two short routes,
and neither keeps anything. The list is read from the SDK's
transcripts each time it is asked for. The server holds a client only
for a conversation that is being spoken to, and makes one on demand
for any id it is handed.

```{quiz}
:id: whose-list
question: A second member of staff opens the chat in another browser. Which conversations does the list show them?
options:
  - { text: "None, until they have had one of their own", explanation: "The list is not made from anything the browser holds. The server reads it from the transcripts." }
  - { text: "Every conversation the SDK has kept for the server's directory, whoever had it", correct: true }
  - { text: "Only the ones their browser's storage has ids for", explanation: "A browser stores one id, for the conversation it is showing. The list comes from the server." }
explanation: "The server lists every session it can find, and has no idea whose each one is. Nothing in this application knows who anybody is."
```

That is the piece a real application has to add. The shop's staff
sharing one list may be what a shop wants. An application with
separate people in it needs to record whose each conversation is, in
a database of its own beside the transcripts, list only a person's
own, and refuse an id that belongs to somebody else. The id in the
address is not a secret, and here anyone who has it can read and
carry on that conversation.

The SDK has more for looking after sessions than this workshop used:
`rename_session()` gives one a title of your choosing,
`tag_session()` labels it, and `delete_session()` removes its
transcript.

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
