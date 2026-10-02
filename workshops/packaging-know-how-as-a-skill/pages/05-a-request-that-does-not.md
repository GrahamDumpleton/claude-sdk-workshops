---
title: A request that does not
requires: [verify:other-request-answered, verify:runs-compared]
---

# A request that does not

Now a request the skill has nothing to do with, put to the same agent
with the same options.

```{cell-insert}
:id: insert-hours
:path: {{ notebook }}
:tags: [hours]
:run: true
hours = await ask("What time does the shop close on a Saturday?")
```

Look at what the model asked for. The skill was as available as it was
a moment ago, and its description was in front of the model. The
description did not fit the question, so there was no reason to load
it, and the agent most likely went straight to the file that answers.

```{verify}
:id: other-request-answered
:label: The agent answered the second request
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed hours
if "4:40" not in hours["result"].result:
    print("The answer does not give the closing time from the file. Run the cell again.")
hours["result"].subtype == "success" and "4:40" in hours["result"].result
```

## What each run was sent

This cell calls nothing. It puts the two runs side by side: the tools
each asked for, and the size in tokens of the first request and the
last request the model was sent.

```{cell-insert}
:id: insert-compared
:path: {{ notebook }}
:tags: [compared]
:run: true
for label, run in [("the refund", refund), ("the hours", hours)]:
    print(
        f"{label:<11} first request {run['requests'][0]:>5}   "
        f"last request {run['requests'][-1]:>5}   {run['calls']}"
    )
```

The two runs began the same size. Each was sent the system prompt, the
tools and the skill's description, and nothing of its body. That
first figure is what it costs to have the skill on hand, and it is
paid whether or not the skill is used.

By its last request the refund run had grown, by the body of the skill
and by the policy it was told to read. The run that never asked for
the skill never carried it.

Compare that with a `CLAUDE.md`. Had the same steps been put in the
project's instruction file, both runs would have carried them from
the first request, and so would every other request this agent is
ever sent.

```{verify}
:id: runs-compared
:label: Both runs began with the description only
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed compared
abs(refund["requests"][0] - hours["requests"][0]) < 100 and refund["requests"][-1] > refund["requests"][0]
```
