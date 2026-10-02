---
title: Do the reading yourself
requires: [verify:ask-defined, verify:read-directly]
---

# Do the reading yourself

First the plain way, as a measure to set the other against. One agent
is given `Glob` and `Read` and a question about the suppliers.

The same question is put several times in this workshop, to agents set
up differently, so the first cell defines a function for the run.
`ask()` takes a set of options and does three things:

- it prints each tool request, and says whether the main agent made it
  or a subagent did;

- it keeps the result;

- when the run is over, it asks the client how much of the main
  conversation there is, in tokens, the unit a model reads and writes
  in. A token is about the size of a short word.

It uses a `ClaudeSDKClient`, which keeps the session open long enough
to ask that last question. The cell calls nothing yet.

```{cell-insert}
:id: insert-ask
:path: {{ notebook }}
:tags: [ask]
:run: true
question = (
    "Which of our suppliers deliver within a week, that is in seven working days "
    "or fewer, and what is the minimum order for each? The suppliers' terms are "
    "in the suppliers directory."
)


def describe(block):
    if block.name == "Agent":
        return f"Agent, to the {block.input.get('subagent_type')}: {block.input.get('description')}"
    target = block.input.get("file_path") or block.input.get("pattern") or ""
    return f"{block.name} {Path(target).name if block.name == 'Read' else target}"


def words_in(content):
    if isinstance(content, list):
        content = " ".join(part.get("text", "") for part in content)
    return len(str(content).split())


async def ask(options):
    run = {"main": [], "inside": [], "report_words": None}
    handed_over = set()
    async with ClaudeSDKClient(options=options) as client:
        await client.query(question)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if not isinstance(block, ToolUseBlock):
                        continue
                    if message.parent_tool_use_id is None:
                        run["main"].append(block.name)
                        print("the main agent asks :", describe(block))
                        if block.name == "Agent":
                            handed_over.add(block.id)
                    else:
                        run["inside"].append(block.name)
                        print("    the subagent asks :", describe(block))
            elif isinstance(message, UserMessage) and isinstance(message.content, list):
                for block in message.content:
                    if isinstance(block, ToolResultBlock) and block.tool_use_id in handed_over:
                        run["report_words"] = words_in(block.content)
                        print("the report comes back :", run["report_words"], "words")
            elif isinstance(message, ResultMessage):
                run["result"] = message
        context = await client.get_context_usage()
    sizes = {entry["name"]: entry["tokens"] for entry in context["categories"]}
    run["conversation"] = sizes.get("Messages", 0)
    print()
    print(run["result"].result)
    print()
    print("the main conversation now holds:", run["conversation"], "tokens")
    return run


print("ready to ask")
```

```{verify}
:id: ask-defined
:label: The function that runs the agent is defined
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed ask
callable(ask) and len(list(Path("suppliers").glob("*.md"))) == 10
```

## One agent, ten files

The options are the kind you have written many times. The run takes a
little longer than usual, since there are ten files to read.

```{cell-insert}
:id: insert-direct
:path: {{ notebook }}
:tags: [direct]
:run: true
direct_options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "Answer in a few sentences, from what you find in the shop's files and nothing else."
    ),
    tools=["Glob", "Read"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=30,
)

direct = await ask(direct_options)
```

The agent listed the directory, read all ten files, and answered. The
answer is a few lines. Look at the last line of the output, though:
the conversation holds thousands of tokens, nearly all of them the
text of the ten files.

The answer needed one sentence from each file, the one that gives the
delivery time and the minimum order. The rest, about accounts and
damaged deliveries and window posters, is still in the conversation,
and would be sent again with every question this agent was asked
next.

```{verify}
:id: read-directly
:label: The agent read the files itself and answered
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed direct
if "Spindrift" not in direct["result"].result:
    print("The answer does not name a supplier it should. Run the cell again.")
(
    "Read" in direct["main"]
    and direct["inside"] == []
    and "Spindrift" in direct["result"].result
)
```
