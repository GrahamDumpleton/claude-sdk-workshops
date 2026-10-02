---
title: A call that is allowed
requires: [verify:write-allowed]
---

# A call that is allowed

The first job is one the rules permit: read the opening hours in
{open}`shop/opening-hours.md` and write a notice for the door, in
`notices`.

```{cell-insert}
:id: insert-first
:path: {{ notebook }}
:tags: [first]
:run: true
door = Path("notices/door.md")

first = await attempt(
    "Read shop/opening-hours.md and write a short notice for the shop door "
    "giving the opening hours, to the file notices/door.md."
)

print()
print("the notice exists:", door.exists())
```

Read the lines in order. The model asked for `Read`, and nothing came
between the request and the tool: reading inside the working directory
needs no approval, so there was nothing to ask about. Then the model
asked for `Write`. That does need approval, so the SDK stopped and
called your function, the function said yes, and the file was written.

So the callback is not told about everything the agent does. It is
the answer to one question, asked only when the rules already in
force leave a call undecided: may this run?

```{verify}
:id: write-allowed
:label: The callback was asked about the write and allowed it
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed first
if "allowed" not in verdicts(first):
    print("The callback did not allow a write. Run the cell again.")
"allowed" in verdicts(first) and door.exists() and first["denied"] == []
```
