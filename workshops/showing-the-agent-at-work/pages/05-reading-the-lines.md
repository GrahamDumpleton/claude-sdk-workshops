---
title: Reading the lines
requires: [quiz:what-returned-counts, verify:server-stopped]
---

# Reading the lines

The lines in the chat are the agent loop, drawn. Read down them once
more with the loop in mind.

- **A request.** Each dashed line appeared when the model's reply
  asked for a tool. What follows the tool's name is the input the
  model chose: a pattern to search for, or the path of a file.

- **A result.** The line turned solid when the SDK had run the tool
  and sent the result back to the model.

- **Several at once.** Where two lines appeared together, the model
  asked for both in one reply. Tools that only read are run side by
  side, so their results come back in any order, and the id is what
  ties each result to its line.

- **Words in between.** Anything the model wrote before it had
  finished looking has a bubble of its own now, above the lines that
  came after it.

```{quiz}
:id: what-returned-counts
question: A line in the chat ends "returned 388 characters". Where are those characters now?
options:
  - { text: "In the page, hidden until the line is clicked", explanation: "The server sent the page the size of the result and nothing of the result itself." }
  - { text: "In the conversation, where they are sent to the model with every later request", correct: true }
  - { text: "Nowhere: a result is thrown away once the model has read it", explanation: "A model reads nothing once and for all. It is sent the whole conversation each time, results included." }
explanation: "A tool result becomes part of the conversation. That is how the model comes to know what was in the file, and it is why a long session of reading costs more with every message."
```

What the page shows is a choice, and this is one of several. The name
and input of each tool suits people who want to know what the agent is
up to, such as the staff of a shop. A page for the public might say
"Looking that up" and no more. Either way the choice is made in two
places you now know: what `events_for()` sends, and what `send()`
draws.

A request that fails is drawn in red. Nothing failed here, because
reading a file that exists does not. The next workshop gives the
agent a tool that can be refused.

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
