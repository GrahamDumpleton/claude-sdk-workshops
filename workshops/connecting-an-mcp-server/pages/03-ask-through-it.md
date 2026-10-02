---
title: Ask through it
requires: [verify:answered-through-server]
---

# Ask through it

To the model, a tool on a server looks like any other tool: a name, a
description and an input schema. The description is the docstring you
read in the server's source.

The client is still connected. This cell sends it a question and
prints each request the model makes and what the server sends back.

```{cell-insert}
:id: insert-asked
:path: {{ notebook }}
:tags: [asked]
:run: true
def text_of(content):
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content)
    return str(content)


calls = []

await client.query("How many copies of Tidewater do we have, and what is its stock code?")

async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                calls.append(block.name)
                print("the model asks   :", block.name, block.input)
    elif isinstance(message, UserMessage) and isinstance(message.content, list):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                print("the server says  :", text_of(block.content))
    elif isinstance(message, ResultMessage):
        answer = message

print()
print(answer.result)
```

The model asked for `mcp__stock__check_stock`. This time no function
of yours ran in the notebook. The request went to the other process,
the function there read the file, and its return value came back
across. It may arrive wrapped as data, `{"result": ...}`, which is how
this server library returns a value.

That is what the protocol buys. The lookup is written once, in a
program that can be tested and run on its own, and this notebook is
only one of the things that can use it. Register the same file with
Claude Code or the Claude desktop app and they get the same two
tools.

```{verify}
:id: answered-through-server
:label: The agent answered through the server's tool
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed asked
if "mcp__stock__check_stock" not in calls:
    print("The model did not ask for the server's tool. Run the cell again.")
elif "TW-4471-K" not in answer.result:
    print("The answer does not give the stock code from the file. Run the cell again.")
"mcp__stock__check_stock" in calls and "TW-4471-K" in answer.result
```

```{hint}
:title: Why the tools still needed approving
A tool that arrives from a server needs approval before it runs, like
a tool of your own, and for the same reason: the SDK cannot know what
it does. `allowed_tools=["mcp__stock__*"]` approved every tool of this
one server. Approve servers by name, and only the ones you have read
or have reason to trust. A server is a program running on your
machine with your access to it.
```
