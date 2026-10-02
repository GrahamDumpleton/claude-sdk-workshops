---
title: What it used
requires: [verify:usage-read]
---

# What it used

A model reads and writes in tokens. A token is a piece of text about
the size of a short word, and it is the unit everything about a model
is measured in: how much it can be sent, how much it wrote, and how
much of your plan a run used.

The result's `usage` is a dictionary of token counts for the whole
run. Four of them matter.

```{cell-insert}
:id: insert-usage
:path: {{ notebook }}
:tags: [usage]
:run: true
usage = result.usage

print("input tokens          :", usage["input_tokens"])
print("output tokens         :", usage["output_tokens"])
print("written to the cache  :", usage["cache_creation_input_tokens"])
print("read from the cache   :", usage["cache_read_input_tokens"])

tokens_in = (
    usage["input_tokens"]
    + usage["cache_creation_input_tokens"]
    + usage["cache_read_input_tokens"]
)

print("everything sent       :", tokens_in)
```

- **Input tokens** are what the model was sent. The count is the total
  over every request of the run, and each request carries the whole
  conversation so far, so the question was counted once for every turn.
  That is why input is much the larger number.

- **Output tokens** are what the model wrote: its requests for tools
  and its answer.

## The cache

Most of each request repeats the one before it. The service can keep
the part that repeats ready to use again, and that store is the cache.
Input written to the cache is being stored for the first time. Input
read from the cache was already there, and costs a fraction of what
fresh input does.

The three input counts do not overlap. Added together they are
everything the model was sent, which is the last line the cell printed.

A request has to be a few thousand tokens long before the cache is
used, and these requests are smaller than that, so both cache counts
are probably zero here. In a long conversation, or under long
instructions, most of the input is read from the cache. Later
workshops show both.

```{verify}
:id: usage-read
:label: The result reports the four token counts
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed usage
tokens_in > 0 and usage["output_tokens"] > 0
```
