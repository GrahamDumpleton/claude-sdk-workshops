---
title: Tools that wait
requires: [verify:tools-defined, verify:tools-loaded-up-front, verify:tools-deferred]
---

# Tools that wait

The first measurement of this workshop showed that tools take room
before anything is said. Two built-in tools were most of the window.
An agent connected to a few servers of the kind **Connect an MCP
server** used can have dozens of tools, or hundreds, and every one of
their descriptions is sent with every request, used or not.

Tool search is the SDK's answer. With it on, the model is sent only
the names of your tools, and one built-in tool, `ToolSearch`, to look
them up with. When it wants a tool it asks for it by way of
`ToolSearch`, and only then is that tool's description and input
schema put in front of it. It is the idea behind skills, applied to
tools.

To see it, the agent needs a number of tools. This cell makes twenty,
for the back office of the shop. They are made in a loop from a table
of names and descriptions, and every one returns a fixed line, since
it is their descriptions that matter here and not what they do. The
cell calls nothing.

```{cell-insert}
:id: insert-tools
:path: {{ notebook }}
:tags: [tools]
:run: true
catalogue = {
    "check_stock": "Look up how many copies of a book are in stock and which shelf it is on, by exact title.",
    "book_price": "Look up the current selling price of a book, in dollars, by exact title.",
    "order_status": "Look up the status of a customer order by its order number.",
    "supplier_terms": "Look up a supplier's delivery time, minimum order and carriage charge, by supplier name.",
    "staff_rota": "Look up which members of staff are working in the shop on a given date.",
    "event_bookings": "Look up how many places are booked for one of the shop's events, by event name.",
    "voucher_balance": "Look up the balance left on a gift voucher, by voucher number.",
    "loyalty_points": "Look up how many loyalty points a customer has, by customer name.",
    "reserved_copies": "Look up whether a copy of a book is being held for a customer, by title.",
    "new_releases": "List the books due to be published in a given month.",
    "bestsellers": "List the shop's ten best selling books for a given month.",
    "author_visits": "List the authors booked to visit the shop in a given month.",
    "school_orders": "Look up the books a school has on order, by school name.",
    "damaged_stock": "List the copies written off as damaged in a given month.",
    "till_total": "Look up the takings recorded by the till on a given date.",
    "deliveries_due": "List the deliveries expected from suppliers on a given date.",
    "window_display": "Look up which books are in the shop window this week.",
    "book_club_choice": "Look up the book chosen by the shop's book club for a given month.",
    "signed_copies": "List the signed copies the shop holds, with their stock codes.",
    "out_of_print": "Look up whether a book is out of print, by exact title.",
}


def make_tool(name, description):
    async def handler(args):
        if name == "voucher_balance":
            text = f"Voucher {args['query']} has $17.35 left on it."
        else:
            text = f"{name}: nothing is recorded for {args['query']}."
        return {"content": [{"type": "text", "text": text}]}

    return tool(name, description, {"query": str}, annotations=ToolAnnotations(readOnlyHint=True))(handler)


back_office = create_sdk_mcp_server(
    name="backoffice",
    version="1.0.0",
    tools=[make_tool(name, description) for name, description in catalogue.items()],
)


async def measure(tools):
    measured_options = ClaudeAgentOptions(
        model="haiku",
        system_prompt=(
            "You are the assistant for the staff of Tidewater Books, a small bookshop. "
            "Answer in one sentence, from what your tools tell you."
        ),
        tools=tools,
        mcp_servers={"backoffice": back_office},
        allowed_tools=["mcp__backoffice__*"],
        setting_sources=[],
        strict_mcp_config=True,
        thinking={"type": "disabled"},
        max_turns=8,
    )
    run = {"calls": [], "requests": []}
    async with ClaudeSDKClient(options=measured_options) as measuring:
        await measuring.query("How much is left on gift voucher GV-5521?")
        async for message in measuring.receive_response():
            if isinstance(message, AssistantMessage):
                usage = message.usage
                run["requests"].append(
                    usage["input_tokens"]
                    + usage["cache_creation_input_tokens"]
                    + usage["cache_read_input_tokens"]
                )
                for block in message.content:
                    if isinstance(block, ToolUseBlock):
                        run["calls"].append(block.name)
            elif isinstance(message, ResultMessage):
                run["result"] = message
        context = await measuring.get_context_usage()
    sizes = {entry["name"]: entry["tokens"] for entry in context["categories"]}
    run["loaded"] = sizes.get("MCP tools", 0)
    run["waiting"] = sizes.get("MCP tools (deferred)", 0)
    print("tools asked for       :", run["calls"])
    print("first request         :", run["requests"][0], "tokens")
    print("your tools, loaded    :", run["loaded"], "tokens")
    print("your tools, waiting   :", run["waiting"], "tokens")
    print()
    print(run["result"].result)
    return run


print("tools defined:", len(catalogue))
```

```{verify}
:id: tools-defined
:label: Twenty tools and the function that measures a run are defined
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed tools
len(catalogue) == 20 and callable(measure)
```

## Every description, every time

First the way every agent in these workshops has been set up so far:
no built-in tools at all. With no `ToolSearch` tool there is no tool
search, and all twenty descriptions are sent with every request.

```{cell-insert}
:id: insert-up-front
:path: {{ notebook }}
:tags: [up-front]
:run: true
up_front = await measure(tools=[])
```

The model asked for the one tool it needed, straight away, since it
had every description in front of it. The cost is on the third line:
twenty tools' worth of descriptions in the window, for a question
that used one.

```{verify}
:id: tools-loaded-up-front
:label: All twenty descriptions were in the window
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed up-front
up_front["loaded"] > 500 and up_front["waiting"] == 0 and "17.35" in up_front["result"].result
```

## Looked up when wanted

Now the same agent with one built-in tool, `ToolSearch`. Giving the
agent that tool is what turns tool search on.

```{cell-insert}
:id: insert-searched
:path: {{ notebook }}
:tags: [searched]
:run: true
searched = await measure(tools=["ToolSearch"])

print()
print("turns, loaded up front :", up_front["result"].num_turns)
print("turns, with tool search:", searched["result"].num_turns)
```

The descriptions have moved from loaded to waiting. The model was
shown the names of the twenty tools, asked `ToolSearch` for the one
about vouchers, and then called it. Only that tool's description
entered the window.

Compare the two runs honestly, though. Tool search took a turn more,
for the lookup, and `ToolSearch` is a tool with a description of its
own, so with twenty small tools the saving on the first request is
modest. It grows with the number of tools and the length of their
descriptions. An agent with three hundred tools
cannot sensibly send them all, and tool search is what makes such an
agent possible. With a handful, load them and be done.

```{verify}
:id: tools-deferred
:label: With tool search the descriptions waited to be looked for
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed searched
if searched["waiting"] == 0:
    print("No tools were waiting. Check that the cell passes tools=[\"ToolSearch\"].")
(
    searched["waiting"] > 0
    and searched["loaded"] < up_front["loaded"]
    and searched["result"].subtype == "success"
)
```

```{hint}
:title: Tool search and the default set of tools
An agent left with every built-in tool has `ToolSearch` among them,
so tool search is on unless something turns it off. These workshops
name each agent's tools, which leaves it out, and that is why you
have not met it before. The environment variable `ENABLE_TOOL_SEARCH`,
set through the `env` option, gives finer control: `false` turns it
off, and `auto` turns it on only once the tools would take a tenth of
the window.
```
