---
title: Where the rules travel
requires: [verify:rules-measured]
---

# Where the rules travel

The rules were not added to your system prompt, and they were not put
in the request. This cell calls nothing. It shows where they went,
from what the two runs kept: the parts of the context before anything
was asked, and the size of the first request the model was sent,
counted in tokens. A token is a piece of text about the size of a
short word.

```{cell-insert}
:id: insert-measured
:path: {{ notebook }}
:tags: [measured]
:run: true
for name in ("System prompt", "Memory files"):
    without = plain["categories"].get(name, 0)
    with_rules = loaded["categories"].get(name, 0)
    print(f"{name:<14} without the rules {without:>5}   with them {with_rules:>5}")

print()
print("first request, without the rules :", plain["first_request"], "tokens")
print("first request, with the rules    :", loaded["first_request"], "tokens")
```

The system prompt is the same size in both runs. The rules are counted
separately, under memory files, which is the SDK's name for
instruction files, and the first request grew by about their length.

That is the cost, and it is paid on every request of every turn: the
file is not read once and remembered, because the model remembers
nothing. It is sent each time. So an instruction file wants to be
short and to hold only what the agent needs all the time.

## Why this outlasts a prompt

Being sent every time is also what the file is good for. In a long
conversation the older messages are eventually replaced by a summary,
to make room, and a rule you gave in your first message can be reworded
or dropped when that happens. The file is not part of the conversation.
It is read from disk and sent in full with every request, however long
the session has run.

| An instruction in | Is written by | Is sent | Holds through a long session |
| --- | --- | --- | --- |
| The prompt | Whoever makes the request | Once, as part of the conversation | Only until it is summarised |
| The system prompt | The program's author, in code | With every request | Yes |
| `CLAUDE.md` | Anyone who can edit the project | With every request | Yes |

The second and third rows differ in who owns them. The system prompt
belongs to your program. The file belongs to the project, and Claude
Code reads the same file when a person works in that directory, so one
set of rules serves the agent you write and the one you type to.

```{verify}
:id: rules-measured
:label: The rules were measured in the context
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed measured
(
    loaded["categories"].get("Memory files", 0) > plain["categories"].get("Memory files", 0)
    and loaded["first_request"] > plain["first_request"]
)
```
