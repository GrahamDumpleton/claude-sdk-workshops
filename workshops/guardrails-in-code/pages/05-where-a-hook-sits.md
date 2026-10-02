---
title: Where a hook sits
---

# Where a hook sits

You now have three ways to control what an agent does to the world,
and they sit at different points between the model asking and the
tool running. The step below opens a picture of the order.

```{file-open}
:id: open-order
:title: Open the picture of what happens before a tool runs
:path: diagrams/before-a-tool-runs.md
:factory: Markdown Preview
```

| | Permission rules | The callback | A hook |
| --- | --- | --- | --- |
| Set with | `tools`, `allowed_tools`, `disallowed_tools`, `permission_mode` | `can_use_tool` | `hooks` |
| Is it your code | No, it is configuration | Yes | Yes |
| When it applies | Every call | Only a call the rules left undecided | Every call, before the rules |
| Good for | Saying what the agent has, and what needs no asking | Putting a person's decision in the loop | A rule that must hold, and a record of what happened |

The three are used together. The rules settle most calls cheaply. The
callback catches what is left and asks a person. Hooks hold the lines
that must not be crossed whoever approved what, and keep the log.

## Other moments a hook can be called

`PreToolUse` and `PostToolUse` are two events of several. In Python
the SDK can call a hook:

| Event | When |
| --- | --- |
| `PreToolUse` | A tool is about to run |
| `PostToolUse` | A tool has run |
| `PostToolUseFailure` | A tool was run and failed |
| `UserPromptSubmit` | A prompt has arrived, before the model sees it |
| `PermissionRequest` | A call needs someone's approval |
| `Stop` | The agent is about to finish |
| `SubagentStart`, `SubagentStop` | A subagent begins or ends, which the next workshop is about |
| `PreCompact` | A long conversation is about to be summarised |
| `Notification` | The agent has something to tell the person using it |

Each is given a dictionary describing the event and returns one saying
what should happen, in the way the two you wrote did.

## What a hook is not

A hook is ordinary code, and it enforces what it checks and nothing
more. The one in this workshop looks at the `file_path` of `Write` and
`Edit`. It would not stop an agent that had been given `Bash` from
writing a file with a shell command, because it never looks at shell
commands. A guardrail starts with giving the agent few tools, and a
hook covers the ones it has.
