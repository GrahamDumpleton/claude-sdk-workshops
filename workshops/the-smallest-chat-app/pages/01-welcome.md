---
title: Welcome
requires: [verify:python-found, verify:login-works]
---

# Build the smallest chat app

An agent is a model with a program around it, here the Claude Agent
SDK. So far your own code has started each run: a script or a notebook
cell calls `query()` and prints what comes back. A chat application is
the same agent with a different front door. The prompt is typed into a
web page by somebody else, and the reply has to get back to that page.

That takes three pieces, and this workshop puts them together.

- **A page**, in the browser, with a box to type in and somewhere to
  show what was said.

- **A server**, a Python program of yours that stays running. It hands
  the browser the page, and it answers each message the page sends.

- **The agent**, which the server runs to work out each reply.

The agent here is the assistant for the staff of Tidewater Books, a
small bookshop, and what it knows about the shop is in a few files.

```{file-open}
:id: open-diagram
:title: Open a diagram of the three pieces
:path: diagrams/three-pieces.md
:factory: Markdown Preview
:area: code
```

These workshops build one application a step at a time, and this one
makes the smallest version that works. The server is written with
[FastAPI](https://fastapi.tiangolo.com), a Python library for writing
web servers. You need no knowledge of it: each page says what the code
it adds does.

## What it runs on

The SDK calls the model with the Claude login on this machine, the one
the `claude` command uses. Every run counts against that plan's usage,
as a message in the Claude app does. This workshop makes three small
runs on the smallest model.

```{when} "claude" in missing_tools
The `claude` command was not found. The SDK carries its own copy of
Claude Code, so the workshop still works if this machine has logged in
before. If the login check further down fails, install
[Claude Code](https://code.claude.com/docs/en/setup), run `claude` in a
terminal and log in.
```

## The window

The main area has three parts. On the left are the two files the
application is made of, {open}`app.py`, the server, and
{open}`page.html`, the page. Below them is a terminal, where the server
will run. The space on the right is for the application itself, once
it is running.

You never have to type code. Each step changes a file or runs a command
through a button on these pages.

## Find the right Python

The server has to run on a Python that has the SDK installed, and that
is the one JupyterLab itself runs on. A terminal does not always find
the same one, so the step below asks JupyterLab where its Python is.
The commands on later pages use the answer.

```{kernel-execute}
:id: find-python
:title: Find the Python that JupyterLab runs on
:capture: app_python
import sys

print(sys.executable)
```

It is {var}`app_python`.

```{verify}
:id: python-found
:label: The path of JupyterLab's Python is known
:trigger: after:find-python
import os

assert os.path.exists("{{ app_python }}"), "Click the action above to find the Python."
```

## Check the login

Before anything else, make sure the SDK can reach the model. The script
{open}`check_login.py` asks the agent for one word. It takes a few
seconds, as every step that calls the model does: the wait is the model
working.

```{execute}
:id: check-login
:title: Ask the model for one word
:session: server
:wait: prompt
{{ app_python | shell }} check_login.py
```

The last line it prints is `ready: True` when the model answered.

```{verify}
:id: login-works
:label: The SDK can reach the model with your login
:substrate: contents
:trigger: after:check-login
contains login.txt ready: True
```

```{hint}
:title: If it says you are not logged in
The SDK found no Claude login on this machine. In a terminal, run
`claude`, type `/login` and sign in with a Claude Pro, Max, Team or
Enterprise account, then run the step again. The command
`claude auth status` shows whether a login is in place.

An API key in the `ANTHROPIC_API_KEY` environment variable also works,
and is used in preference to a login when it is set. Runs are then
billed to that key.
```

```{hint}
:title: What the options in that script are for
`query()` runs an agent once and hands back messages as the run goes
on. `model="haiku"` picks the smallest model, `system_prompt` is the
standing instruction the agent works under, `tools=[]` gives it no
tools, and `max_turns` stops a run that goes wrong.

`setting_sources=[]` and `strict_mcp_config=True` keep your own Claude
configuration out of the run, so the agent behaves the same on every
machine. `thinking={"type": "disabled"}` turns off a step in which the
model reasons privately before it answers, which these tasks do not
need. Every agent in these workshops sets all three.

The `env` line is housekeeping. The SDK normally saves every run to a
file under your home directory, so that it can be picked up again
later. This one run is not worth keeping, so the line tells the SDK
not to save it.
```
