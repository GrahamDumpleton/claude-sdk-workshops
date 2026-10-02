---
title: Someone to ask
requires: [verify:callback-defined]
---

# Someone to ask

The function the SDK calls is an `async` function of three arguments:

- `tool_name`, the tool the model has asked for;

- `tool_input`, a dictionary of exactly what the model wants to pass
  to it, such as the path and the contents of a file to write;

- `context`, with a few extras this workshop does not need.

It answers by returning one of two objects.

- `PermissionResultAllow()` lets the call run. Given
  `updated_input=...`, it lets the call run with that input in place
  of the model's.

- `PermissionResultDeny(message=...)` stops it. The message is sent to
  the model as the result of its request, so it is written for the
  model to read and act on.

The function below stands in for the shop's manager. Its rules are
about where a file may be written:

- anything outside the agent's working directory is refused;

- the shop's own documents, under `shop`, are refused, with a reason;

- a file under `notices` is allowed;

- a file anywhere else is allowed, and moved into `notices`.

It keeps a note of each decision in `decisions`, and prints it, so
that you can see when it was asked. This cell calls nothing.

```{cell-insert}
:id: insert-callback
:path: {{ notebook }}
:tags: [callback]
:run: true
workspace = Path.cwd().resolve()

decisions = []


def decide(verdict, tool_name, detail):
    decisions.append({"verdict": verdict, "tool": tool_name, "detail": detail})
    print(f"  the callback is asked about {tool_name}: {verdict} ({detail})")


async def approve(tool_name, tool_input, context):
    if tool_name not in ("Write", "Edit"):
        decide("refused", tool_name, "not a tool this shop approves")
        return PermissionResultDeny(message="That tool is not approved here.")

    target = Path(tool_input["file_path"]).resolve()

    if not target.is_relative_to(workspace):
        decide("refused", tool_name, "outside the workspace")
        return PermissionResultDeny(message="Files may only be written in the working directory.")

    place = target.relative_to(workspace)

    if place.parts[0] == "shop":
        decide("refused", tool_name, str(place))
        return PermissionResultDeny(
            message=(
                "The shop's documents are changed by the manager only. "
                "Tell the member of staff to ask Marguerite."
            )
        )

    if place.parts[0] == "notices":
        decide("allowed", tool_name, str(place))
        return PermissionResultAllow()

    moved = workspace / "notices" / place.name
    decide("changed", tool_name, f"{place} becomes notices/{place.name}")
    return PermissionResultAllow(updated_input={**tool_input, "file_path": str(moved)})


print("the callback is defined")
```

## A function for the run

Each page of this workshop gives the agent one job, so this cell
defines a function for the run. The options are the ones you know,
with two things to notice.

- `permission_mode="default"` asks for the standard rules: a call
  that needs approval is put to whoever is there to give it.

- `can_use_tool=callback` says who that is.

It calls nothing yet.

```{cell-insert}
:id: insert-attempt
:path: {{ notebook }}
:tags: [attempt]
:run: true
async def attempt(task, callback=approve, tools=("Read", "Write", "Edit")):
    options = ClaudeAgentOptions(
        model="haiku",
        system_prompt=(
            "You are the assistant for the staff of Tidewater Books, a small bookshop. "
            "Do what is asked, then say in one sentence what you did. If you cannot do "
            "it, say why and stop. If something you need to know was not stated, ask "
            "with the AskUserQuestion tool rather than guessing."
        ),
        tools=list(tools),
        permission_mode="default",
        can_use_tool=callback,
        setting_sources=[],
        strict_mcp_config=True,
        thinking={"type": "disabled"},
        max_turns=12,
    )
    decisions.clear()
    outcome = {"calls": []}
    seen = set()
    async for message in query(prompt=task, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.id not in seen:
                    seen.add(block.id)
                    outcome["calls"].append(block.name)
                    print("the model asks for", block.name)
        elif isinstance(message, ResultMessage):
            outcome["denied"] = [denial["tool_name"] for denial in message.permission_denials or []]
            outcome["ended"] = message.subtype
            outcome["said"] = message.result
    outcome["decisions"] = list(decisions)
    print()
    print(outcome["said"])
    return outcome


def verdicts(outcome):
    return [decision["verdict"] for decision in outcome["decisions"]]


print("ready to attempt")
```

```{verify}
:id: callback-defined
:label: The callback and the function for the run are defined
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed attempt
callable(approve) and callable(attempt)
```

```{hint}
:title: Why the callback checks the path itself
The rules are about where a file ends up, so the function works that
out for itself. It turns the path into an absolute one and compares
it with the working directory before it looks at anything else. A
model can write a path in more than one way, and a rule that only
compared text could be walked around with `..` in the middle.
```
