---
title: Compact it
requires: [quiz:what-compaction-does, verify:session-compacted]
---

# Compact it

When a conversation has to be made smaller, the SDK compacts it. It
asks the model to write a summary of everything so far, and then
replaces the history with that summary. The session carries on with
the summary standing in for what was said.

The SDK does this by itself when the window is nearly full, at the
figure the first cell printed. That is a long way off here, and
filling a window to find out would be a costly experiment. It can
also be asked for at any time, by sending `/compact` as a prompt.
`/compact` is a command to the SDK, not a message to the model: it is
not answered, it is carried out.

```{quiz}
:id: what-compaction-does
:title: What compaction does
question: "The conversation holds the text of ten files. After `/compact`, what has happened to them?"
options:
  - text: "Nothing. Compaction only shortens the model's replies."
    explanation: "It replaces the whole history, tool results included, since they are the bulk of it."
  - text: "They are gone from the conversation, replaced by a summary the model wrote of what it had learned."
    correct: true
  - text: "They are deleted from disk."
    explanation: "Compaction changes the conversation and nothing else. The files are where they were."
  - text: "They are moved into the system prompt, where they are safe."
    explanation: "The system prompt is not touched, and moving them would free no room."
explanation: "A summary takes the place of the history. What the summary says, the agent still knows. What it leaves out is no longer in front of the model."
```

The cell sends the command and picks two things out of what comes
back: a system message of subtype `compact_boundary`, which marks the
place and says how big the conversation was before and after, and
the summary itself, which arrives as a message in the user's role.
It takes longer than a turn, since the model has a summary to write.

```{cell-insert}
:id: insert-compact
:path: {{ notebook }}
:tags: [compact]
:run: true
def text_from(content):
    if isinstance(content, str):
        return content
    return " ".join(block.text for block in content if isinstance(block, TextBlock))


boundary = None
summary = None

await client.query("/compact")

async for message in client.receive_response():
    if isinstance(message, SystemMessage) and message.subtype == "compact_boundary":
        boundary = message.data["compact_metadata"]
    elif isinstance(message, UserMessage) and summary is None:
        summary = text_from(message.content)

if boundary is None:
    print("no compaction took place")
else:
    print("asked for by      :", boundary["trigger"])
    print("tokens before     :", boundary["pre_tokens"])
    print("tokens after      :", boundary["post_tokens"])
    print()
    print((summary or "")[:1200])
    print("...")
    print()

context = await snapshot("after compaction")
```

The boundary says the compaction was asked for by hand, and gives the
size of the conversation on each side of it. Under that is the start
of the summary: an account, written by the model, of what was asked,
what was read and what was found.

Now the table. The tool results column has gone to nothing. The files
are no longer in the conversation as the results of tool requests. In
their place are the summary and, as a convenience, the few files that
were read most recently, which the SDK puts back whole so that the
agent does not have to read them again at once. That is why the
conversation has shrunk by a part and not to nothing. In a session
with a hundred thousand tokens of history, the same few files would
be a small part of what was left.

```{verify}
:id: session-compacted
:label: The conversation was compacted and a summary took its place
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed compact
if boundary is None:
    print("No compact_boundary message arrived. Run the cells of the last page, then this one again.")
(
    boundary is not None
    and boundary["post_tokens"] < boundary["pre_tokens"]
    and bool(summary)
    and history[-1]["tool results"] < history[-2]["tool results"]
)
```
