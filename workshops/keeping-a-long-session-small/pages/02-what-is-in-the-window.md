---
title: What is in the window
requires: [verify:window-measured]
---

# What is in the window

A connected client can say what is in the context window at any
moment, with `get_context_usage()`. It answers from what the SDK
already knows, and is not a call to the model. The answer is counted
in tokens, the unit a model reads and writes in. A token is about the
size of a short word.

This cell connects a client, which keeps one session open across the
cells that follow, and defines `snapshot()`. Each time it is called it
measures the window and adds a row to a table, so that the table grows
as the session does. The columns are:

- **tools**, the descriptions of the built-in tools the agent was
  given;

- **conversation**, everything said so far: prompts, replies, tool
  requests and tool results;

- **tool results**, the part of the conversation that is what tools
  sent back;

- **in all**, the whole window.

```{cell-insert}
:id: insert-connect
:path: {{ notebook }}
:tags: [connect]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "Answer in a sentence or two, from what you find and nothing else."
    ),
    tools=["Glob", "Read"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=30,
)

client = ClaudeSDKClient(options=options)

await client.connect()

connected = True

history = []


async def snapshot(label):
    context = await client.get_context_usage()
    sizes = {entry["name"]: entry["tokens"] for entry in context["categories"]}
    history.append(
        {
            "label": label,
            "tools": sizes.get("System tools", 0),
            "conversation": sizes.get("Messages", 0),
            "tool results": context["messageBreakdown"]["toolResultTokens"],
            "in all": context["totalTokens"],
        }
    )
    print(f"{'':<24}{'tools':>8}{'conversation':>14}{'tool results':>14}{'in all':>8}")
    for row in history:
        print(
            f"{row['label']:<24}{row['tools']:>8}{row['conversation']:>14}"
            f"{row['tool results']:>14}{row['in all']:>8}"
        )
    return context


context = await snapshot("before anything")

window_size = context["maxTokens"]
compacts_at = context.get("autoCompactThreshold")

print()
print("the window holds        :", window_size)
print("it is compacted beyond  :", compacts_at)
```

Nothing has been said, and the window is not empty. The two tools the
agent was given are described to the model with every request, and
those descriptions are the largest thing in it so far. That is the
standing cost of an agent, paid on every request before a word of
conversation, and the reason these workshops give each agent only the
tools it needs.

The last two lines are the limits. The first is the size of the
window for this model. The second is the point at which the SDK steps
in by itself to make the conversation smaller, which a later page
does by hand.

```{verify}
:id: window-measured
:label: The client is connected and the window was measured
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed connect
connected and history[0]["tools"] > 0 and history[0]["in all"] < window_size
```

```{hint}
:title: If a cell says the client is not connected
The client was lost, most likely because the kernel was restarted.
Run this page's cell again, then carry on from the cell after it. The
session starts again from nothing, so run the cells that follow in
order.
```
