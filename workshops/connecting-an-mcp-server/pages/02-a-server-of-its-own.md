---
title: A server of its own
requires: [verify:server-connected]
---

# A server of its own

Read {open}`stock_server.py` before running anything. It is short.

- It makes a server, with a name of its own.

- It defines two ordinary functions and registers each as a tool with
  `@server.tool()`. The function's name becomes the tool's name, its
  docstring becomes the description, and its parameters become the
  input schema.

- When run as a program, it calls `server.run()`, which waits for
  requests on its standard input and writes answers to its standard
  output.

Nothing in it mentions Claude. It is written with the `mcp` package,
the Python library for the protocol, which is installed with the SDK.

The step below opens a picture of where this program sits when an
agent uses it.

```{file-open}
:id: open-pieces
:title: Open the picture of where a tool runs
:path: diagrams/where-a-tool-runs.md
:factory: Markdown Preview
```

## Tell the SDK how to start it

A server that is a program is described to the SDK by the command that
starts it. The entry below says: this is a `stdio` server, start it by
running `stock_server.py` with the Python this notebook is using.
`stdio` is short for standard input and output, the two streams the
SDK will talk to it over.

The entry goes in `mcp_servers` under a name, here `stock`, and the
name becomes part of each tool's name, as it did before:
`mcp__stock__check_stock`.

The cell connects a `ClaudeSDKClient`, which starts the session and
keeps it open across cells. Connecting starts the server. Then it asks
the client how its servers are, with `get_mcp_status()`. No model is
called.

```{cell-insert}
:id: insert-connect
:path: {{ notebook }}
:tags: [connect]
:run: true
stock_entry = {
    "type": "stdio",
    "command": sys.executable,
    "args": ["stock_server.py"],
}

options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "Answer in one or two sentences, from what your tools tell you and nothing else."
    ),
    tools=[],
    mcp_servers={"stock": stock_entry},
    allowed_tools=["mcp__stock__*"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=8,
)


async def server_status(client, name):
    for _ in range(50):
        status = await client.get_mcp_status()
        entry = next(server for server in status["mcpServers"] if server["name"] == name)
        if entry["status"] != "pending":
            break
        await asyncio.sleep(0.2)
    return entry


client = ClaudeSDKClient(options=options)

await client.connect()

connected = True

stock = await server_status(client, "stock")
stock_tools = [entry["name"] for entry in stock.get("tools", [])]

print("server :", stock["name"])
print("status :", stock["status"])
print("it says:", stock.get("serverInfo"))
print("tools  :", stock_tools)
```

The status is `connected`, and the server has introduced itself by the
name it gave in its own source, `tidewater-stock`. The tools are the
two functions in the file. The SDK did not need to be told what they
were: it asked the server, which is part of what the protocol is for.

A server can take a moment to start, and until it has, its status is
`pending`. `server_status()` asks again until the answer is something
else.

```{verify}
:id: server-connected
:label: The server started and offered its tools
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed connect
if stock["status"] != "connected":
    print("The server's status is", stock["status"], "- open the hint below.")
stock["status"] == "connected" and "check_stock" in stock_tools
```

```{hint}
:title: If the status is failed
The server is run with the same Python as this notebook, and needs the
`mcp` package, which the SDK installs. If the status is `failed`,
print `stock.get("error")` in a new cell to see what the server said,
and check that `stock_server.py` is in the workshop's folder of files.
Then run the cell again: it connects a new client.
```
