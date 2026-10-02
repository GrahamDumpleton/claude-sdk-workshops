---
title: What each conversation held
requires: [verify:conversations-compared]
---

# What each conversation held

Both runs are still in the notebook. This cell calls nothing. It sets
side by side what the main conversation held at the end of each, and
what each run used in total.

```{cell-insert}
:id: insert-compared
:path: {{ notebook }}
:tags: [compared]
:run: true
def total_sent(run):
    return sum(
        usage["inputTokens"] + usage["cacheReadInputTokens"] + usage["cacheCreationInputTokens"]
        for usage in run["result"].model_usage.values()
    )


for label, run in [("reading it yourself", direct), ("handing it over", delegated)]:
    print(
        f"{label:<20} main conversation {run['conversation']:>6} tokens   "
        f"sent in total {total_sent(run):>6} tokens   "
        f"estimated ${run['result'].total_cost_usd:.3f}"
    )

print()
print("the report that came back:", delegated["report_words"], "words")
```

Read the first column of figures. The agent that did its own reading
is left holding all ten files. The agent that handed the reading over
is left holding a report, and its conversation is a fraction of the
size.

Now the other two columns, which count everything the model was sent
across the whole run, by the main agent and the subagent together,
and what that would cost at API prices. Under a subscription nothing
is charged per run, and the figure is a measure of size. Handing the
work over did not make the job cheaper. The ten files were still
read, by the subagent, and starting a subagent has a cost of its own.

So a subagent does not save work. It saves room, in the one
conversation that carries on. That is worth having when:

- the session is long, and what one question drags in would be paid
  for again on every later turn;

- the job is wide, and several subagents can each take a part and run
  at the same time;

- the work wants different instructions, tools or a different model
  from the main agent's.

For a single question that ends the session, as here, reading it
yourself is the simpler choice and costs no more.

```{verify}
:id: conversations-compared
:label: The delegating agent's conversation is the smaller
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed compared
if delegated["conversation"] >= direct["conversation"]:
    print("The main agent seems to have read the files itself. Run the cell on the page before again.")
delegated["conversation"] < direct["conversation"]
```
