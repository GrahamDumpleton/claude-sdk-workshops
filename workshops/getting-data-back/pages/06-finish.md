---
title: What you know now
requires: [quiz:what-a-schema-promises]
---

# What you know now

An agent can end a run with data in place of prose.

- `output_format={"type": "json_schema", "schema": ...}` describes the
  shape wanted, as a JSON Schema.

- `structured_output` on the result is then a Python value in that
  shape, checked against the schema before it is handed back.

- The descriptions in the schema are read by the model. Use them to
  say what each field means and what form it takes.

- The agent still loops, reads and reasons on the way. Only the form
  of its final answer changes.

- A run that cannot produce a fitting value ends with the subtype
  `error_max_structured_output_retries`.

```{quiz}
:id: what-a-schema-promises
:title: What a schema promises
question: "An agent returns `structured_output` that fits your schema. What can your program rely on?"
options:
  - text: "That the fields are there, with the names and types the schema gives."
    correct: true
  - text: "That every value in it is true."
    explanation: "The schema fixes the shape, not the facts. An agent that misread the file would return a wrong closing time in a perfectly well formed entry."
  - text: "That the agent used no tools."
    explanation: "The agent used its tools as it would on any run. Here it read the file before it answered."
  - text: "That the same data comes back on every run."
    explanation: "The shape is the same every time. What is in it is still the model's work, and can differ between runs."
explanation: "A schema guarantees shape. Whether the contents are right still depends on what the agent was given to work from and how well it read it."
```

## Where these workshops have got to

You began with one call and a model that could not open a file. You
can now do what any program built on an agent does:

- run an agent and read every message it produces;

- follow the loop, and tell what the model did from what the SDK did;

- read what a run cost and what stopped it;

- give an agent its instructions, choose its model, and decide what it
  may do;

- hold a conversation with it, and take one up again later;

- show its reply as it is written, and get data back from it.

There are two ways an agent is used, and you have done both. As a
conversation, it talks to a person, turn by turn. As a function, it is
called by a program and returns a value.

## What comes next

**Extending an agent with the Claude Agent SDK** is the next set of
workshops. The agents here used the tools that come built in. Those
workshops give an agent tools you write yourself, connect it to other
services, have it answer from your own data, and put limits on it in
code.

**Building a chat app with the Claude Agent SDK** follows that, and
builds a web application around an agent a step at a time.

Press Finish below to end the workshop.
