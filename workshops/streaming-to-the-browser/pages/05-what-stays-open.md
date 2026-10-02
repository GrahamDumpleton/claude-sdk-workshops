---
title: What stays open
requires: [quiz:held-open, verify:server-stopped]
---

# What stays open

The reply now appears as it is written. Before you leave it, look at
what changed about the exchange between the page and the server,
because the rest of these workshops build on it.

```{file-open}
:id: open-diagram
:title: Open a diagram of a streamed reply
:path: diagrams/a-streamed-reply.md
:factory: Markdown Preview
:area: code
```

Before, a message was one request and one short response at the end.
Now the response begins as soon as the route yields its first event
and stays open until the function finishes. For the whole of that time
the server is holding two things for that one page: a connection to
the browser, and a run of the agent.

- **Many at once.** Each page that is waiting for a reply has a route
  of its own in progress. They do not block one another, because the
  route is `async` and gives way at every `await`.

- **Quiet stretches.** While the agent reads a file there is nothing
  to send. FastAPI fills a long silence with a comment line, `: ping`,
  every fifteen seconds, so that nothing between the server and the
  browser decides the connection is dead. The page's reader ignores
  any line that does not begin `data:`.

- **An end.** A stream has no length in advance, so the page needs to
  be told when the reply is over. That is what the `done` event is
  for, and the connection closes after it.

```{quiz}
:id: held-open
question: A member of staff asks a question and closes the browser tab while the reply is still being written. What is true of this application as it stands?
options:
  - { text: "The reply is finished and kept, and shown when they come back", explanation: "Nothing in the server keeps a reply. The run belongs to the request that started it." }
  - { text: "The route stops where it is, and the run it was reading goes with it", correct: true }
  - { text: "The server carries on sending events to a page that is no longer there", explanation: "The server is told the connection has closed, and stops the route." }
explanation: "The run lives inside the route, and the route lives as long as its request. The next workshop moves the conversation out of the request, so that it can outlast one."
```

One event type carries text. The same stream can carry anything else
the page should know while a run is going on: that a tool was called,
that the agent is waiting for permission, how much the run cost. Later
workshops add those as new values of `type`, and the reader in the
page will not need to change again.

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
