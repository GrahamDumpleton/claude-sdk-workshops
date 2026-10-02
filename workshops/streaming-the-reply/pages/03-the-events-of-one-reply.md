---
title: The events of one reply
requires: [verify:events-counted]
---

# The events of one reply

The service that runs the model can report a reply as it is produced,
as a series of small events. By default the SDK gathers them up and
hands your code the finished message. One option changes that:
`include_partial_messages=True` passes each event on as well, wrapped
in a message of the type `StreamEvent`.

A `StreamEvent` has an `event`, a dictionary, and the dictionary has a
`type` saying what kind of event it is. Before printing any text, see
what kinds there are. The cell copies the options with the one field
added, asks the same thing again, and counts the events of each type
in the order they first appear.

```{cell-insert}
:id: insert-events
:path: {{ notebook }}
:tags: [events]
:run: true
stream_options = replace(options, include_partial_messages=True)

kinds = {}

async for message in query(prompt=prompt, options=stream_options):
    if isinstance(message, StreamEvent):
        kind = message.event["type"]
        kinds[kind] = kinds.get(kind, 0) + 1

for kind, count in kinds.items():
    print(f"{count:>4}  {kind}")
```

One reply is made of six kinds of event, and they nest:

- `message_start` opens the reply.

- `content_block_start` opens a block inside it. This reply has one
  block, of text.

- `content_block_delta` carries the next piece of that block. There
  are many of these, because the text arrives a few words at a time.
  Delta is the usual word for a change, here an addition.

- `content_block_stop` closes the block.

- `message_delta` carries what is only known at the end, such as why
  the model stopped and how many tokens it wrote.

- `message_stop` closes the reply.

A reply with two blocks, some text and then a request for a tool,
would have a start, its deltas and a stop for each block, inside one
message.

```{verify}
:id: events-counted
:label: The run produced stream events, most of them deltas
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed events
if not kinds:
    print("No stream events arrived. Check that the cell sets include_partial_messages=True, and run it again.")
"message_start" in kinds and kinds.get("content_block_delta", 0) > 1
```
