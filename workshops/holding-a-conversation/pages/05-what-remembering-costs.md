---
title: What remembering costs
requires: [verify:second-turn-larger, verify:window-read]
---

# What remembering costs

If every turn sends the whole conversation, every turn is larger than
the one before. The results of the two turns say by how much. A model
reads and writes in tokens, pieces of text about the size of a short
word, and each result counts the tokens its turn was sent, in three
parts that the cell adds together.

This cell calls nothing. It reads the two results you have.

```{cell-insert}
:id: insert-sizes
:path: {{ notebook }}
:tags: [sizes]
:run: true
def tokens_sent(result):
    usage = result.usage
    return (
        usage["input_tokens"]
        + usage["cache_creation_input_tokens"]
        + usage["cache_read_input_tokens"]
    )


first_size = tokens_sent(turn_one)
second_size = tokens_sent(turn_two)

print("turn one was sent :", first_size, "tokens")
print("turn two was sent :", second_size, "tokens")
print("the difference    :", second_size - first_size)
```

The second turn was sent everything the first was, and then the first
reply and the second question. Two short turns add little. The rule
they show is what matters: a conversation of fifty turns sends the
first turn fifty times, and a long file read on turn three is sent
again on every turn after it.

```{verify}
:id: second-turn-larger
:label: The second turn was sent more than the first
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed sizes
second_size > first_size
```

## The context window

There is a limit to how much a model can be sent at once, called its
context window. Everything has to fit in it together: the system
prompt, the descriptions of the tools, and the whole conversation.

A connected client can report how full the window is. Asking is not a
call to the model.

```{cell-insert}
:id: insert-window
:path: {{ notebook }}
:tags: [window]
:run: true
context = await client.get_context_usage()

for category in context["categories"]:
    print(f"{category['name']:<16}{category['tokens']:>8}")

window_used = context["totalTokens"]
window_size = context["maxTokens"]

print()
print("in the window :", window_used)
print("it can hold   :", window_size)
```

The lines at the top divide the window by what is in it: the system
prompt, the messages of the conversation, and the free space left,
which here is nearly all of it. You may see a line for memory files as
well. Claude Code keeps notes of its own about a project it has been
used in, and a session started inside that project is sent the list of
them.

A short conversation with no tools barely touches the window. An agent
that reads files for an hour fills it, since every tool result stays
in the conversation. When the window is nearly full, the SDK makes
room by replacing the older part of the conversation with a summary.
**Extending an agent with the Claude Agent SDK**, the set of workshops
after these, has one on keeping a long session small.

```{verify}
:id: window-read
:label: The client reported how full the context window is
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed window
0 < window_used < window_size
```
