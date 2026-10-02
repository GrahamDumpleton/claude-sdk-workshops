---
title: How it ended
requires: [verify:ending-read]
---

# How it ended

The first thing a program asks of a run is whether it worked. Three
fields answer that, and two more say how much work the run was.

```{cell-insert}
:id: insert-ending
:path: {{ notebook }}
:tags: [ending]
:run: true
print("subtype     :", result.subtype)
print("is_error    :", result.is_error)
print("stop_reason :", result.stop_reason)
print("turns       :", result.num_turns)
print("seconds     :", result.duration_ms / 1000)
```

- **subtype** says how the run ended. `success` means the agent
  finished the job on its own. Every other value starts with `error_`
  and names what stopped it, and a later page produces one.

- **is_error** is the same answer as a true or false.

- **stop_reason** is why the model stopped writing its last reply.
  `end_turn` means it had said what it meant to say.

- **turns** counts the times round the loop: one for each tool the
  model asked for, and one for the answer.

- **seconds** is how long the run took from start to finish, which the
  result reports in milliseconds as `duration_ms`.

Check `subtype` before reading `result`. The answer is only there when
the subtype is `success`.

```{verify}
:id: ending-read
:label: The run ended in success, after more than one turn
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed ending
if result.num_turns < 2:
    print("The run took one turn, so the model answered without reading. Run the cell on the previous page again.")
result.subtype == "success" and not result.is_error and result.num_turns >= 2
```
