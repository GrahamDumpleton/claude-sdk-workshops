---
title: Welcome
requires: [verify:sdk-ready, verify:login-works]
---

# Run your first agent

A language model does one thing: it takes text and produces text. It
cannot open a file, run a command or look anything up, and it remembers
nothing from one request to the next.

An agent is a program wrapped around a model. The program tells the
model which tools exist. The model replies with an answer, or with a
request to use a tool. The program carries out the request and sends
back what it found, and that goes round until the model has an answer.
The model decides, and the program does.

The Claude Agent SDK is that program as a Python library. It is the
same loop and the same tools as Claude Code, the coding assistant,
driven from your own code.

The step below opens a picture of those pieces and what passes
between them. It opens as a tab in the main area, where there is room
for it, and stays there for you to come back to.

```{file-open}
:id: open-pieces
:title: Open the picture of the pieces
:path: diagrams/the-pieces-of-an-agent.md
:factory: Markdown Preview
```

This workshop runs an agent, takes apart the messages that come back,
then asks a question the model cannot answer on its own and gives it
the one tool that changes that.

## What it runs on

The SDK calls the model with the Claude login on this machine, the one
the `claude` command uses. Every run counts against that plan's usage,
as a message in the Claude app does. This workshop makes four small
runs on the smallest model.

```{when} "claude" in missing_tools
The `claude` command was not found. The SDK carries its own copy of
Claude Code, so the workshop still works if this machine has logged in
before. If the login check further down fails, install
[Claude Code](https://code.claude.com/docs/en/setup), run `claude` in a
terminal and log in.
```

## The notebook

The step below creates the notebook. Its first cell imports what the
workshop uses from the SDK.

```{notebook-create}
:id: create-notebook
:path: {{ notebook }}
:open: true
- markdown: |
    # Run your first agent
    Each step of the workshop adds a cell below.
- code: |
    import claude_agent_sdk
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ResultMessage,
        SystemMessage,
        TextBlock,
        ToolResultBlock,
        ToolUseBlock,
        UserMessage,
        query,
    )

    sdk_version = claude_agent_sdk.__version__
    print("claude-agent-sdk:", sdk_version)
  tags: [setup]
```

```{cell-run}
:id: run-setup
:path: {{ notebook }}
:cell: setup
```

The cell prints the version of the SDK this JupyterLab has installed.

```{verify}
:id: sdk-ready
:label: The SDK is importable
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: after:run-setup; cell-executed setup
bool(sdk_version)
```

## Check the login

Before anything else, make sure the SDK can reach the model. The cell
below asks the agent for one word. It takes a few seconds, as every
cell that calls the model does: the wait is the model working.

Do not read the code closely yet. The next page writes the same call
out and explains each part.

```{cell-insert}
:id: insert-login
:path: {{ notebook }}
:tags: [login]
:run: true
ready = False

try:
    async for message in query(
        prompt="Reply with the single word: ready",
        options=ClaudeAgentOptions(
            model="haiku",
            system_prompt="Reply with one word.",
            tools=[],
            setting_sources=[],
            strict_mcp_config=True,
            thinking={"type": "disabled"},
            max_turns=1,
        ),
    ):
        if isinstance(message, ResultMessage):
            ready = not message.is_error
            print("the model replied:", message.result)
except Exception as error:
    print("the run failed:", error)

print("ready:", ready)
```

The last line prints `ready: True` when the model answered.

```{verify}
:id: login-works
:label: The SDK can reach the model with your login
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed login
if not ready:
    print("The run did not reach the model. Open the hint below, then run the cell again.")
ready
```

```{hint}
:title: If it says you are not logged in
The SDK found no Claude login on this machine. In a terminal, run
`claude`, type `/login` and sign in with a Claude Pro, Max, Team or
Enterprise account, then run the cell again from the notebook. The
command `claude auth status` shows whether a login is in place.

An API key in the `ANTHROPIC_API_KEY` environment variable also works,
and is used in preference to a login when it is set. Runs are then
billed to that key.
```
