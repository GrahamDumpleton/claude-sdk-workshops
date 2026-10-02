---
title: Effort
requires: [verify:low-effort-ran]
---

# Effort

The choice of model is the coarse control. `effort` is a finer one,
on the same model: how much work the model puts into each reply. At a
low level it reasons less, makes fewer checks and writes less. At a
high level it is more thorough and takes longer. The levels are
`"low"`, `"medium"` and `"high"`, with higher ones on some models, and
when the option is left out the level is chosen for you.

Not every model takes the option. The larger ones do, so this run
repeats the Sonnet run with `effort="low"`.

```{cell-insert}
:id: insert-low-effort
:path: {{ notebook }}
:tags: [low-effort]
:run: true
answer = await run_task("sonnet, low effort", "sonnet", effort="low")

print(answer.result)
print()
print("read:", rows["sonnet, low effort"]["read"])
print()
show()
```

Compare the last two rows, and the two answers. Look at whether the
low effort run read fewer files, took fewer turns, wrote fewer tokens
or finished sooner, and whether its answer still has all three parts.

On a task this small the difference is often slight, and it can go
either way between one pair of runs: there is little reasoning here to
save. The option earns its place on long jobs of many steps, where a
high level buys care on work that needs it, and a low level saves time
and usage on work that does not, such as looking something up or
listing files.

```{verify}
:id: low-effort-ran
:label: The task ran at low effort
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed low-effort
ended = [rows[label]["ended"] for label in ("haiku", "sonnet", "sonnet, low effort")]
if ended != ["success"] * 3:
    print("The three runs ended with", ended, "- run again the one that did not succeed.")
ended == ["success"] * 3
```
