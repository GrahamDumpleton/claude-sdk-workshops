---
title: A server that does not start
requires: [quiz:when-a-server-fails, verify:failure-reported]
---

# A server that does not start

A server is a separate program, and separate programs fail to start.
The file was moved, a package is missing, a password is wrong. What
your program sees when that happens is worth knowing before it
happens.

The next cell connects a second client. Its options are the first
client's with one more server added, `orders`, whose entry names a
file that does not exist.

```{quiz}
:id: when-a-server-fails
:title: When a server fails
question: "One of two servers cannot be started. What happens when the client connects?"
options:
  - text: "`connect()` raises an exception naming the server."
    explanation: "Connecting does not raise for a server that fails. The session starts without it."
  - text: "The session starts with the tools of the server that works, and the other is reported as failed."
    correct: true
  - text: "The session waits until the missing server appears."
    explanation: "A server that cannot be started is given up on, and the session goes ahead."
  - text: "Neither server is connected, since the configuration is wrong."
    explanation: "Each server is started on its own. One failing does not stop another."
explanation: "A server that fails does not stop the session and raises nothing. The agent simply has fewer tools, and the status is where it shows."
```

```{cell-insert}
:id: insert-broken
:path: {{ notebook }}
:tags: [broken]
:run: true
orders_entry = {
    "type": "stdio",
    "command": sys.executable,
    "args": ["orders_server.py"],
}

second = ClaudeSDKClient(
    options=replace(options, mcp_servers={"stock": stock_entry, "orders": orders_entry})
)

await second.connect()

good = await server_status(second, "stock")
bad = await server_status(second, "orders")

await second.disconnect()

for entry in (good, bad):
    print(entry["name"], ":", entry["status"], "-", entry.get("error", "no error"))
```

Nothing was raised. The session started, the `stock` server connected
as before, and `orders` is `failed`, with a short reason beside it.

An agent in that state does not know a server is missing. It has the
tools it was given and no others, and asked about an order it would
say that it cannot help, or try to answer some other way. So a
program that depends on a server checks for itself. `get_mcp_status()`
is one place to look. The `init` message that opens every run is
another: its `mcp_servers` entry lists each server with its status.

The statuses a server can report are `connected`, `failed`, `pending`
while it is still starting, `needs-auth` when it wants credentials it
was not given, and `disabled`.

```{verify}
:id: failure-reported
:label: The failed server was reported and the other still connected
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed broken
if bad["status"] != "failed":
    print("The orders server's status is", bad["status"], "- run the cell again.")
good["status"] == "connected" and bad["status"] == "failed"
```
