---
title: A function the agent can ask for
requires: [verify:tool-defined, verify:tool-called]
---

# A function the agent can ask for

A tool of your own has four parts, and `@tool` takes the first three
as its arguments:

- **A name**, which the model uses to ask for it.

- **A description**, which says what the tool does. The model reads it
  to decide when the tool is the right one.

- **An input schema**, the shape of what the model has to pass. Here
  it is `{"title": str}`: one piece of text called `title`.

- **A handler**, the function under the decorator. It is given the
  input as a dictionary and returns what the model should be told, as
  a list of content blocks.

The handler here looks a title up in the stock list. It also notes
each call in a list, `handler_calls`, so that you can see afterwards
that your own function was run.

A tool is not handed to an agent on its own. It goes into a server,
which is a named group of tools, made by `create_sdk_mcp_server()`.
This cell defines the tool and the server, and calls nothing.

```{cell-insert}
:id: insert-tool
:path: {{ notebook }}
:tags: [tool]
:run: true
def load_stock():
    with open("shop/stock.csv", newline="") as handle:
        return list(csv.DictReader(handle))


handler_calls = []


@tool(
    "check_stock",
    "Look up one book in the shop's stock list by its exact title. Returns the "
    "author, the stock code, the number of copies in stock and the shelf. It "
    "matches the whole title only: it cannot search by author, by subject or by "
    "part of a title. If you do not have the exact title, ask for it.",
    {"title": str},
)
async def check_stock(args):
    handler_calls.append(args)
    wanted = args["title"].strip().lower()
    for book in load_stock():
        if book["title"].lower() == wanted:
            text = (
                f"{book['title']} by {book['author']}: stock code {book['stock_code']}, "
                f"{book['copies']} in stock, {book['shelf']}"
            )
            break
    else:
        text = f"No book with the title {args['title']!r} is in the stock list."
    return {"content": [{"type": "text", "text": text}]}


shop_server = create_sdk_mcp_server(name="shop", version="1.0.0", tools=[check_stock])

print("tool   :", check_stock.name)
print("server :", shop_server["name"], "of type", shop_server["type"])
```

```{verify}
:id: tool-defined
:label: The tool and its server are defined
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed tool
check_stock.name == "check_stock" and shop_server["type"] == "sdk"
```

## Hand the server to the agent

The server goes to the agent in the `mcp_servers` option, under a name
you choose, here `shop`. The agent then knows the tool as
`mcp__shop__check_stock`: the letters `mcp`, the server's name and the
tool's name, joined by double underscores. The next workshop says what
MCP is. For now it is the name of the way tools are plugged in.

Two more options matter:

- `tools=[]` gives the agent no built-in tools. That option only
  covers the built-in ones, so the tools of your server are still
  there.

- `allowed_tools=["mcp__shop__*"]` approves every tool of the `shop`
  server ahead of time. A tool of your own needs approval before it
  runs, as `Write` does, because the SDK cannot know what your
  function does. Without this line the call would be refused.

The same run is made several times in this workshop, with a different
question or a different server, so the cell below defines a function
for it. `ask()` runs the agent, prints each request the model makes
and what your function sent back, and returns what happened. It calls
nothing yet.

```{cell-insert}
:id: insert-ask
:path: {{ notebook }}
:tags: [ask]
:run: true
system_prompt = (
    "You are the assistant for the staff of Tidewater Books, a small bookshop. "
    "Answer in one or two sentences, from what your tools tell you and nothing else."
)


def text_of(content):
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content)
    return str(content)


async def ask(question, server):
    options = ClaudeAgentOptions(
        model="haiku",
        system_prompt=system_prompt,
        tools=[],
        mcp_servers={"shop": server},
        allowed_tools=["mcp__shop__*"],
        setting_sources=[],
        strict_mcp_config=True,
        thinking={"type": "disabled"},
        max_turns=8,
    )
    run = {"calls": [], "inputs": []}
    async for message in query(prompt=question, options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            run["tools"] = message.data["tools"]
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    run["calls"].append(block.name)
                    run["inputs"].append(block.input)
                    print("the model asks      :", block.name, block.input)
        elif isinstance(message, UserMessage) and isinstance(message.content, list):
            for block in message.content:
                if isinstance(block, ToolResultBlock):
                    print("your function says  :", text_of(block.content))
        elif isinstance(message, ResultMessage):
            run["result"] = message
    print()
    print(run["result"].result)
    return run


print("ready to ask")
```

## Ask something only the tool can answer

The first question is about one book, by its title.

```{cell-insert}
:id: insert-first
:path: {{ notebook }}
:tags: [first]
:run: true
title_question = (
    "Do we have A Field Guide to Knots in stock? Give me its stock code and its shelf."
)

first = await ask(title_question, shop_server)

print()
print("tools the agent had    :", first["tools"])
print("your function was given:", handler_calls)
```

Read it from the top. The model asked for `mcp__shop__check_stock` and
passed a title. The SDK ran your function, here in this notebook's
kernel, and sent back the text it returned. The model wrote its answer
from that.

The last line is the list your handler kept. Nothing was sent away to
be run somewhere else. A tool made with `@tool` is a function in your
own program, with everything your program can reach: its files, its
database connections, its other functions.

```{verify}
:id: tool-called
:label: The agent called your function and answered from it
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed first
if "mcp__shop__check_stock" not in first["calls"]:
    print("The model did not ask for the tool. Run the cell again.")
elif "TW-9000-Z" not in first["result"].result:
    print("The answer does not give the stock code from the file. Run the cell again.")
(
    "mcp__shop__check_stock" in first["calls"]
    and len(handler_calls) >= 1
    and "TW-9000-Z" in first["result"].result
)
```

```{hint}
:title: When a tool fails
A handler that raises an exception does not stop the run. The SDK
catches the exception and sends its message to the model as the
tool's result, marked as an error, and the model carries on from
there. To choose the words yourself, catch the problem in the handler
and return `"is_error": True` beside `"content"`.
```
