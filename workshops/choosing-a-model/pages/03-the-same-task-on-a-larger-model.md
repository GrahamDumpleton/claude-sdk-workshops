---
title: The same task on a larger model
requires: [verify:sonnet-ran]
---

# The same task on a larger model

One word of the options changes: `model="sonnet"`. The task, the
instructions and the tools are the same.

A run on the larger model can take longer than the last one did.

```{cell-insert}
:id: insert-sonnet
:path: {{ notebook }}
:tags: [sonnet]
:run: true
answer = await run_task("sonnet", "sonnet")

print(answer.result)
print()
print("read:", rows["sonnet"]["read"])
print()
show()
```

Check this answer against the same three parts: the 37 days, the shop
credit in place of a refund, and the points that come off the card.
Then read the table across.

- **model** shows the two full names the short ones stood for.

- **turns** and **in** show how each model went about the job. One
  that looks in more places takes more turns, and every turn sends the
  whole conversation again, so the input grows with them.

- **secs** is the wait. A larger model is usually slower for each
  token it writes, though on a job this short the two can come out
  close.

- **est. $** puts a size on the whole run. A token costs several times
  as much on the larger model, so the same job weighs more, on an API
  bill or against a plan's limits.

What you see depends on the run. Either model can do well or badly on
a given attempt, and one pair of runs proves nothing. What holds over
many runs is the trade from the welcome page: the larger model is more
likely to read everything that bears on the question and to get every
part of the answer, and it takes more time and more of your plan to do
it.

```{verify}
:id: sonnet-ran
:label: The task ran on two different models
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed sonnet
if rows["sonnet"]["ended"] != "success":
    print("The run ended with", rows["sonnet"]["ended"], "- run the cell again.")
rows["sonnet"]["ended"] == "success" and rows["sonnet"]["model"] != rows["haiku"]["model"]
```

```{hint}
:title: Other names the model option takes
Short names such as `"haiku"`, `"sonnet"` and `"opus"` are aliases.
Each stands for a current model of that size, so code that uses one
moves to a newer model when the alias does. A full name, such as the
ones in the table, pins a run to that exact model. Which models a
login can use depends on the plan.
```
