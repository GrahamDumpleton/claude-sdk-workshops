---
title: What you know now
requires: [quiz:what-the-model-is-sent]
---

# What you know now

The agent loop is a short conversation between the model and the SDK
that your code only watches:

1. The SDK sends the model the conversation so far.

2. The model replies. A `ToolUseBlock` in the reply is a request: a
   tool's name and its input, written as text.

3. The SDK carries the request out, on this machine, and adds what it
   found to the conversation as a `ToolResultBlock`, in a message in
   the user's role.

4. That repeats, a turn at a time, until the model replies with no
   request. That reply is the answer.

The model decides which tools to ask for and when it has enough. The
SDK does the work. Every request carries everything before it, so the
requests grow as the run goes on.

```{quiz}
:id: what-the-model-is-sent
:title: What the model is sent
question: "A run has read two files and is about to ask the model what comes next, for the third time. What is in that request?"
options:
  - text: "Only the contents of the second file, since the model has seen the rest."
    explanation: "The model has seen nothing. It keeps no memory between requests, so anything left out is gone."
  - text: "The question and a summary of what has been found so far."
    explanation: "Nothing is summarised in a run like this one. The requests and results are sent as they were."
  - text: "Everything: the instructions, the question, each request the model made and each result."
    correct: true
  - text: "Nothing new. The model reads the files directly when it needs them."
    explanation: "The model cannot read files. It is sent their contents as text, by the SDK."
explanation: "The model is sent the whole conversation every time, which is why the token count rose with each reply."
```

## Where this goes next

Every run ends with a `ResultMessage`, and this workshop read one
number from it. The next workshop opens the rest: how the run ended,
how long it took, how many tokens it used and what that amounts to,
and what comes back when a run is stopped before it finishes.

**Read what a run cost** is next.

Press Finish below to move on.
