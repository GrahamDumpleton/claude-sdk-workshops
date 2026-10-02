---
title: What you know now
requires: [quiz:which-kind-of-server]
---

# What you know now

An agent can use tools that live in another program.

- MCP, the Model Context Protocol, is a standard way for a program to
  offer tools. A server offers them, a client uses them, and a server
  written once works with any client.

- A `stdio` entry in `mcp_servers` gives the command that starts a
  server. The SDK starts it, asks it what tools it has, and names each
  one `mcp__<server>__<tool>`.

- `get_mcp_status()` on a connected client reports each server's
  status and tools. A server that fails raises nothing and is reported
  there.

- Tools from a server need approving with `allowed_tools`, by server
  or by tool.

- `strict_mcp_config=True` keeps out every server your code did not
  name.

```{quiz}
:id: which-kind-of-server
:title: Which kind of server
question: "You have a lookup that three different agents need: one built with the SDK, Claude Code on your team's laptops, and the Claude desktop app. Where should it live?"
options:
  - text: "In a function decorated with `@tool`, copied into each program."
    explanation: "A tool made with `@tool` exists only inside the Python program that defines it. Claude Code and the desktop app cannot use it."
  - text: "In an MCP server of its own, which each of the three connects to."
    correct: true
  - text: "In the system prompt, as a description of the data."
    explanation: "A prompt can describe data. It cannot look anything up."
  - text: "It has to be written three times, once for each agent."
    explanation: "That is the problem the protocol exists to remove."
explanation: "A tool that more than one program needs belongs in a server. A tool that only one program needs, and that wants to reach into that program's own state, can stay inside it."
```

## What comes next

**Answer from your own data** uses both kinds of tool you now have,
the built-in ones that search and read files and a tool of your own in
front of a database, and compares the two as ways of putting what you
know within an agent's reach.

Press Finish below to end the workshop.
