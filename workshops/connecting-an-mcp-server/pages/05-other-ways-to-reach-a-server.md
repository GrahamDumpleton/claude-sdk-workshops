---
title: Other ways to reach a server
requires: [verify:client-closed]
---

# Other ways to reach a server

The server here ran on your own machine and was reached over its
input and output. That is one of four kinds of entry `mcp_servers`
takes, and the `type` field says which.

| Type | Where the server runs | The entry gives |
| --- | --- | --- |
| `stdio` | A program the SDK starts on this machine | `command`, `args`, and `env` for its environment |
| `http` | Somewhere else, reached over the network | `url`, and `headers` for credentials |
| `sse` | Somewhere else, by an older way of streaming | `url` and `headers` |
| `sdk` | Inside your own program | What `create_sdk_mcp_server()` returns |

The two remote kinds are how the hosted servers of other companies are
reached, for an issue tracker or a document store. They need a server
to connect to and usually a credential to send, so this workshop names
them and stops there. The tool names, the approval and the status all
work as you have seen.

## What `strict_mcp_config` has been doing

Every agent in these workshops has set `strict_mcp_config=True`. Now
it can be explained. Servers do not only come from `mcp_servers`.
Depending on the other options, a session can also pick them up from a
`.mcp.json` file in the project and from your own Claude settings, and
under a Claude login it is given the connectors of that account, such
as mail and calendar, whatever the other options say.
`strict_mcp_config=True` shuts all of those out, so that the agent has
the servers your code names and no others. Without it, an agent you
run under your own login can arrive with tools you did not give it.

## Hang up

Disconnecting the client ends its session. The SDK then stops the
server it started.

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
