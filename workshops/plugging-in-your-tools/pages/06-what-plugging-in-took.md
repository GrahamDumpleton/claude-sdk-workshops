---
title: What plugging in took
requires: [verify:server-stopped]
---

# What plugging in took

Three things were added to the assistant, and almost all of the work
was in the options.

| | What was shipped | What the options needed |
| --- | --- | --- |
| The stock list | A function with `@tool`, in a server | `mcp_servers`, and its name in `allowed_tools` |
| The orders | A second function in the same server | Its name in `allowed_tools` |
| The refund reply | A directory with a `SKILL.md`, copied into `.claude/skills` | `"Skill"` in `tools`, `setting_sources`, and its name in `skills` |

The application around the agent did not change for any of them. The
route, the conversations, the stream of events and the page's drawing
of tool lines were written for tools in general, so a new tool shows
up in the chat the moment the agent has it. The one addition, the line
that lists the tools, was there to let you watch.

That division is worth keeping in an application of your own. What the
agent can do is decided in its options and in the tools behind them.
The web application carries messages and events, and should not need
to know what any tool is for.

Two limits were set on the way, and both were set in code and not in
the instructions. The orders cannot be changed, because the database
is opened read-only. And the two tools run without asking, because
they are named in `allowed_tools`, while a tool that is not named is
put to the callback, which refuses it. Had the orders tool been able
to write, the place to stop it would have been one of those two, and
never a sentence asking the model to be careful.

## Stop the server

```{interrupt}
:id: stop-server
:title: Stop the server
:session: server
```

```{verify}
:id: server-stopped
:label: The server has stopped
:substrate: script
:script: checks/server_stopped.py
:trigger: after:stop-server
```

Press Finish below to end the workshop.
