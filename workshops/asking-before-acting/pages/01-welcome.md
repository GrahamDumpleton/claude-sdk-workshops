---
title: Welcome
requires: [verify:sdk-ready, verify:login-works]
---

# Ask before acting

An agent acts on the machine it runs on. The model asks for a tool,
and the SDK, the program around the model, decides whether the call
may run before it runs it. Looking at files in the agent's own
directory needs no approval. Changing something does.

**Decide what the agent can do** showed what happens when a call
needs approval and there is nobody to give it: the call is refused.
It then approved calls ahead of time, by tool and by mode. Those are
blanket answers, given before the agent has asked for anything.

This workshop gives the SDK someone to ask. `can_use_tool` is an
option that names a function of yours. When a call needs approval,
the SDK stops, calls your function with the name of the tool and
exactly what the model wants to pass to it, and does what your
function says. That is how a person stays in the loop: the function
shows them the call and returns their answer.

A notebook has no dialog to put in front of you, so the function here
decides by a few rules that stand in for a person. The mechanism is
the one a real application uses, and the last set of workshops,
**Building a chat app with the Claude Agent SDK**, puts a person
behind it.

## What it runs on

The SDK calls the model with the Claude login on this machine, the one
the `claude` command uses. Every run counts against that plan's usage,
as a message in the Claude app does. This workshop makes five small
runs on the smallest model.

The agent writes a few short notices inside this workshop's own folder
of files. The function you give it refuses any write outside that
folder.

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
    # Ask before acting
    Each step of the workshop adds a cell below.
- code: |
    from pathlib import Path

    import claude_agent_sdk
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        PermissionResultAllow,
        PermissionResultDeny,
        ResultMessage,
        ToolUseBlock,
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
