---
title: What you know now
requires: [quiz:which-to-save]
---

# What you know now

A model writes a reply a piece at a time, and streaming lets your code
see the pieces as they are written.

- `include_partial_messages=True` adds `StreamEvent` messages to the
  stream. Each wraps one event from the service.

- A reply is a `message_start`, then for each block a
  `content_block_start`, many `content_block_delta` events and a
  `content_block_stop`, then a `message_delta` and a `message_stop`.

- The text is in the deltas of type `text_delta`. Print each as it
  arrives.

- The complete `AssistantMessage` and the `ResultMessage` still
  arrive. The pieces are for showing, and the complete message is for
  keeping.

Streaming does not shorten a reply. It shortens the wait before
something appears.

```{quiz}
:id: which-to-save
:title: Which to save
question: "A chat application streams each reply to the screen. Once a reply is finished, it saves the reply to a database. What should it save?"
options:
  - text: "The text of the complete `AssistantMessage`."
    correct: true
  - text: "Every `StreamEvent`, so that the reply can be played back."
    explanation: "That stores hundreds of fragments in place of one message, and the fragments say nothing the complete message does not."
  - text: "The pieces it printed, joined together by its own code."
    explanation: "That gives the right text for a reply that is only text, and the SDK has already done the joining. The complete message also has the blocks that are not text."
  - text: "Nothing. The reply can be streamed again later."
    explanation: "Asking again runs the model again, costs again, and gets a differently worded reply."
explanation: "Show the pieces and keep the complete message. The SDK assembles it for you, blocks and all."
```

## Where this goes next

Everything an agent has given you so far has been written for a
person to read. A program that calls an agent often wants something
else: values it can use, in a shape it knows. The last of these
workshops gets that.

**Get data back, not prose** is next.

Press Finish below to move on.
