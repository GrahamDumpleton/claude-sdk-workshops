---
title: Welcome
requires: [verify:python-found, verify:login-works, verify:server-up]
---

# Keep a conversation for each visitor

The chat looks like a conversation and is not one. Each message is
answered by a fresh run of the agent, which has never seen the message
before it.

A model keeps nothing between requests. What makes a conversation is
the program around it: the SDK keeps everything said in a session and
sends all of it to the model with each new message. `query()` starts a
new session every time it is called. A `ClaudeSDKClient` is the SDK's
way of holding one session open and sending it one message after
another.

A web server adds a question a script never had: whose conversation?
One server answers many browsers at once, and each needs a session of
its own, kept apart from the others. This workshop gives every visitor
a conversation, keeps a client on the server for each, and finds out
what happens to them when the page is reloaded and when the server
restarts.

## What it runs on

The SDK calls the model with the Claude login on this machine, the one
the `claude` command uses. Every run counts against that plan's usage,
as a message in the Claude app does.
This workshop makes five small runs on the smallest model.

```{when} "claude" in missing_tools
The `claude` command was not found. The SDK carries its own copy of
Claude Code, so the workshop still works if this machine has logged in
before. If the login check further down fails, install
[Claude Code](https://code.claude.com/docs/en/setup), run `claude` in a
terminal and log in.
```

## The application so far

These workshops build one chat application a step at a time, and each
ships it as the one before left it, so you can start here. The agent
behind it is the assistant for the staff of Tidewater Books, a small
bookshop.

The main area has three parts. On the left are the two files the
application is made of, {open}`app.py`, the server, and
{open}`page.html`, the page. Below them is a terminal, where the server
runs. The space on the right is for the application itself.

The server has one route that matters. `chat()` in `app.py` runs the
agent on each message with `query()` and streams the reply to the page
as the model writes it, and `events_for()` decides what the page is
told about each message of a run. The agent can find and read the
shop's documents, which are in the `shop` directory. Nothing is
remembered from one message to the next.

You never have to type code. Each step changes a file or runs a command
through a button on these pages.

## Find the right Python

The server has to run on a Python that has the SDK installed, and that
is the one JupyterLab itself runs on. A terminal does not always find
the same one, so the step below asks JupyterLab where its Python is.
The commands on these pages use the answer.

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

## Start the server

The command runs the server with `uvicorn`, the program that listens
on a port and passes each request to the application. With `--reload`,
uvicorn restarts the server whenever `app.py` is saved, which the
steps of this workshop rely on.

```{execute}
:id: start-server
:title: Start the server
:session: server
:wait: 4s
{{ app_python | shell }} -m uvicorn app:app --port {{ server_port }} --reload
```

```{verify}
:id: server-up
:label: The server is answering
:substrate: script
:script: checks/server_up.py
:trigger: after:start-server
```

```{hint}
:title: If the port is already in use
The server prints "address already in use" when another program has
port {{ server_port }}. The gear button at the top of this panel opens
the Variables dialog, where `server_port` can be changed. The commands
and links on these pages then use the new number. Run the step again
afterwards.
```

## Open the chat

The step below opens the application beside its source, as a browser
would show it.

```{url-open}
:id: open-chat
:title: Open the chat
:url: http://127.0.0.1:{{ server_port }}/
:pane: chat
:label: Chat
:area: chat
```

You can type in its box at any time. The steps on the pages that
follow ask their questions through the page's address, so that a
button here can put a question to the chat.
