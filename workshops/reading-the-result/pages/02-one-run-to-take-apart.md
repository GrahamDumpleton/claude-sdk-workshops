---
title: One run to take apart
requires: [verify:run-kept]
---

# One run to take apart

The workshop ships two of the bookshop's documents:
{open}`shop/returns-policy.md` and {open}`shop/staff-handbook.md`. The
agent is given the `Read` tool and a question that needs both.

The cell keeps every message of the run in a list, and keeps the last
one, the `ResultMessage`, under a name of its own. It prints only the
answer. Everything else this workshop looks at is already in that one
message.

```{cell-insert}
:id: insert-run
:path: {{ notebook }}
:tags: [run]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "Find the answer in the shop's documents before you reply, and answer in "
        "two or three sentences."
    ),
    tools=["Read"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=8,
)

question = (
    "A customer is returning a book and has no receipt. What do I have to do, "
    "and when do I need the manager? The documents are shop/returns-policy.md "
    "and shop/staff-handbook.md."
)

messages = []

async for message in query(prompt=question, options=options):
    messages.append(message)
    if isinstance(message, ResultMessage):
        result = message

print(result.result)
```

`result.result` is the final answer as plain text. A program that
only wanted the answer could stop here. The pages that follow read the
other fields of the same message, and none of their cells calls the
model.

```{verify}
:id: run-kept
:label: The run finished and its result was kept
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed run
if result.subtype != "success":
    print("The run ended with", result.subtype, "- run the cell again.")
result.subtype == "success" and bool(result.result)
```
