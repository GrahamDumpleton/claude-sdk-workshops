---
title: See every call
requires: [verify:calls-logged]
---

# See every call

A hook does not have to decide anything. The other common use is to
keep a record. `PostToolUse` is the event for a tool that has just
run, and a hook registered under it is told what was asked for and
what came back.

The hook below writes one line to a list for each call. Its
`HookMatcher` has no `matcher`, so it is called for every tool. The
job is run a third time with both hooks in place.

```{cell-insert}
:id: insert-logged
:path: {{ notebook }}
:tags: [logged]
:run: true
log = []


async def record(event, tool_use_id, context):
    log.append((event["tool_name"], place(event["tool_input"].get("file_path", ""))))
    return {}


blocked.clear()

logged = await attempt(
    hooks={
        "PreToolUse": [guard],
        "PostToolUse": [HookMatcher(hooks=[record])],
    }
)

print()
print("the log of calls that ran:")
for tool_name, where in log:
    print("  ", tool_name, where)
```

The log has the read of the opening hours and the write of the
notice. Two things about it are worth noticing.

The `Read` is there. Reading inside the working directory needs no
approval, so a permission callback, the mechanism of **Ask before
acting**, is never asked about it. A hook is called all the same. A
callback answers the question "may this run?" when someone has to. A
hook is told about every call, whether or not anyone had to be asked.

The write to `archive` is not there, if the model tried it. The first
hook refused it, so it never ran, and `PostToolUse` reports only what
ran. A log kept this way is a record of what the agent did, not of
what it wanted to do.

```{verify}
:id: calls-logged
:label: The hook recorded the calls that ran
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed logged
if not any(tool_name == "Read" for tool_name, _ in log):
    print("The log has no Read in it. Run the cell again.")
(
    any(tool_name == "Read" for tool_name, _ in log)
    and all(not where.startswith("archive") for _, where in log)
    and not logged["archived"]
)
```
