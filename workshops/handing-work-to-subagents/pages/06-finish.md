---
title: What you know now
requires: [quiz:what-a-subagent-saves]
---

# What you know now

One agent can hand part of a job to another.

- `AgentDefinition` describes a subagent: a `description` the main
  agent chooses it by, a `prompt` of its own, its own `tools` and its
  own `model`. Definitions go in the `agents` option.

- The main agent starts one with the `Agent` tool, which has to be in
  its `tools`, and passes it a task in words.

- A subagent has its own conversation. What it reads stays there, and
  only its final report joins the main conversation.

- Messages from inside a subagent carry a `parent_tool_use_id`, which
  is how the function in this workshop told the two apart.

- The total work is not less. What is saved is room in the main
  conversation, and each agent can run on the model that suits it.

```{quiz}
:id: what-a-subagent-saves
:title: What a subagent saves
question: "A support agent chats with a customer for an hour. Now and then it has to search three hundred pages of manuals to answer. Why give the searching to a subagent?"
options:
  - text: "Because a subagent reads faster than the main agent."
    explanation: "It runs the same loop on the same kind of model. The reading takes as long."
  - text: "Because the pages it reads then stay out of the hour-long conversation, which is sent again on every turn."
    correct: true
  - text: "Because subagents are not counted against usage."
    explanation: "Every request a subagent makes counts, as the totals in this workshop showed."
  - text: "Because the main agent cannot be given `Read`."
    explanation: "It can. The question is where what is read ends up."
explanation: "A subagent keeps bulky, one-off reading out of a conversation that has to go on. The customer's chat carries the short report, not the manuals."
```

## What comes next

This workshop was about keeping one conversation from filling up.
**Keep a long session small** looks at the same problem head on: what
is in a conversation, how to watch it grow, and what the SDK does when
it has grown too far.

Press Finish below to end the workshop.
