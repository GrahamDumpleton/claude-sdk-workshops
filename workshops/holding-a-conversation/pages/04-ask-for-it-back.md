---
title: Ask for it back
requires: [verify:code-remembered]
---

# Ask for it back

The same question that failed before, sent to the client that was
told the code a moment ago.

```{cell-insert}
:id: insert-turn-two
:path: {{ notebook }}
:tags: [turn-two]
:run: true
await client.query(ask)

async for message in client.receive_response():
    if isinstance(message, ResultMessage):
        turn_two = message

print(turn_two.result)
print("session:", turn_two.session_id)
print("same session as turn one:", turn_two.session_id == turn_one.session_id)
```

This time it knows, and the two turns report one session id.

The model has not changed and has not started remembering. What
changed is what it was sent. The session keeps everything said in it:
your first prompt, the model's reply, your second prompt. When the
second prompt went in, the model was sent all three, and answered the
last by reading the first. Each turn in a conversation is the whole
conversation so far, sent again, with one more message on the end.

That is all a conversation with a model is, in a chat application as
much as here.

```{verify}
:id: code-remembered
:label: The second turn was on the same session and gave the code
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed turn-two
if turn_two.session_id != turn_one.session_id:
    print("The two turns were on different sessions. Run the cells from the one that connects the client again, in order.")
elif "TW-4471-K" not in (turn_two.result or ""):
    print("The reply does not give the code. Run the cell that tells the client the code, then this one.")
turn_two.session_id == turn_one.session_id and "TW-4471-K" in (turn_two.result or "")
```
