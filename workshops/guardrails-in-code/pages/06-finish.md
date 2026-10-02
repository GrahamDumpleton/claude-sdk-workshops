---
title: What you know now
requires: [quiz:hook-or-prompt]
---

# What you know now

A rule that must hold goes in code.

- A rule in a prompt is a request. The model weighs it against
  everything else it has been sent, and can be argued out of it.

- A hook is a function the SDK calls at a fixed point in the loop. It
  is registered in the `hooks` option, under the name of an event,
  in a `HookMatcher` that can narrow it to some tools.

- A `PreToolUse` hook sees every call before it runs. Returning a
  `permissionDecision` of `"deny"` stops the call and sends the reason
  to the model. It runs before the permission mode is consulted.

- A `PostToolUse` hook sees every call that ran, which makes it the
  place to keep a record.

- A permission callback is asked only when a call needs approval. A
  hook is told about every call.

```{quiz}
:id: hook-or-prompt
:title: Hook or prompt
question: "An agent answers customers for a shop. Which of these should be a hook, and not a line in the system prompt?"
options:
  - text: "Replies are friendly and short."
    explanation: "Tone is a matter of judgement, which is what a model is for. There is nothing here for code to check."
  - text: "Refunds of more than fifty dollars are never issued without a manager's approval."
    correct: true
  - text: "The agent introduces itself as the shop's assistant."
    explanation: "That is who the agent is, which belongs in the system prompt."
  - text: "Prices are quoted in dollars and cents."
    explanation: "A matter of style. If it slips once, nothing is lost that cannot be put right."
explanation: "Ask in a prompt for what you would like. Enforce in code what must not happen: where a mistake costs money, loses data or cannot be undone, and where the thing to check is a fact about the call."
```

## What comes next

Every agent so far has done its own work. **Hand work to subagents**
has one agent give part of a job to another, which has its own
instructions, its own tools and a context of its own, and hands back
only what it found.

Press Finish below to end the workshop.
