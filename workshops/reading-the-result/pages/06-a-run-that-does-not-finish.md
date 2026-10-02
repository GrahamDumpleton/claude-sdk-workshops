---
title: A run that does not finish
requires: [quiz:what-comes-back, verify:limit-hit]
---

# A run that does not finish

Nothing in the loop decides how many turns a run takes. The model goes
on asking for tools until it thinks it has enough, and a model that is
confused, or has been given a job with no end, could go on for a long
time. `max_turns` is the guard: the run is stopped once it has taken
that many turns.

Every cell so far set it higher than the job needed. This one sets it
to one, on the same question, which needs at least a turn to read and
another to answer.

```{quiz}
:id: what-comes-back
:title: What comes back
question: "The job needs more than one turn and the run is allowed one. What do you expect to get back?"
options:
  - text: "A shorter answer, made from whatever the model had read by then."
    explanation: "The model is not asked to wrap up. The run is stopped between turns, and the model never gets the chance to answer."
  - text: "An answer from what the model already knew, with no file read."
    explanation: "The model does not know about the limit, so it sets about the job the same way as before."
  - text: "A result that says the limit was reached, with no answer in it."
    correct: true
  - text: "Nothing at all. The call never returns."
    explanation: "The limit exists so that a run always ends. It ends with a result, like any other run."
explanation: "A stopped run still ends with a `ResultMessage`. Its subtype names the limit, and its `result` is empty because the model never wrote an answer."
```

The cell copies the options with one field changed, runs the question
again, and prints what it gets. It is written with `try` because of
what the SDK does after the result arrives, which the output shows.

```{cell-insert}
:id: insert-limited
:path: {{ notebook }}
:tags: [limited]
:run: true
limited_options = replace(options, max_turns=1)

limited = None
caught = None

try:
    async for message in query(prompt=question, options=limited_options):
        if isinstance(message, ResultMessage):
            limited = message
except ResultError as error:
    caught = type(error).__name__
    print("raised   :", caught)
    print("it said  :", error)

print("subtype  :", limited.subtype)
print("is_error :", limited.is_error)
print("result   :", limited.result)
print("errors   :", limited.errors)
print("cost     :", limited.total_cost_usd)
```

Two things happened, in this order:

1. The run ended with a `ResultMessage` whose subtype is
   `error_max_turns`. There is no answer in `result`, and `errors` says
   why. The cost is still reported: the turn that was taken was used
   and counted.

2. `query()` then raised a `ResultError`. A run that ends in an error
   is not allowed to pass for one that worked, so a program that does
   not check the subtype is stopped by the exception.

A program that calls an agent needs both halves: read the subtype on
the result, and wrap the loop in `try` when it must carry on after a
failure.

```{verify}
:id: limit-hit
:label: The run was stopped by its turn limit
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed limited
if limited.subtype != "error_max_turns":
    print("The run ended with", limited.subtype, "and not at the limit. Run the cell again.")
limited.subtype == "error_max_turns" and limited.result is None and caught == "ResultError"
```

```{hint}
:title: Other limits
`max_budget_usd` stops a run once its estimated cost passes a figure
you give, and the result's subtype is then `error_max_budget_usd`. An
agent that runs with nobody watching should have one limit or the
other.
```
