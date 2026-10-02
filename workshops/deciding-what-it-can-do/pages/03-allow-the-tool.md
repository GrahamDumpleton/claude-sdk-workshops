---
title: Allow the tool
requires: [verify:write-allowed]
---

# Allow the tool

The most direct way to let a call run is to approve the tool ahead of
time. `allowed_tools` is a list of tools whose calls are approved
without anyone being asked.

The name misleads on first reading, and it is worth getting straight:

- `tools` is what the agent **has**. A tool that is not in it cannot
  be used at all.

- `allowed_tools` is what the agent may use **without asking**. It
  gives the agent nothing it did not have. A tool left off the list is
  still there, and calls to it that need approval are still put to
  whoever is there to approve them.

The second attempt is the first one with `Write` approved.

```{cell-insert}
:id: insert-second
:path: {{ notebook }}
:tags: [second]
:run: true
second = await attempt(permission_mode="default", allowed_tools=["Write"])

report(second)

print()
print(notice.read_text())
```

This time the request to write was answered and not refused. Nothing
is listed under **calls denied**, the notice was written, and the last
lines are the file itself, read back from disk by the cell. An agent
has changed something on your machine.

```{verify}
:id: write-allowed
:label: The write was approved and the notice exists
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed second
if not second["written"]:
    print("The notice was not written. Run the cell again.")
second["written"] and second["denied"] == []
```

## The checks as a picture

The step below opens a picture of the questions the SDK asks before a
tool is used, with the option that answers each. The first two
attempts took two different ways through it.

```{file-open}
:id: open-checks
:title: Open the picture of the checks
:path: diagrams/may-this-call-run.md
:factory: Markdown Preview
```

```{hint}
:title: Approving less than a whole tool
`allowed_tools=["Write"]` approves every call to `Write`. A rule can
be narrower than that, covering edits under one directory or commands
of one form, so that everything else is still asked about. The
permissions page of the SDK's documentation gives the forms a rule can
take.
```
