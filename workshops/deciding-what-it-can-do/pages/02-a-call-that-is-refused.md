---
title: A call that is refused
requires: [quiz:what-happens-to-the-write, verify:write-refused]
---

# A call that is refused

The job is to read {open}`shop/opening-hours.md` and write a notice
for the shop door to a new file, `notices/door.md`. It needs two
tools: `Read`, and `Write`, which creates a file with the contents the
model gives it.

## One function for every attempt

The job is run four times with only the permission options changed, so
the first cell defines the job and a function that attempts it. The
function deletes any notice left by an earlier attempt, runs the agent
with `tools=["Read", "Write"]` and whatever permission options it is
passed, and prints each step. It returns what happened: the tools the
session had, the tools the model asked for, the calls that were
denied, and whether the notice exists afterwards. `report()` prints
that.

This cell calls nothing yet.

```{cell-insert}
:id: insert-attempt
:path: {{ notebook }}
:tags: [attempt]
:run: true
notice = Path("notices/door.md")

task = (
    "Read shop/opening-hours.md and write a short notice for the shop door "
    "giving the opening hours, to the file notices/door.md."
)


async def attempt(**permissions):
    notice.unlink(missing_ok=True)
    options = ClaudeAgentOptions(
        model="haiku",
        system_prompt=(
            "You are the assistant for the staff of Tidewater Books, a small bookshop. "
            "Do what is asked, then say in one sentence what you did. If you cannot do "
            "it, say why and stop."
        ),
        tools=["Read", "Write"],
        setting_sources=[],
        strict_mcp_config=True,
        thinking={"type": "disabled"},
        max_turns=10,
        **permissions,
    )
    outcome = {"calls": []}
    async for message in query(prompt=task, options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            outcome["tools"] = message.data["tools"]
            outcome["mode"] = message.data["permissionMode"]
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    outcome["calls"].append(block.name)
                    print("the model asks      :", block.name)
        elif isinstance(message, UserMessage) and isinstance(message.content, list):
            for block in message.content:
                if isinstance(block, ToolResultBlock):
                    label = "an error comes back :" if block.is_error else "the SDK answers     :"
                    print(label, str(block.content)[:90])
        elif isinstance(message, ResultMessage):
            denials = message.permission_denials or []
            outcome["denied"] = [denial["tool_name"] for denial in denials]
            outcome["ended"] = message.subtype
            outcome["said"] = message.result
    outcome["written"] = notice.exists()
    return outcome


def report(outcome):
    print()
    print("permission mode :", outcome["mode"])
    print("tools given     :", outcome["tools"])
    print("tools asked for :", outcome["calls"])
    print("calls denied    :", outcome["denied"])
    print("notice written  :", outcome["written"])
    print("the agent said  :", outcome["said"])


print("ready to attempt:", task)
```

## The first attempt

The first attempt gives the agent both tools and no permission to use
them beyond what every agent has. `permission_mode="default"` asks for
the standard rules by name: a call that needs approval is put to
whoever is there to approve it. Here nobody is. This is a notebook
cell, and the options name no one to ask.

```{quiz}
:id: what-happens-to-the-write
:title: What happens to the write
question: "The agent has the `Write` tool and nobody is there to approve its use. When the model asks to write the notice, what happens?"
options:
  - text: "The file is written. The agent was given the tool, so it may use it."
    explanation: "Being given a tool lets the model ask for it. Whether a call runs is a second question, decided each time."
  - text: "The run stops and waits for someone to answer."
    explanation: "There is nobody to wait for. A call that cannot be approved is turned down, and the run carries on."
  - text: "The call is refused, the model is told so, and the run ends without the file."
    correct: true
  - text: "The run fails with an exception."
    explanation: "A refused call is not a failure of the run. It is a result the model is sent, like any other tool result, and the run ends normally."
explanation: "A call that needs approval and gets none is refused. The model is sent the refusal as the result of its request, and it goes on from there."
```

```{cell-insert}
:id: insert-first
:path: {{ notebook }}
:tags: [first]
:run: true
first = await attempt(permission_mode="default")

report(first)
```

Read the steps from the top. The model asked for `Read`, and the SDK
answered with the file: reading inside the working directory needs no
approval. Then the model asked for `Write`, and an error came back in
place of an answer. The model was told that it had not been granted
permission, as the result of its request. What it said last is its
response to that.

The summary underneath shows the same thing as data. `Write` is among
the tools given and the tools asked for. It is also under **calls
denied**, which comes from `permission_denials` on the result, and the
notice was not written. The run itself ended normally. A program finds
out that an agent was stopped from doing something by reading that
list.

```{verify}
:id: write-refused
:label: The write was refused and no file was made
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed first
if "Write" not in first["denied"]:
    print("No call to Write was denied. The model may not have tried to write. Run the cell again.")
elif first["written"]:
    print("The notice exists, so a write was allowed. Check that the cell passes only permission_mode=\"default\".")
"Write" in first["denied"] and not first["written"]
```
