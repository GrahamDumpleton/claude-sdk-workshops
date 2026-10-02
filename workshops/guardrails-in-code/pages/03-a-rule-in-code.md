---
title: A rule in code
requires: [verify:rule-enforced]
---

# A rule in code

Now the same rule as code. A hook is an `async` function that the SDK
calls when something happens in the loop. Which thing is chosen by the
event it is registered under. `PreToolUse` is the event for a tool
that is about to run: the model has asked, and nothing has been done
yet.

The function is given three arguments. The first is the one that
matters, a dictionary describing the event. For `PreToolUse` it holds
`tool_name` and `tool_input`, the same two things the model sent.

What it returns decides what happens:

- an empty dictionary lets the call go on as if the hook were not
  there;

- a `hookSpecificOutput` with `permissionDecision` set to `"deny"`
  stops the call, and `permissionDecisionReason` is sent to the model
  as the result.

Hooks are registered in the `hooks` option, under the name of the
event, each wrapped in a `HookMatcher`. The matcher narrows a hook to
the tools it cares about, here `Write` or `Edit`, so that it is not
called for a `Read`.

The cell defines the hook and runs the same job. The system prompt,
the request and the permission mode are the ones the last run had.
The only thing added is the hook.

```{cell-insert}
:id: insert-enforced
:path: {{ notebook }}
:tags: [enforced]
:run: true
blocked = []


async def keep_to_notices(event, tool_use_id, context):
    target = Path(event["tool_input"].get("file_path", "")).resolve()
    if target.is_relative_to(notices):
        return {}
    blocked.append(place(target))
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Files may only be written in the notices directory.",
        }
    }


guard = HookMatcher(matcher="Write|Edit", hooks=[keep_to_notices])

enforced = await attempt(hooks={"PreToolUse": [guard]})

print("the hook refused       :", blocked)
```

The notice in `notices` was written, and the copy in `archive` was
not. If the model asked for it, as it most likely did, the hook
refused the call and an error came back in place of a result, with
the reason you wrote. The last line lists what the hook turned away.

Nothing about the model changed between the two runs. It was sent the
same instructions and the same argument, and may well have made the
same choice. The difference is that this time its choice was not the
last word. The hook does not know or care what the model was told. It
looks at where the file would go.

The permission mode did not get a say either. `acceptEdits` would have
approved the write, and the hook ran before the mode was consulted.

```{verify}
:id: rule-enforced
:label: Nothing was written outside the notices directory
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed enforced
if enforced["archived"]:
    print("archive/door.md exists, so the hook did not stop the write. Check that the cell passes the hook.")
elif not blocked:
    print("Note: the model did not try the second write on this run, so the hook had nothing to refuse.")
not enforced["archived"] and enforced["ended"] == "success"
```

```{hint}
:title: What else a PreToolUse hook can return
`permissionDecision` can also be `"allow"`, which approves the call
without anyone being asked, or `"ask"`, which sends it to whoever
approves calls. Beside the decision, `updatedInput` replaces the
input the tool is run with, as the callback in **Ask before acting**
could. When several hooks answer about one call, a single deny wins.
```
