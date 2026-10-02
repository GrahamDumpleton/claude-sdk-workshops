---
title: A prompt of your own
requires: [verify:first-answered]
---

# A prompt of your own

The agent in this workshop answers customers of the bookshop from one
document, {open}`shop/returns-policy.md`. A customer asks two things
at once. The policy covers the first. It says nothing about the second,
and what the agent does then is up to its instructions.

## One question, asked three times

The same question is going to be asked under three system prompts, so
the first cell defines the question and a function that asks it. The
function takes a system prompt, runs the agent and returns two things:
the result, and the number of tokens in the first request the model
was sent. A token is a piece of text about the size of a short word,
and the count is used at the end of the workshop.

This cell calls nothing yet.

```{cell-insert}
:id: insert-ask
:path: {{ notebook }}
:tags: [ask]
:run: true
question = (
    "I bought a book here last month and I've lost the receipt. "
    "Can I bring it back? And do you buy second-hand books?"
)


async def ask(system_prompt):
    options = ClaudeAgentOptions(
        model="haiku",
        system_prompt=system_prompt,
        tools=["Read"],
        setting_sources=[],
        strict_mcp_config=True,
        thinking={"type": "disabled"},
        max_turns=6,
    )
    first_request = None
    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage) and first_request is None:
            usage = message.usage or {}
            first_request = (
                usage.get("input_tokens", 0)
                + usage.get("cache_creation_input_tokens", 0)
                + usage.get("cache_read_input_tokens", 0)
            )
        elif isinstance(message, ResultMessage):
            result = message
    return result, first_request


print("ready to ask:", question)
```

## The first prompt

A system prompt for an agent with a job of its own says four things:
who the agent is, what it may draw on, what to do when that is not
enough, and how to answer. This one says each in a sentence.

```{cell-insert}
:id: insert-first
:path: {{ notebook }}
:tags: [first]
:run: true
shop_prompt = (
    "You are the assistant for Tidewater Books, a small bookshop. "
    "Answer customers from the returns policy in shop/returns-policy.md and from nothing else. "
    "If the policy does not cover a question, say that you do not know. "
    "Answer in two or three sentences."
)

first, first_size = await ask(shop_prompt)

print(first.result)
```

Read the reply against the prompt. The agent answered the first half
of the question from the policy, which it had to read to do. Look at
what it did with the second half, about second-hand books, which the
policy does not mention. The third sentence of the prompt told it what
to do there.

None of that was in the customer's question. It came from the
instructions, which the customer never sees.

```{verify}
:id: first-answered
:label: The agent answered under your prompt
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed first
if first.subtype != "success":
    print("The run ended with", first.subtype, "- run the cell again.")
first.subtype == "success" and first_size > 0
```
