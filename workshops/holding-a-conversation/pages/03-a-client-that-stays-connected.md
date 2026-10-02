---
title: A client that stays connected
requires: [verify:first-turn-done]
---

# A client that stays connected

Underneath, the SDK runs Claude Code as a separate process. `query()`
starts that process, runs one exchange and shuts it down. A
`ClaudeSDKClient` starts it and leaves it running, with one session
open inside it, until you say otherwise. While it is open you can send
it one prompt after another.

Connecting calls nothing yet. It takes the same options as before.

```{cell-insert}
:id: insert-connect
:path: {{ notebook }}
:tags: [connect]
:run: true
client = ClaudeSDKClient(options=options)

await client.connect()

connected = True

print("connected:", connected)
```

A client splits into two steps what `query()` did in one:

- `await client.query(prompt)` sends a prompt and returns at once.

- `client.receive_response()` hands back the messages of the reply, up
  to and including the `ResultMessage` that ends it.

The client lives in the notebook's kernel, so it is still connected
when the next cell runs. The first turn tells it the stock code.

```{cell-insert}
:id: insert-turn-one
:path: {{ notebook }}
:tags: [turn-one]
:run: true
await client.query(tell)

async for message in client.receive_response():
    if isinstance(message, ResultMessage):
        turn_one = message

print(turn_one.result)
print("session:", turn_one.session_id)
```

So far this looks the same as the first cell of the workshop: the
agent was told the code and said so. The difference is that this time
the session did not end. It is still open, waiting for the next thing
you say.

```{verify}
:id: first-turn-done
:label: The client is connected and took the first turn
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed turn-one
if turn_one.subtype != "success":
    print("The turn ended with", turn_one.subtype, "- run the cell again.")
connected and turn_one.subtype == "success"
```

```{hint}
:title: If a cell says the client is not connected
The client was lost, most likely because the kernel was restarted.
Run the cell that connects it again, then carry on from the cell after
it.
```
