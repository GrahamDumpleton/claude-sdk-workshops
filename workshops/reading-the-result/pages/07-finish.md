---
title: What you know now
requires: [quiz:before-reading-the-answer]
---

# What you know now

Every run ends with a `ResultMessage`, and it is the run's report on
itself:

- `subtype` and `is_error` say how the run ended. `success` is the
  only subtype that comes with an answer.

- `num_turns` and `duration_ms` say how much work it was.

- `usage` counts the tokens: input, output, and the input written to
  and read from the cache. Input is counted again on every turn.

- `total_cost_usd` is those tokens at API prices. On a subscription it
  is a measure of size, and the tokens count against the plan's
  limits. A `RateLimitEvent` in the stream says where those stand.

A run stopped by `max_turns` ends with the subtype `error_max_turns`
and no answer, and `query()` raises `ResultError` after yielding it.

```{quiz}
:id: before-reading-the-answer
:title: Before reading the answer
question: "Your program runs an agent overnight and stores `result.result` in a database. What should it check first?"
options:
  - text: "That `total_cost_usd` is above zero."
    explanation: "A stopped run reports a cost as well. Cost says the run used something, not that it finished."
  - text: "That `subtype` is `success`."
    correct: true
  - text: "That `num_turns` is below `max_turns`."
    explanation: "That would usually hold for a run that worked, and it is a roundabout way to ask. The subtype says directly how the run ended, and covers the other ways a run can fail."
  - text: "Nothing. If there is no answer, `query()` raises."
    explanation: "It does raise, after it has yielded the result. Code that stored the result as it arrived has already stored an empty one."
explanation: "The subtype is the run's own statement of how it ended, and `result` is only filled in when it is `success`."
```

## Where this goes next

Every run so far worked under a line or two of instructions that the
workshops passed over quickly. The next workshop is about those
instructions: what a system prompt is, how changing one rule in it
changes what the agent does, and what the size of it adds to every
request.

**Give the agent its instructions** is next.

Press Finish below to move on.
