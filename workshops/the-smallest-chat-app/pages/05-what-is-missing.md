---
title: What is missing
requires: [verify:server-stopped]
---

# What is missing

The application works: a question typed into a web page is answered
from the shop's files by an agent. It is also the least a chat
application can be, and each thing it lacks is a workshop of its own.

| What it lacks | What you saw | Where it is added |
| --- | --- | --- |
| Words as they are written | Three dots until the whole reply is ready | **Stream the reply to the browser** |
| Memory | A second message that knew nothing of the first | **Keep a conversation for each visitor** |
| Any sign of work | No way to tell reading files from being stuck | **Show the agent at work** |
| A way to say no | An agent that can only read, because nobody could be asked about anything more | **Approve from the browser** |

One more thing is worth knowing now. Every call to `query()` starts a
copy of Claude Code as a separate process, runs the exchange and shuts
it down. That is simple and it wastes nothing between messages. It
also means each message pays for starting the process, and nothing
carries over. A conversation needs something that stays running, and
the third workshop changes the server to keep it.

## Stop the server

The server is still running in the terminal. The step below sends it
the same interrupt as pressing Control and C there.

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
