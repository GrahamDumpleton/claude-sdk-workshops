---
title: A question it cannot answer
requires: [verify:no-tool-asked, quiz:what-has-to-change]
---

# A question it cannot answer

The first question needed nothing but what the model already knows.
This one does not. The workshop ships a file,
{open}`shop/opening-hours.md`, with the bookshop's hours in it, and
they are not hours anyone could guess.

The cell asks when the shop closes on Saturday, and tells the agent
where the file is. The options are the same ones as before, so the
agent still has no tools.

This time the cell does not keep every message. It gathers the blocks
of the model's replies, and keeps the result. Then it lists any block
that is a `ToolUseBlock`, which is what a request to use a tool looks
like.

```{cell-insert}
:id: insert-no-tools
:path: {{ notebook }}
:tags: [no-tools]
:run: true
question = (
    "What time does Tidewater Books close on Saturday? "
    "The opening hours are in the file shop/opening-hours.md."
)

blocks = []

async for message in query(prompt=question, options=options):
    if isinstance(message, AssistantMessage):
        blocks.extend(message.content)
    elif isinstance(message, ResultMessage):
        without_tools = message

asked_for = [block.name for block in blocks if isinstance(block, ToolUseBlock)]

print("tools asked for:", asked_for)
print(without_tools.result)
```

Read what it said. The model asked for no tool, because it was told of
none, and so it has no way to see the file. It can only tell you that,
or ask you for the contents. A model on its own is in this position
with every file, every database and everything that happened after it
was trained.

```{verify}
:id: no-tool-asked
:label: The model asked for no tool
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed no-tools
if asked_for:
    print("The model asked for", asked_for, "- the options should still say tools=[].")
asked_for == [] and without_tools.subtype == "success"
```

```{quiz}
:id: what-has-to-change
:title: What has to change
question: "The model could not answer. What has to change before it can?"
options:
  - text: "The prompt has to describe the file in more detail."
    explanation: "The prompt already named the file. However the model is asked, it has no way to open it."
  - text: "The agent has to be given a tool that reads files."
    correct: true
  - text: "The run has to be allowed more turns."
    explanation: "The run ended after one turn because the model had nothing it could ask for, not because it ran out of turns."
  - text: "A larger model has to be used."
    explanation: "A larger model reasons better, and it still only takes text and produces text. It cannot read a file either."
explanation: "A model produces text and nothing else. Reading a file is something the program around it has to do, and the program does it only when the model has been told the tool exists and asks for it."
```
