---
title: What was kept
requires: [verify:code-survived, verify:client-closed]
---

# What was kept

A summary is shorter than what it summarises, so something has been
left out. The way to find out what is to ask.

The next turn asks for two things. One is the stock code you gave the
agent in your first message, which is in no file. The other is a
detail from the terms of one supplier, a file the agent read near the
start: what Saltmarsh Editions charges for carriage. The answer to
that is in {open}`suppliers/saltmarsh-editions.md`.

```{cell-insert}
:id: insert-kept
:path: {{ notebook }}
:tags: [kept]
:run: true
kept = await turn(
    "What is the stock code I gave you, and what does Saltmarsh Editions charge for carriage?"
)
```

The stock code came back. Compaction is built to keep what the user
said, and the summary carries your messages nearly word for word.

The carriage charge is another matter. It was never asked about
before, so the summary had no reason to mention it, and the file it
was in is unlikely to be one of the few that were put back. Look at
what the agent did. It may have said it does not have that detail, or
it may have made a tool request and read the file again. If it did
either, the detail was no longer in what the model was sent.

That is the trade compaction makes:

- **Kept**: what you asked for, what was decided, what was found out
  and said aloud, and a note of which files were read.

- **At risk**: anything that was only ever in a tool result, and any
  instruction given once, early on, in passing.

Two things follow for the way you build an agent. A rule that must
hold for the whole of a long session does not belong in the first
prompt. It belongs in the system prompt, or in a `CLAUDE.md` loaded
with `setting_sources`, both of which are sent in full with every
request and are never summarised. And an agent that can go back to
the source, with a tool that reads the file or runs the query again,
loses little when a detail drops out of its conversation.

```{verify}
:id: code-survived
:label: What you told the agent survived the compaction
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed kept
if "TW-4471-K" not in kept.result:
    print("The reply does not give the stock code. Run the cell again.")
"TW-4471-K" in kept.result
```

## Hang up

That is all this session is needed for. The last part of the workshop
uses agents of its own.

```{cell-insert}
:id: insert-disconnect
:path: {{ notebook }}
:tags: [disconnect]
:run: true
await client.disconnect()

connected = False

print("connected:", connected)
```

```{verify}
:id: client-closed
:label: The client was disconnected
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed disconnect
connected is False
```

```{hint}
:title: Having a say in what is kept
The model writes the summary under instructions from the SDK, and you
can add to them. Text after the command, as in `/compact keep every
price that was quoted`, is passed on as an instruction for the
summary. A
`PreCompact` hook is called just before a compaction of either kind,
which is the moment to save the full transcript if you need it.
```
