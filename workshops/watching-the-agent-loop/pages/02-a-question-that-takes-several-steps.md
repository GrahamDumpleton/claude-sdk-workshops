---
title: A question that takes several steps
requires: [verify:loop-ran]
---

# A question that takes several steps

The workshop ships four of the bookshop's documents, in the `shop`
directory: {open}`shop/opening-hours.md`, {open}`shop/returns-policy.md`,
{open}`shop/staff-handbook.md` and {open}`shop/events.md`.

The agent is not told which one to read. It is given three tools to
find out with, all of them built into the SDK and none of them able to
change anything:

- `Glob` lists the files whose names match a pattern.

- `Grep` searches inside files for a piece of text.

- `Read` reads one file.

The question is one a member of staff might ask, and no single file
answers all of it. The cell prints each step of the run as it arrives:
when the model **asks** for a tool, when the SDK **answers** with what
the tool found, and when the model **says** something.

The run takes several steps, so it takes longer than the login check
did.

```{cell-insert}
:id: insert-run
:path: {{ notebook }}
:tags: [run]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "The shop's documents are in the shop directory. Find the answer in them "
        "before you reply, and answer in two or three sentences."
    ),
    tools=["Glob", "Grep", "Read"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=12,
)

question = (
    "A customer is returning a book and has no receipt. "
    "What do I have to do, and when do I need the manager?"
)

messages = []
requests = []
answers = []

async for message in query(prompt=question, options=options):
    messages.append(message)
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                requests.append(block)
                print("the model asks  :", block.name, block.input)
            elif isinstance(block, TextBlock):
                print("the model says  :", block.text)
    elif isinstance(message, UserMessage) and isinstance(message.content, list):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                answers.append(block)
                print("the SDK answers :", str(block.content)[:70], "...")
    elif isinstance(message, ResultMessage):
        result = message
        print("the run ends    :", message.subtype)

tool_calls = [block.name for block in requests]
```

Read the output from the top. The model did not answer the question
when it was first asked. It asked for something, and then for
something else, and each time the SDK answered. Only at the end did it
say something with no request beside it, and that was the answer.

Which tools it asked for, and in what order, was the model's choice.
Run the cell again and it may go about it differently. The rest of the
workshop takes this one run apart, using the messages the cell kept.

```{verify}
:id: loop-ran
:label: The agent used its tools and finished
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed run
if "Read" not in tool_calls:
    print("The model answered without reading a file. Run the cell again.")
elif result.subtype != "success":
    print("The run ended with", result.subtype, "- run the cell again.")
"Read" in tool_calls and result.subtype == "success"
```

```{hint}
:title: Why the model says things before it asks
Between requests the model often writes a line about what it is going
to do next. That text is part of the same reply as the request that
follows it. It is not an answer, and the loop carries on.
```
