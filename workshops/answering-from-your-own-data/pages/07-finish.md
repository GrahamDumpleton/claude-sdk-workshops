---
title: What you know now
requires: [quiz:where-a-total-comes-from]
---

# What you know now

An agent answers from your data when a tool puts that data in front
of the model.

- Documents need nothing new. With `Glob`, `Grep` and `Read`, and a
  system prompt that says where to look, the agent searches and reads
  for itself.

- Records need a tool of yours in front of the database. The tool's
  description has to describe the tables, since the model has seen
  none of them.

- What a tool must never do is made impossible in the tool. Here the
  database was opened read-only.

- Given both, the model chooses between them from what it has been
  told about each.

- The SDK has no index or vector store of its own. Retrieval of that
  kind is another tool you can write.

```{quiz}
:id: where-a-total-comes-from
:title: Where a total comes from
question: "You want an agent to answer \"what did we take in orders last month?\" from a table of forty thousand orders. Which is the sound design?"
options:
  - text: "Export the table to a text file and let the agent read it."
    explanation: "Forty thousand rows would not fit in what the model can be sent, and a model adding up figures it has read is not reliable."
  - text: "Give the agent a tool that runs a query, so the database does the sum."
    correct: true
  - text: "Put the table in the system prompt."
    explanation: "The system prompt is sent with every request. A table that size does not fit, and the sum would still be the model's."
  - text: "Ask the model to estimate from a sample of the rows."
    explanation: "A total is a fact the database can give exactly. There is no reason to estimate it."
explanation: "Let the database do what databases do. The model's part is to work out which query answers the question, and to put the result into words."
```

## What comes next

Everything here was looked up when it was needed. **Give instructions
that persist** is about the other kind of knowledge, the kind an agent
should have in mind all the time: house rules, kept in a file and
loaded with every session.

Press Finish below to end the workshop.
