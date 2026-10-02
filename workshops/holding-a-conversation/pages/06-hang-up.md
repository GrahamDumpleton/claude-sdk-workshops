---
title: Hang up
requires: [verify:client-closed]
---

# Hang up

A connected client is a running process, and it stays running until it
is told to stop. `disconnect()` ends the session and shuts the process
down.

```{cell-insert}
:id: insert-disconnect
:path: {{ notebook }}
:tags: [disconnect]
:run: true
await client.disconnect()

connected = False

print("connected:", connected)
```

The conversation is over, and this client cannot be sent anything
more.

In a program, a client is usually written with `async with`, which
connects on the way in and disconnects on the way out, whatever
happens in between:

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("...")
    async for message in client.receive_response():
        ...
```

A notebook spreads one conversation over several cells, so this
workshop connected and disconnected by hand.

```{verify}
:id: client-closed
:label: The client was disconnected
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed disconnect
connected is False
```

## Which to use

- `query()` for a job with a beginning and an end: one prompt, one
  result. A script, a scheduled task, a step in a larger program.

- `ClaudeSDKClient` for anything with a second message: a chat, or a
  job where your program reads the reply before deciding what to say
  next.
