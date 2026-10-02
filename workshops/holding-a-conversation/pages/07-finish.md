---
title: What you know now
requires: [quiz:where-the-memory-is]
---

# What you know now

A model remembers nothing. A conversation is made by keeping what was
said and sending all of it again with each new message.

- Each call to `query()` is a session of its own. A second call knows
  nothing of the first.

- A `ClaudeSDKClient` keeps one session open. `client.query()` sends a
  prompt, `client.receive_response()` reads the reply, and each turn is
  answered with the whole conversation in front of the model.

- Every turn is sent more than the one before, because it carries all
  the turns before it.

- The context window is the most a model can be sent at once.
  `get_context_usage()` says how full it is.

```{quiz}
:id: where-the-memory-is
:title: Where the memory is
question: "On the second turn, the agent gave back the stock code it had been told on the first. Where was the code kept between the two turns?"
options:
  - text: "In the model, which learned it during the first turn."
    explanation: "A model is not changed by being used. It was the same before and after the first turn, and knew nothing of it."
  - text: "In the session the client held open, which sent the first turn to the model again along with the second."
    correct: true
  - text: "In a file the agent wrote on the first turn and read on the second."
    explanation: "The agent had no tools. It could not write or read anything."
  - text: "In the notebook, in the variable `tell`."
    explanation: "The variable held the text of the first prompt, and it was sent only once, on the first turn. The second cell sent only the question."
explanation: "The memory is the conversation itself, kept by the session and sent to the model in full on every turn."
```

## Where this goes next

The conversation you held ended when the client was disconnected, and
would have ended the same way if the kernel had stopped. The next
workshop is about getting one back: where the SDK keeps a session
after the program has gone, how to resume it, and how to branch it and
try two ways forward.

**Pick up where you left off** is next.

Press Finish below to move on.
