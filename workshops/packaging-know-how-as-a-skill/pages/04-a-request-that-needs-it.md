---
title: A request that needs it
requires: [verify:ask-defined, quiz:how-the-body-arrives, verify:skill-used]
---

# A request that needs it

Two requests are put to the agent, one that the skill fits and one
that it does not, so the first cell defines a function for the run.
`ask()` prints each step and keeps the tools the model asked for and
the size of the first and the last request the model was sent. It
calls nothing yet.

```{cell-insert}
:id: insert-ask
:path: {{ notebook }}
:tags: [ask]
:run: true
def tokens_sent(message):
    usage = message.usage
    return (
        usage["input_tokens"]
        + usage["cache_creation_input_tokens"]
        + usage["cache_read_input_tokens"]
    )


async def ask(request):
    run = {"calls": [], "requests": []}
    async for message in query(prompt=request, options=options):
        if isinstance(message, AssistantMessage):
            run["requests"].append(tokens_sent(message))
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    run["calls"].append(block.name)
                    print("the model asks      :", block.name, block.input)
        elif isinstance(message, UserMessage) and isinstance(message.content, list):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print("the SDK sends text  :", len(block.text.split()), "words, beginning")
                    print("                     ", block.text[:70].replace("\n", " "))
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

## A refund comes up

The request says nothing about a skill, a procedure or a reference.
It is what a member of staff would type.

```{quiz}
:id: how-the-body-arrives
:title: How the body arrives
question: "The model has seen the skill's description and nothing more. How does it get the steps?"
options:
  - text: "It cannot. The steps have to be put in the system prompt."
    explanation: "That would send them with every request, which is what a skill avoids."
  - text: "It asks for the `Skill` tool by name, and the SDK sends the body back into the conversation."
    correct: true
  - text: "The SDK notices the word refund in the request and adds the body before sending it."
    explanation: "The SDK does not read the request. The model decides, from the description, and asks."
  - text: "The model opens `SKILL.md` with `Read`."
    explanation: "It could read the file if it knew the path, but that is not how a skill is loaded. There is a tool for it."
explanation: "Loading a skill is a tool call like any other. The model asks for `Skill`, and the body comes back as more to read."
```

```{cell-insert}
:id: insert-refund
:path: {{ notebook }}
:tags: [refund]
:run: true
refund = await ask(
    "A customer bought a paperback 20 days ago, has the receipt, and wants "
    "her money back. Write the reply to send her."
)
```

Follow the steps. The model asked for `Skill` and named
`refund-reply`. The SDK then sent text into the conversation: that is
the body of the skill, arriving now and not before. From there the
agent did what the body says. It read the returns policy, as the first
step told it to, and wrote a reply to the pattern.

The reply carries a returns desk reference. That line is in the body
of the skill and nowhere else, so the model could only have written it
after the body was loaded.

```{verify}
:id: skill-used
:label: The agent loaded the skill and followed it
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed refund
if "Skill" not in refund["calls"]:
    print("The model did not ask for the skill. Run the cell again.")
elif "RF-3318-Q" not in refund["result"].result:
    print("The reply does not carry the reference the skill asks for. Run the cell again.")
"Skill" in refund["calls"] and "RF-3318-Q" in refund["result"].result
```
