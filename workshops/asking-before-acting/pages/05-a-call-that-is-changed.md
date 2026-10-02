---
title: A call that is changed
requires: [verify:write-moved]
---

# A call that is changed

Yes and no are not the only answers. The callback is handed the
input the model wants to pass, and it can hand back a different one.
The call then runs with yours.

The third job asks for a notice in a file at the top of the working
directory. The shop keeps its notices in `notices`, and the rule for
this case does not refuse: it allows the write and changes where it
goes.

```{cell-insert}
:id: insert-third
:path: {{ notebook }}
:tags: [third]
:run: true
asked_for = Path("bookclub.md")
moved_to = Path("notices/bookclub.md")

third = await attempt(
    "Write a two line notice about the harbour book club, which meets on the "
    "first Tuesday of the month at 6:30pm, to the file bookclub.md."
)

print()
print("written where the model asked :", asked_for.exists())
print("written where the rule sent it:", moved_to.exists())
```

The model asked to write `bookclub.md`. The callback returned
`PermissionResultAllow(updated_input=...)` with the path changed, and
the tool wrote the file under `notices`. Nothing was refused, so
nothing is listed as denied.

The model is not told that its input was changed. It sees the result
of the tool, which here names the file that was written, and may or
may not remark on it. So a change of this kind suits corrections the
agent does not need to reason about: a path kept inside a directory, a
limit added to a query, a field filled in. Where the agent ought to
know, refuse with a message that says what to do.

```{verify}
:id: write-moved
:label: The write ran with the input the callback gave it
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed third
if "changed" not in verdicts(third):
    print("The callback was not asked about a file outside notices. Run the cell again.")
"changed" in verdicts(third) and moved_to.exists() and not asked_for.exists()
```
