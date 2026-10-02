---
title: A run that ends
requires: [verify:session-kept]
---

# A run that ends

First, a conversation worth coming back to. The cell tells the agent a
fact that is in no file and could not be guessed, a stock code for a
book, with a single call to `query()`. When the cell finishes, the run
is over and the process that held the session has gone.

```{cell-insert}
:id: insert-first
:path: {{ notebook }}
:tags: [first]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "Answer in one sentence."
    ),
    tools=[],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=3,
)

tell = "The stock code for the harbour atlas is TW-4471-K. Say that you have noted it."

async for message in query(prompt=tell, options=options):
    if isinstance(message, ResultMessage):
        first = message

print(first.result)
print("session:", first.session_id)
```

## Where it went

As a session runs, the SDK writes every message of it to a file, called
a transcript. Transcripts are kept in Claude Code's own configuration
directory, under your home directory, filed by the directory the agent
was working in. Every run you have made in these workshops left one.

`list_sessions()` reads those files. Given a directory, it returns the
sessions that were run there. The agent's working directory is this
notebook's, so the cell asks about that.

This cell calls nothing. It reads what is on disk.

```{cell-insert}
:id: insert-listed
:path: {{ notebook }}
:tags: [listed]
:run: true
here = str(Path.cwd())

kept = {session.session_id: session for session in list_sessions(directory=here)}

ours = kept.get(first.session_id)

print("sessions kept for this directory:", len(kept))

if ours is None:
    print("the session just made is not among them")
else:
    print("id           :", ours.session_id)
    print("summary      :", ours.summary)
    print("first prompt :", ours.first_prompt)
```

The session is there, under the id the result gave. The summary is a
title for the conversation, there so that a list of sessions can be
shown to a person.

`get_session_messages()` reads the conversation itself back.

```{cell-insert}
:id: insert-transcript
:path: {{ notebook }}
:tags: [transcript]
:run: true
transcript = get_session_messages(first.session_id, directory=here)

for entry in transcript:
    content = entry.message["content"]
    if isinstance(content, list):
        content = " ".join(block.get("text", "") for block in content)
    print(entry.type, ":", content)
```

Both sides of the exchange are there: what you said and what the
agent replied. That is the whole of what a session is. Anything that
can send those messages to the model again can carry the conversation
on.

```{verify}
:id: session-kept
:label: The session was kept and could be read back
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed transcript
if ours is None:
    print("The session was not found on disk. Run the three cells on this page again, in order.")
ours is not None and len(transcript) >= 2
```
