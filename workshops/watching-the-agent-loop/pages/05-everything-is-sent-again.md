---
title: Everything is sent again
requires: [verify:requests-grow]
---

# Everything is sent again

The model keeps nothing between one request and the next. It does not
remember the question, what it asked for, or what came back. So each
time the SDK asks the model what comes next, it sends the whole
conversation so far: the instructions, the question, every request the
model made and every result.

That can be measured. A model reads and writes in tokens, pieces of
text about the size of a short word, and each of the model's replies
reports how many tokens it was sent. The cell prints that count for
each reply in the run.

Two details of the code:

- The SDK delivers one reply from the model as an `AssistantMessage`
  for each block in it, so some text followed by a request arrives as
  two messages. They share a `message_id`, and the cell uses that to
  count each reply once.

- The count of what was sent is in three parts, which the cell adds
  together. The next workshop says what the parts are.

```{cell-insert}
:id: insert-sizes
:path: {{ notebook }}
:tags: [sizes]
:run: true
replies = {}

for message in messages:
    if isinstance(message, AssistantMessage):
        usage = message.usage or {}
        sent = (
            usage.get("input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0)
        )
        reply = replies.setdefault(message.message_id, {"sent": sent, "blocks": []})
        reply["blocks"].extend(type(block).__name__ for block in message.content)

sizes = [reply["sent"] for reply in replies.values()]

for number, reply in enumerate(replies.values(), start=1):
    print("reply", number, "was sent", reply["sent"], "tokens and held", ", ".join(reply["blocks"]))
```

The number goes up with every reply. Nothing was sent twice by
mistake: the second request is the first one again with the model's
own request and its result added on the end, and the third is the
second with more added.

Two things follow from this, and both come back in later workshops:

- A long run costs more than its steps added up, because every step
  pays again for all the steps before it.

- Whatever a tool returns stays in the conversation for the rest of
  the run. A tool that returns a large file makes every later request
  that much larger.

```{verify}
:id: requests-grow
:label: Each request was larger than the first
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed sizes
if len(sizes) < 2:
    print("The run had only one reply from the model. Run the cell on the second page again, then this one.")
len(sizes) >= 2 and sizes[-1] > sizes[0]
```
