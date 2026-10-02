---
title: The reply and the result
requires: [verify:result-read]
---

# The reply and the result

## The reply

An `AssistantMessage` is what the model produced. Its `content` is a
list of blocks, because a reply can hold more than one kind of thing.
Here there is one kind, a `TextBlock`, which holds the words.

```{cell-insert}
:id: insert-reply
:path: {{ notebook }}
:tags: [reply]
:run: true
texts = []

for message in messages:
    if isinstance(message, AssistantMessage):
        for block in message.content:
            print("block:", type(block).__name__)
            if isinstance(block, TextBlock):
                texts.append(block.text)

reply = "\n".join(texts)

print(reply)
```

That is the answer to the question. What it says differs from run to
run: ask a model the same thing twice and it words the reply
differently.

## The result

The last message is the SDK's report on the whole run.

```{cell-insert}
:id: insert-result
:path: {{ notebook }}
:tags: [result]
:run: true
result = next(message for message in messages if isinstance(message, ResultMessage))

print("subtype :", result.subtype)
print("turns   :", result.num_turns)
print("result  :", result.result)
```

- **subtype** says how the run ended. `success` means the agent
  finished the job.

- **turns** counts the times the model was asked to respond. One was
  enough here.

- **result** is the final answer as plain text, the same words the
  text block held.

A program that only wants the answer reads `result.result` and ignores
everything else. A program that wants to show what the agent is doing
as it goes reads the messages before it.

```{verify}
:id: result-read
:label: The run succeeded and returned an answer
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed result
if result.subtype != "success":
    print("The run ended with", result.subtype, "- go back and run the first question again.")
result.subtype == "success" and bool(reply) and bool(result.result)
```
