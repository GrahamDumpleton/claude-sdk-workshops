---
title: What you have built
requires: [verify:server-stopped]
---

# What you have built

That is the application finished, as far as these workshops take it.
Open {open}`app.py` and read it from the top once more. It is under
three hundred lines, and every part of it was added for a reason you
have seen.

| The part | What it is for |
| --- | --- |
| `OPTIONS` | What the agent is: its model, instructions, tools, skill and limits |
| `events_for()` | What the page is told about each message of a run |
| `Conversation` | A connected client for one conversation, its turns kept in order |
| `approve()` | The question put to the person in the chat before a notice is written |
| The `chat` route | A turn started, and its events streamed to the page |
| The other routes | An answer to a question, a stop, a choice of model, what was said, the list, a branch |

Very little of it is about the model. The SDK runs the agent loop,
keeps the session and writes the transcript. The application's work
is the part around that: getting messages in and events out, deciding
what each person may see and do, and keeping hold of what is live.

## What is left for an application of your own

These workshops ran everything on your machine, for you. An
application for other people needs more, and none of it is special
to agents.

- **Knowing who is there.** Nothing here knows who anybody is. Anyone
  who can reach the server can read any conversation, answer any
  question and choose any model. An application for several people
  puts a login in front of all of it, and records whose each
  conversation is.

- **A key, not a login.** The agent ran on your own Claude login,
  which is for your own use. An application that other people use
  authenticates with an API key from the Claude Console, and its
  usage is billed to that key.

- **Somewhere to run.** Each conversation is a process, and its
  transcript is a file on one machine. The SDK's documentation on
  hosting covers how many a machine can hold, and how to keep
  transcripts where more than one server can reach them.

- **A box around the agent.** The agent here can read every file
  below the server's directory. One that can run commands or fetch
  from the web needs to be shut in, and the documentation on secure
  deployment says how.

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
