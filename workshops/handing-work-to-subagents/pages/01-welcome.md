---
title: Welcome
requires: [verify:sdk-ready, verify:login-works]
---

# Hand work to subagents

An agent works in a loop: the model asks for a tool, the SDK runs it,
and the result joins the conversation. The model remembers nothing
between requests, so the whole conversation is sent again each time,
and everything an agent has read stays in it, to be sent with every
request for the rest of the session.

That is wasteful when a job means reading a lot to learn a little. To
find which of ten suppliers deliver within a week, an agent has to
read ten documents. Once it has the answer it has no more use for
them, and it carries them all the same.

A subagent is a way round that. It is a second agent, started by the
first to do one piece of work. It has its own instructions and its
own tools, and above all its own conversation, which starts empty. It
does the reading there, and when it is done it sends back a report.
The report joins the main conversation. Everything else the subagent
read is dropped with it.

This workshop does the same job both ways for a small bookshop,
Tidewater Books, and measures what each leaves behind. The reading is
the terms of supply of its ten suppliers, in the `suppliers` folder,
such as {open}`suppliers/saltmarsh-editions.md`.

## What it runs on

The SDK calls the model with the Claude login on this machine, the one
the `claude` command uses. Every run counts against that plan's usage,
as a message in the Claude app does. This workshop makes four runs.
Three of them read ten short files each, which makes them larger than
the runs of the earlier workshops, and the last uses a larger model,
Sonnet, for the main agent.

The agents can list and read the files in this workshop's own folder.
They change nothing.

```{when} "claude" in missing_tools
The `claude` command was not found. The SDK carries its own copy of
Claude Code, so the workshop still works if this machine has logged in
before. If the login check further down fails, install
[Claude Code](https://code.claude.com/docs/en/setup), run `claude` in a
terminal and log in.
```

## The notebook

The step below creates the notebook. Its first cell imports what the
workshop uses.

```{notebook-create}
:id: create-notebook
:path: {{ notebook }}
:open: true
- markdown: |
    # Hand work to subagents
    Each step of the workshop adds a cell below.
- code: |
    from dataclasses import replace
    from pathlib import Path

    import claude_agent_sdk
    from claude_agent_sdk import (
        AgentDefinition,
        AssistantMessage,
        ClaudeAgentOptions,
        ClaudeSDKClient,
        ResultMessage,
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

```{hint}
:title: What the options in that cell are for
`query()` runs an agent once and hands back messages as the run goes
on. `model="haiku"` picks the smallest model, `system_prompt` is the
standing instruction the agent works under, `tools=[]` gives it no
tools, and `max_turns` stops a run that goes wrong.

`setting_sources=[]` and `strict_mcp_config=True` keep your own Claude
configuration out of the run, so the agent behaves the same on every
machine. `thinking={"type": "disabled"}` turns off a step in which the
model reasons privately before it answers, which these tasks do not
need. Every agent in these workshops sets all three.
```
