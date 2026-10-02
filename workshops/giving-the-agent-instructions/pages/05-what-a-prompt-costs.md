---
title: What a prompt costs
requires: [verify:preset-is-larger]
---

# What a prompt costs

Each of the three runs kept the size of the first request it sent to
the model: the system prompt, the description of the one tool, and the
customer's question, before anything had been read. The question and
the tool were the same each time, so the difference between the
numbers is the system prompt.

This cell calls nothing. It prints what the runs kept.

```{cell-insert}
:id: insert-sizes
:path: {{ notebook }}
:tags: [sizes]
:run: true
print("your own prompt    :", first_size, "tokens in the first request")
print("with one rule new  :", second_size)
print("the preset         :", third_size)

times_larger = round(third_size / first_size, 1)

print("the preset is", times_larger, "times the size of your own")
```

The first two are within a few tokens of each other, since one rule
was swapped for another. The preset is several times their size, and
nearly all of the extra is instructions for writing software, which an
agent that answers questions about returns never uses.

That size is paid on every request. An agent sends the system prompt
with each turn of each run, so a job of ten turns sends it ten times.

```{verify}
:id: preset-is-larger
:label: The preset made the request several times larger
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed sizes
if third_size <= 3 * first_size:
    print("The preset run was not several times larger. Run the three cells before this one again, in order.")
third_size > 3 * first_size
```

## What makes that affordable

Sending the same long text again and again is the case the cache
exists for. The service keeps the start of a request that it has seen
before, and input read back from the cache costs a fraction of what
fresh input does. The result of the preset run shows it at work.

```{cell-insert}
:id: insert-cache
:path: {{ notebook }}
:tags: [cache]
:run: true
usage = third.usage

print("fresh input          :", usage["input_tokens"])
print("written to the cache :", usage["cache_creation_input_tokens"])
print("read from the cache  :", usage["cache_read_input_tokens"])
```

Almost none of what the preset run sent was fresh input. On its first
request the long prompt was written to the cache, or read from it if
this cell's run was not the first in the last hour. On the next request
it was read back. Your own short prompt is below the size at which the
cache is used at all, which is one more way of saying it is small.

## Which to use

- **A prompt of your own**, for an agent with its own job. It says
  what this agent needs and nothing else, and it is small.

- **The preset, with `append`**, when the agent does what Claude Code
  does: works on code, in a project, with someone following along.
  The instructions it carries are then the ones the job needs.

- **Nothing at all** is the third choice. Leave `system_prompt` out
  and the SDK sends a minimal prompt that covers how to call tools and
  no more. The model is then given no idea whose assistant it is.
