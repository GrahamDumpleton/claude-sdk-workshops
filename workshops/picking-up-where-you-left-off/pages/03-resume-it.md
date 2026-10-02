---
title: Resume it
requires: [verify:session-resumed]
---

# Resume it

A new run takes a session up again when it is given the session's id
in the `resume` option. The SDK loads the transcript, and the new
prompt becomes the next message of that conversation.

The cell is a fresh call to `query()`. It shares nothing with the
first run but the id: in a real program it could be running the next
day, after a restart. It copies the options with `resume` added and
asks for the stock code.

```{cell-insert}
:id: insert-resumed
:path: {{ notebook }}
:tags: [resumed]
:run: true
resume_options = replace(options, resume=first.session_id)

ask = "What is the stock code for the harbour atlas?"

async for message in query(prompt=ask, options=resume_options):
    if isinstance(message, ResultMessage):
        resumed = message

print(resumed.result)
print("session:", resumed.session_id)
print("same session as the first run:", resumed.session_id == first.session_id)
```

The agent gave the code, though this run never told it. The model was
sent the first exchange from the transcript, and then the question.
The result carries the first run's session id, because it is the same
session, one message longer than it was.

So the id is what a program has to keep. Store it beside whatever the
conversation belongs to, a user or a ticket or a job, and the
conversation can be taken up again from anywhere that can reach the
transcript.

```{verify}
:id: session-resumed
:label: The new run carried on the first session and knew the code
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed resumed
if resumed.session_id != first.session_id:
    print("The run was a new session. Check that the cell passes resume=first.session_id, and run it again.")
elif "TW-4471-K" not in (resumed.result or ""):
    print("The reply does not give the code. Run the cell again.")
resumed.session_id == first.session_id and "TW-4471-K" in (resumed.result or "")
```

```{hint}
:title: Resuming without an id
`continue_conversation=True` resumes the most recent session in the
working directory, with no id given. It suits a program that only ever
has one conversation going. With more than one, keep the ids.
```
