---
title: What you know now
requires: [quiz:what-to-do-first]
---

# What you know now

A session has a size, you can measure it, and there are ways to keep
it down.

- `get_context_usage()` on a connected client says what is in the
  context window: the tools, the conversation, and how much of the
  conversation is tool results.

- Everything in the window is sent with every request. A cache makes
  the repeat cheaper and frees no room.

- Compaction replaces the history with a summary. The SDK does it
  when the window is nearly full, and `/compact` sent as a prompt does
  it on request. A `compact_boundary` system message marks it.

- What you said survives a compaction. Detail that was only in a tool
  result may not, so rules that must hold go where they are sent
  every time, and an agent keeps the tools to look things up again.

- With the `ToolSearch` tool, the definitions of your own tools stay
  out of the window until the model looks for one.

## The ways to stay small

These workshops have shown several, and they work together.

| What takes the room | What to do about it | Where it was shown |
| --- | --- | --- |
| Tools the agent never uses | Name the tools with `tools` | Every workshop |
| Many tools from servers | Tool search | This workshop |
| Instructions needed now and then | A skill, loaded on use | **Package know-how as a skill** |
| Reading that is needed once | A subagent, with a conversation of its own | **Hand work to subagents** |
| Whole files where rows would do | A tool that queries | **Answer from your own data** |
| A long history | Compaction | This workshop |

```{quiz}
:id: what-to-do-first
:title: What to do first
question: "An agent's sessions keep reaching the point where they are compacted, and it then forgets details it needs. What is the best first move?"
options:
  - text: "Switch to a model with a larger window and change nothing else."
    explanation: "That puts the problem off and makes every request cost more in the meantime."
  - text: "Find out what is filling the window, with `get_context_usage()`, and keep the bulk out of the main conversation."
    correct: true
  - text: "Turn compaction off."
    explanation: "Then the session fails when the window is full, which is worse than a summary."
  - text: "Tell the model in the system prompt to remember more."
    explanation: "A model cannot keep what is not sent to it. The summary decides what is sent."
explanation: "Measure first. If the window is full of tool results from reading, a subagent or a narrower tool keeps them out. If it is full of tool definitions, give fewer tools or let them be searched for."
```

## Where these workshops have got to

You began this set with an agent that could use only the tools that
came with it. You can now:

- give an agent tools of your own, in your program or in a server any
  agent can use;

- put your documents and your records within its reach;

- give it instructions that are always there, and skills that arrive
  when they are needed;

- put a decision of your own in front of what it does, and rules in
  code that it cannot talk its way past;

- have it hand work to other agents, and keep a long session within
  bounds.

## What comes next

**Building a chat app with the Claude Agent SDK** is the last set of
workshops. It builds a web application around an agent a step at a
time, and what you have learned in these two sets is what it is built
from: a reply streamed to a browser, a conversation for each visitor,
approvals asked in a dialog, and your own tools plugged in.

Press Finish below to end the workshop.
