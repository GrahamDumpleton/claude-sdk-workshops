---
title: Fill it
requires: [verify:window-filled, verify:sent-again]
---

# Fill it

Now give the session something to carry. The first turn tells the
agent a stock code that is in no file, and then has it read all ten of
the suppliers' terms to answer one small question.

`turn()` sends a prompt on the open client, counts the tool requests,
and prints the reply and how many tokens the model was sent over the
turn. This run is slower than most, since there are ten files to read.

```{cell-insert}
:id: insert-fill
:path: {{ notebook }}
:tags: [fill]
:run: true
def tokens_sent(result):
    usage = result.usage
    return (
        usage["input_tokens"]
        + usage["cache_creation_input_tokens"]
        + usage["cache_read_input_tokens"]
    )


async def turn(prompt):
    requests = 0
    await client.query(prompt)
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            requests += sum(isinstance(block, ToolUseBlock) for block in message.content)
        elif isinstance(message, ResultMessage):
            result = message
    print("tool requests :", requests)
    print("it was sent   :", tokens_sent(result), "tokens over the turn")
    print()
    print(result.result)
    print()
    return result


reading = await turn(
    "The stock code for our signed copy of Tidewater is TW-4471-K. Remember it. "
    "Then read every file in the suppliers directory and tell me which supplier "
    "has the smallest minimum order."
)

context = await snapshot("after the reading")
```

Compare the two rows of the table. The conversation has gone from
almost nothing to thousands of tokens, and nearly all of it is in the
tool results column: the text of ten files. The answer was one
sentence. The files it was drawn from are now part of the session.

```{verify}
:id: window-filled
:label: The reading filled the conversation with tool results
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed fill
if history[-1]["tool results"] < 2000:
    print("The agent did not read the files. Run this page's cell again.")
reading.subtype == "success" and history[-1]["tool results"] > 2000
```

## What a small question now costs

The next question is five words long and needs no tools. The agent
can answer it from what it has already read.

```{cell-insert}
:id: insert-follow-up
:path: {{ notebook }}
:tags: [follow-up]
:run: true
follow_up = await turn("Which supplier delivers fastest?")

context = await snapshot("after one more question")
```

Look at how much the model was sent for that turn. The question was a
few tokens. The request that carried it held the whole session: the
tools, the first prompt, ten files and the first answer. The table
has barely moved, because a short question and a short answer add
little. What it shows is that the reading is paid for again on every
turn from now on.

Sending the same text again is made cheaper by a cache: the part of a
request that repeats the one before is read back at a fraction of the
price. That softens the cost. It does not free any room, and a
session that keeps reading keeps growing.

```{verify}
:id: sent-again
:label: The short question was sent with the whole conversation
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed follow-up
follow_up.subtype == "success" and tokens_sent(follow_up) > history[1]["conversation"]
```
