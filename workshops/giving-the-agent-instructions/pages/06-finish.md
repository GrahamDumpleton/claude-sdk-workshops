---
title: What you know now
requires: [quiz:where-to-start]
---

# What you know now

The model is sent two kinds of text. The prompt is the request, and
changes every time. The system prompt is the standing instruction: who
the agent is, what it may draw on, what to do when that runs out, and
how to answer.

- `system_prompt="..."` gives the agent instructions of your own, and
  only those.

- `system_prompt={"type": "preset", "preset": "claude_code", "append": "..."}`
  gives it Claude Code's instructions with yours on the end.

- One changed rule changes what the agent does, in every run.

- The system prompt is sent with every request, so its size is paid on
  every turn. The cache takes most of the sting out of a long one, and
  a short one costs little to begin with.

```{quiz}
:id: where-to-start
:title: Where to start
question: "You are building an agent that answers a shop's customers by email, from the shop's own documents. Which system prompt do you start from?"
options:
  - text: "A prompt of your own, saying who the agent is, what it may draw on and how to answer."
    correct: true
  - text: "The `claude_code` preset, since it is the most complete."
    explanation: "It is complete for a different job. Most of it is about writing software, and it would be sent with every request for an agent that never writes any."
  - text: "The `claude_code` preset with the shop's rules appended."
    explanation: "That works, as the third run showed, and it carries thousands of tokens the agent does not need on every turn. It is the right start for an agent that works on code."
  - text: "None. The customer's email says what is wanted."
    explanation: "The email says what the customer wants. It cannot say what the shop wants its assistant to do, and the customer should not be the one who decides that."
explanation: "An agent with a job of its own starts from a prompt of its own. The preset is for agents that do what Claude Code does."
```

## Where this goes next

Every run so far has been on the same model, the smallest, with a line
in the options that turned its private reasoning off. The next
workshop is about those two choices: what a larger model buys and
costs, what effort changes, and what thinking is.

**Choose a model and how hard it thinks** is next.

Press Finish below to move on.
