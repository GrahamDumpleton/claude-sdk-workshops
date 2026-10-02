---
title: What you know now
requires: [quiz:when-the-callback-is-asked]
---

# What you know now

A function of yours can decide what an agent is allowed to do, call by
call.

- `can_use_tool` names an `async` function that is given the tool's
  name and the input the model wants to pass.

- `PermissionResultAllow()` lets the call run, and with
  `updated_input` it runs with input of your choosing.

- `PermissionResultDeny(message=...)` stops it, and the model is sent
  the message as the result.

- A question from the agent, through `AskUserQuestion`, arrives at the
  same function and is answered through `updated_input`.

- The function is asked only when a call needs approval and nothing
  has already decided it. Calls that need none, and calls approved by
  `allowed_tools` or by a permission mode, never reach it.

```{quiz}
:id: when-the-callback-is-asked
:title: When the callback is asked
question: "An agent has `can_use_tool` set and `allowed_tools=[\"Write\"]`. The model asks to write a file. Is the callback called?"
options:
  - text: "Yes. The callback sees every tool call."
    explanation: "It sees only the calls that are still undecided when every other rule has been applied."
  - text: "No. The write was approved ahead of time, so there is nothing left to ask."
    correct: true
  - text: "Yes, but its answer is ignored."
    explanation: "It is not called at all. A call that an allow rule approves never reaches it."
  - text: "Only if the file is outside the working directory."
    explanation: "Being approved by name covers the tool wherever it writes. The callback would not be asked."
explanation: "The callback stands where the dialog would be in Claude Code: it is consulted when a call needs a decision. To see or stop every call, whatever has been approved, there is another mechanism."
```

## What comes next

That other mechanism is a hook. **Put guardrails in code** uses one to
enforce a rule on every call, whether or not the call needed anyone's
approval, and sets hooks beside the callback you wrote here.

Press Finish below to end the workshop.
