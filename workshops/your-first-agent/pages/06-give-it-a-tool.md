---
title: Give it a tool
requires: [verify:file-was-read]
---

# Give it a tool

The SDK comes with tools built in, the ones Claude Code uses. `Read`
reads a file. One line of the options changes: `tools=["Read"]`.

The question is the same. The cell prints each step of the run as it
arrives, so there is more to look for than last time:

- when the model **asks**, in a `ToolUseBlock`, naming the tool and
  what it wants read;

- when the SDK **answers**, in a `ToolResultBlock`, with what the file
  holds;

- when the model **says** something, in a `TextBlock`.

```{cell-insert}
:id: insert-with-read
:path: {{ notebook }}
:tags: [with-read]
:run: true
with_read = ClaudeAgentOptions(
    model="haiku",
    system_prompt="You are the assistant for Tidewater Books, a small bookshop. Answer in one or two sentences.",
    tools=["Read"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=5,
)

tools_given = []
tool_calls = []

async for message in query(prompt=question, options=with_read):
    if isinstance(message, SystemMessage) and message.subtype == "init":
        tools_given = message.data["tools"]
        print("tools given     :", tools_given)
    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                tool_calls.append(block.name)
                print("the model asks  :", block.name, block.input)
            elif isinstance(block, TextBlock):
                print("the model says  :", block.text)
    elif isinstance(message, UserMessage) and isinstance(message.content, list):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                print("the SDK answers :", str(block.content)[:70], "...")
    elif isinstance(message, ResultMessage):
        with_tools = message

answer = with_tools.result

print("turns           :", with_tools.num_turns)
```

Read the run from the top. The model did not answer straight away. It
asked for the file. The SDK read it, on this machine, and sent the
contents back. Only then did the model answer, and the answer has the
closing time that is in the file.

Nothing about the model changed between the last page and this one. It
was told a tool existed, it asked for it, and the program around it did
the reading. That exchange is the loop, and it took two turns: one for
the model to ask, one for it to answer.

```{verify}
:id: file-was-read
:label: The agent read the file and answered from it
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed with-read
if "Read" not in tool_calls:
    print("The model did not ask for Read. Run the cell again.")
elif "4:40" not in answer and "16:40" not in answer:
    print("The answer does not give the Saturday closing time from the file. Run the cell again.")
tools_given == ["Read"] and "Read" in tool_calls and ("4:40" in answer or "16:40" in answer)
```

## The run as a picture

The step below opens a diagram of the run you just made: each request
and each reply, in order, between your code, the SDK, the model and the
file. Read it beside the cell's output, which is in the notebook's tab.

```{file-open}
:id: open-run
:title: Open the picture of the run
:path: diagrams/a-run-with-a-tool.md
:factory: Markdown Preview
```

```{hint}
:title: Why nobody was asked for permission
Reading a file inside the agent's working directory is allowed without
asking. Writing a file is not, and neither is reading one somewhere
else. **Decide what the agent can do**, later in these workshops, is
about where those lines are and how to move them.
```
