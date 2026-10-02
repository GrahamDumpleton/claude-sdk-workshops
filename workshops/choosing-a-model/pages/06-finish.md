---
title: What you know now
requires: [quiz:which-model-first]
---

# What you know now

The model makes every decision in a run, so the choice of model is the
one that matters most.

- `model` takes a short name or a full one. A smaller model is faster
  and lighter on a plan. A larger one reads more carefully, follows
  more steps, and costs more of both time and usage.

- `effort` sets how much work a model puts into each reply, on the
  models that take it. Lower it for simple, well defined jobs.

- `thinking` lets the model reason to itself before it replies. The
  reasoning is output and is counted as output. It is for problems
  that need working out, and it is off in these workshops because
  theirs do not.

The table you built is the way to decide. Run the real task on the
smallest model several times and read the answers. If it gets the job
right every time, that is the model to use. If it misses parts of a
job with several steps, move up a size and look again. The price of
moving up is in the last three columns.

```{quiz}
:id: which-model-first
:title: Which model first
question: "You are building an agent that reads a customer's email and files it under one of five headings. Thousands of emails arrive a day. Where do you start?"
options:
  - text: "On the largest model, to be safe, and move down later if it costs too much."
    explanation: "Every one of thousands of runs would take longer and use more than it needs to, for a job with one short step."
  - text: "On the smallest model, checking its answers on real emails, and move up only if it gets them wrong."
    correct: true
  - text: "On the smallest model with thinking turned on, so that it reasons like a larger one."
    explanation: "Thinking adds output to every run and does not turn a small model into a large one. Sorting into five headings does not need working out."
  - text: "On whichever model the SDK picks when `model` is left out."
    explanation: "Then the choice is made by a default that was not chosen for this job, and it can change under you."
explanation: "Use the smallest model that does the job reliably. A simple, well defined job done many times is where a small model pays off most."
```

## Where this goes next

Every tool the agent has been given so far could only look: list
files, search them, read one. The next workshop gives it a tool that
changes something, and that raises a question the workshops have
stepped around until now: who says a call may run.

**Decide what the agent can do** is next.

Press Finish below to move on.
