---
title: What you know now
requires: [quiz:where-the-tool-runs]
---

# What you know now

An agent can call a function you wrote.

- `@tool(name, description, input_schema)` turns an `async` function
  into a tool. The function is given the input as a dictionary and
  returns a list of content blocks.

- `create_sdk_mcp_server()` gathers tools into a server, and
  `mcp_servers={"shop": server}` hands it to the agent. A tool is then
  called `mcp__shop__<tool>`.

- The tool runs in your own program. `tools=[]` does not remove it,
  and it needs approving with `allowed_tools` before it will run.

- The name, the description and the input schema are all the model is
  shown. Say what the tool does, what it returns and what it cannot
  do.

- `ToolAnnotations(readOnlyHint=True)` tells the SDK a tool changes
  nothing, so that several calls to it can run at once.

```{quiz}
:id: where-the-tool-runs
:title: Where the tool runs
question: "The agent calls `mcp__shop__check_stock`. Where does the code of `check_stock` run?"
options:
  - text: "On Anthropic's servers, next to the model."
    explanation: "The model only ever produces the request. It runs nothing, and your function is never sent to it."
  - text: "In your own Python process, the one that called `query()`."
    correct: true
  - text: "In a separate process the SDK starts for each tool."
    explanation: "That is how the server in the next workshop runs. A server made with `create_sdk_mcp_server()` runs inside your program."
  - text: "Inside the model, which was shown the function."
    explanation: "The model is shown the name, the description and the input schema, never the function."
explanation: "A tool made with `@tool` is a function in your own program. The model asks, the SDK passes the request to your function, and the result goes back as text."
```

## What comes next

The server in this workshop lived inside the notebook. **Connect an
MCP server** runs the same stock lookup as a program of its own, which
any agent can use, and says what the letters in `mcp__shop__` stand
for.

Press Finish below to end the workshop.
