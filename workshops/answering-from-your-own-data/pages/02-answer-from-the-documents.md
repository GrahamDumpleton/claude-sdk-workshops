---
title: Answer from the documents
requires: [verify:ask-defined, verify:answered-from-documents]
---

# Answer from the documents

Start with the documents. The agent is given three tools that only
look, and is told in its system prompt where the shop keeps its
files. It is not told which file holds what.

The workshop asks three questions, each with a different set of tools,
so the first cell defines a function for the run. `ask()` takes the
question, the built-in tools to give the agent, and any servers of
your own. It prints each thing the model asks for and returns what
happened. It calls nothing yet.

```{cell-insert}
:id: insert-ask
:path: {{ notebook }}
:tags: [ask]
:run: true
system_prompt = (
    "You are the assistant for the staff of Tidewater Books, a small bookshop. "
    "The shop's documents are Markdown files in the shop directory. Its orders "
    "are in a database. Use the tools you have been given to find the answer, "
    "and answer in two or three sentences from what you find and nothing else."
)


def describe(block):
    detail = (
        block.input.get("sql")
        or block.input.get("file_path")
        or block.input.get("pattern")
        or block.input
    )
    return f"{block.name}: {detail}"


def tokens_sent(result):
    usage = result.usage
    return (
        usage["input_tokens"]
        + usage["cache_creation_input_tokens"]
        + usage["cache_read_input_tokens"]
    )


async def ask(question, tools, mcp_servers=None):
    options = ClaudeAgentOptions(
        model="haiku",
        system_prompt=system_prompt,
        tools=tools,
        mcp_servers=mcp_servers or {},
        allowed_tools=["mcp__orders__*"],
        setting_sources=[],
        strict_mcp_config=True,
        thinking={"type": "disabled"},
        max_turns=12,
    )
    run = {"calls": []}
    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    run["calls"].append(block.name)
                    print("the model asks :", describe(block))
        elif isinstance(message, ResultMessage):
            run["result"] = message
    print()
    print(run["result"].result)
    return run


print("ready to ask")
```

```{verify}
:id: ask-defined
:label: The function that runs the agent is defined
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed ask
callable(ask)
```

## A question the documents answer

The first question is one a member of staff might ask at the counter.
The answer is in one of the five files.

```{cell-insert}
:id: insert-documents
:path: {{ notebook }}
:tags: [documents]
:run: true
events_question = "What does a ticket for an author evening cost, and what happens to that money?"

documents = await ask(events_question, tools=["Glob", "Grep", "Read"])
```

Read the requests in order. The agent was not handed the right file.
It went looking: it listed the files or searched them for a likely
word, picked one from what came back, and read it. The answer is
written from the file.

This is how an agent built on the SDK gets at documents. Nothing
sorted the files ahead of time or picked out passages for it. The
model decides what to look for, sees what comes back, and decides
again, with the same loop it uses for everything else. It can follow
a pointer from one document to another, try a second word when the
first finds nothing, and read a whole file when a line is not enough.

The price is that whatever it reads becomes part of the conversation
and is sent with every request after. That is fine for five short
files. It is the thing to watch as the documents grow.

```{verify}
:id: answered-from-documents
:label: The agent found and read the document that holds the answer
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed documents
if "$9" not in documents["result"].result:
    print("The answer does not give the price from the file. Run the cell again.")
(
    any(name in documents["calls"] for name in ("Read", "Grep"))
    and "$9" in documents["result"].result
)
```
