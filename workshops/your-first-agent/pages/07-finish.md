---
title: What you know now
requires: [quiz:how-a-run-ends]
---

# What you know now

An agent is a model with a program around it. The model takes text and
produces text. The program, here the Claude Agent SDK, tells the model
which tools exist, carries out the ones it asks for, and sends back
what they found.

One call runs it:

```python
async for message in query(prompt=question, options=options):
    ...
```

What comes back is a stream of messages:

- a `SystemMessage` with the subtype `init`, saying what the session
  was given: the model, the tools, the working directory;

- an `AssistantMessage` for each thing the model produced, holding a
  `TextBlock` when it says something and a `ToolUseBlock` when it asks
  for a tool;

- a `UserMessage` holding a `ToolResultBlock`, when the SDK sends back
  what a tool found;

- a `ResultMessage` at the end, with how the run went and the final
  answer.

With `tools=[]` the model could only say that it could not see the
file. With `tools=["Read"]` it asked for the file, the SDK read it, and
the answer was right.

```{quiz}
:id: how-a-run-ends
:title: How a run ends
question: "Your program wants to know that a run is over, whether it worked, and what the answer was. Which message tells it?"
options:
  - text: "The `ResultMessage`."
    correct: true
  - text: "The `SystemMessage` with the subtype `init`."
    explanation: "That one comes first. It says how the session was set up, before the model has said anything."
  - text: "The last `AssistantMessage`."
    explanation: "It holds the model's final words, and nothing that says the run is over or whether it succeeded. A run that hits a limit also ends, with no final answer."
  - text: "The `UserMessage` holding the tool result."
    explanation: "That is the SDK sending the model what a tool found, part way through the run."
explanation: "The `ResultMessage` is always last. Its `subtype` says how the run ended and its `result` holds the final answer."
```

## Where this goes next

The run on the last page went by in a few lines of output. The next
workshop slows it down, on a question that takes several tool calls:
what a request from the model really is, who carries it out, and why
the result comes back in a message from the user.

**Watch the agent loop** is next.

Press Finish below to move on.
