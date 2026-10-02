---
title: Let a mode decide
requires: [verify:mode-approved]
---

# Let a mode decide

Approving tools one by one is exact, and for an agent with many tools
it is a long list. A permission mode approves a whole kind of action
at once. `acceptEdits` approves changes to files, by whichever tool
makes them.

The third attempt names no tool. It only changes the mode.

```{cell-insert}
:id: insert-third
:path: {{ notebook }}
:tags: [third]
:run: true
third = await attempt(permission_mode="acceptEdits")

report(third)
```

The notice was written again, and this time the options never
mentioned `Write`. The mode approved the call because of what it did,
not which tool it was.

```{verify}
:id: mode-approved
:label: The mode approved the write
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed third
if not third["written"]:
    print("The notice was not written. Run the cell again.")
third["written"] and third["mode"] == "acceptEdits" and third["denied"] == []
```

## The modes

Each mode is an answer to one question: how much may the agent do
without anyone being asked?

| Mode | What runs without asking |
| --- | --- |
| `default` | Only calls that need no approval, such as reading in the working directory, and calls an allow rule covers. Anything else is put to your program, and refused if it gave no way to ask. |
| `dontAsk` | The same calls. Anything else is refused outright, and nobody is asked. |
| `acceptEdits` | All of that, and changes to files. |
| `plan` | Looking and planning. A change to a file is never approved without asking. |
| `auto` | Whatever a separate model, which reviews actions such as commands, decides to let through. |
| `bypassPermissions` | Everything. |

Set the mode yourself. When the option is left out, the mode a session
starts in is decided by settings and defaults that are not the same
everywhere, which is why the first attempt named `default` and did not
rely on it.

The last row is there for completeness. `bypassPermissions` is for an
agent sealed inside a container or a machine with nothing on it that
matters, and for nowhere else. No workshop here uses it.
