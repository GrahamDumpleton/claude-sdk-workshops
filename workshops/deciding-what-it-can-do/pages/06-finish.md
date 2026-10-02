---
title: What you know now
requires: [quiz:read-only-agent]
---

# What you know now

Two questions are asked about every tool, and four options answer
them.

- `tools` decides what exists for the agent. A tool that is not there
  cannot be used, whatever the model asks for.

- `allowed_tools` approves tools by name, so that their calls run
  without anyone being asked. It adds nothing to what the agent has.

- `permission_mode` approves a whole kind of action. `acceptEdits`
  approves changes to files.

- `disallowed_tools` takes tools away, before everything else.

A call that needs approval and gets none is refused. The model is told,
the run goes on, and the result lists the call in
`permission_denials`.

## Why this matters more for an agent

A chat assistant produces text, and the worst a bad reply can do is be
wrong. An agent acts. It runs on your machine, as you, and a tool that
writes files can write any file you can. The model that decides what
to ask for can be mistaken, and it reads text you did not write: a
document it was told to summarise can contain instructions of its own.

So the tools an agent is given, and the calls it may make without
asking, are a decision about risk. The habit these workshops keep is
the one to take away: give an agent the fewest tools the job needs,
approve the narrowest thing that lets it work, and keep it inside one
directory.

```{quiz}
:id: read-only-agent
:title: An agent that must not change anything
question: "You want an agent that can search and read a project's files and can never change one, however it is asked. Which options say that most surely?"
options:
  - text: "`tools=[\"Read\", \"Glob\", \"Grep\"]`, so that no tool that changes anything exists for it."
    correct: true
  - text: "Every tool, with `allowed_tools=[\"Read\", \"Glob\", \"Grep\"]`."
    explanation: "That approves the three, and leaves the tools that write in place. Whether they run then depends on the mode and on who is asked."
  - text: "Every tool, with a system prompt that says never to change a file."
    explanation: "A prompt is an instruction the model follows as well as it can. It is not a lock. The tools are still there to be asked for."
  - text: "Every tool, with `permission_mode=\"acceptEdits\"`."
    explanation: "That mode approves changes to files without asking, which is the opposite of what is wanted."
explanation: "What an agent has not been given, it cannot use. Leaving a tool out is surer than any rule about when it may run."
```

## Where this goes next

Each run so far has been one question and one answer, and the agent
began every one knowing nothing of the last. The next workshop is
about conversation: how an agent comes to remember what was said, and
what that memory is made of.

**Hold a conversation** is next.

Press Finish below to move on.
