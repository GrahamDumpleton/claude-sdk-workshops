---
title: What you know now
requires: [quiz:where-a-rule-belongs]
---

# What you know now

An agent can be given standing instructions from a file.

- A `CLAUDE.md` in the working directory holds instructions for any
  agent that works there.

- `setting_sources=["project"]` loads it, along with the `CLAUDE.md`
  of every directory above. `setting_sources=[]` loads nothing.

- `get_context_usage()` on a connected client lists the files a
  session was given, under `memoryFiles`.

- The file is sent with every request. It costs its length each time,
  and it holds through a session of any length.

- Left out, the option loads your own settings and instructions as
  well, which is why an agent built for a job sets it.

```{quiz}
:id: where-a-rule-belongs
:title: Where a rule belongs
question: "A shop wants every agent that works on its files, the ones its staff type to and the ones its programs run, to sign replies the same way. Where does the rule go?"
options:
  - text: "In the prompt of each request."
    explanation: "Every person and every program would have to remember to add it, and it would be lost when a long conversation is summarised."
  - text: "In the system prompt of each program."
    explanation: "That covers the programs, one at a time. It does nothing for a person using Claude Code in the same directory."
  - text: "In the project's `CLAUDE.md`."
    correct: true
  - text: "In your own `CLAUDE.md`, under your home directory."
    explanation: "That file is yours. It reaches agents you run, on your machine, and nobody else's."
explanation: "A rule that belongs to a project goes in the project's file, where every agent that loads project instructions is given it."
```

## What comes next

A `CLAUDE.md` is sent whole with every request, so it suits what an
agent needs all the time. **Package know-how as a skill** is about the
rest: a procedure the agent needs once in a while, kept in a file that
stays out of the way until the moment it is wanted.

Press Finish below to end the workshop.
