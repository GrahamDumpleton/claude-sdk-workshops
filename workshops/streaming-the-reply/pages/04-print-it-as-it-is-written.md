---
title: Print it as it is written
requires: [verify:text-streamed]
---

# Print it as it is written

The text is in the deltas. A `content_block_delta` event has a
`delta`, and when the delta's type is `text_delta` its `text` is the
next few characters of the reply. Printing each one as it arrives,
without starting a new line, writes the reply out as the model
produces it.

The cell does that. It also keeps each piece and the moment it
arrived, and keeps the text of the complete `AssistantMessage`, which
still comes. The next page uses them.

Watch this one while it runs.

```{cell-insert}
:id: insert-streamed
:path: {{ notebook }}
:tags: [streamed]
:run: true
pieces = []
times = []
final_text = ""
started = time.monotonic()

async for message in query(prompt=prompt, options=stream_options):
    if isinstance(message, StreamEvent):
        event = message.event
        if event["type"] == "content_block_delta" and event["delta"]["type"] == "text_delta":
            pieces.append(event["delta"]["text"])
            times.append(time.monotonic() - started)
            print(event["delta"]["text"], end="", flush=True)
    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                final_text += block.text

first_at = times[0]
last_at = times[-1]

print()
print()
print(f"first text after {first_at:.1f} seconds, last after {last_at:.1f}, in {len(pieces)} pieces")
```

The reply appeared a phrase at a time. The last line says when the
first piece and the last piece arrived.

The whole reply took about as long as it did when it arrived at once.
Streaming does not make a model faster. What changed is the wait for
the first sign of life, which is now a fraction of the total, and
that is the wait a person notices.

```{verify}
:id: text-streamed
:label: The text arrived in pieces, over time
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed streamed
len(pieces) > 1 and first_at < last_at
```

```{hint}
:title: Why the code checks two types
A delta is not always text. When the model asks for a tool, the input
it is writing for the tool streams as deltas of the type
`input_json_delta`, and thinking streams as deltas of its own type.
Checking for `text_delta` keeps only the words meant for the reader.
```
