---
title: A model for each
requires: [verify:two-models-used]
---

# A model for each

The reader was given `model="haiku"`, and so far the main agent has
run on Haiku too. They need not match.

Reading ten files and picking out a sentence from each is plain work
that the smallest model does well. Deciding what to do with what was
found can be harder, and in a real application the main agent is
where a larger model earns its place. With a subagent you can pay
the larger model for the thinking and the smaller one for the
reading.

This run changes one option: the main agent's model, to Sonnet. The
reader stays on Haiku. The result of a run reports its usage for each
model separately, in `model_usage`, and the cell prints that.

```{cell-insert}
:id: insert-mixed
:path: {{ notebook }}
:tags: [mixed]
:run: true
mixed = await ask(replace(delegating_options, model="sonnet"))

print()
for model, usage in mixed["result"].model_usage.items():
    sent = usage["inputTokens"] + usage["cacheReadInputTokens"] + usage["cacheCreationInputTokens"]
    print(f"{model:<28} sent {sent:>6} tokens   wrote {usage['outputTokens']:>5}")

models_used = list(mixed["result"].model_usage)
```

Two models are listed. The smaller one was sent the bulk of the
tokens, the ten files and the requests it took to read them. The
larger one was sent the question, the definition of the subagent and
the report, and wrote the answer.

`model` in a definition takes the short names you have used,
`"haiku"`, `"sonnet"` and `"opus"`, a full model name, or `"inherit"`
for whatever the main agent is running on.

```{verify}
:id: two-models-used
:label: The main agent and the subagent ran on different models
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed mixed
if len(models_used) < 2:
    print("Only one model was used, so the subagent was not started. Run the cell again.")
len(models_used) >= 2 and "Agent" in mixed["main"]
```

```{hint}
:title: Limits worth knowing about
The model decides when to start a subagent and how many, and each one
makes requests of its own, so a run with subagents can grow.
`max_budget_usd` in the options stops a run when its estimated cost
reaches a figure, subagents included. A subagent cannot ask the user
a question, and unless you say otherwise it can start subagents of
its own. The documentation page linked at the end gives the settings
that cap how deep and how wide that goes.
```
