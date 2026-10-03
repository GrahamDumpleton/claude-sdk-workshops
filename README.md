# Claude Agent SDK workshops

Guided, hands-on workshops on the
[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)
for Python, and through it on what an AI agent is and how one works.
They are for a Python developer who has used a chat assistant, and
perhaps a coding agent, and has never programmed one. Each workshop
takes one question, explains the idea behind it, and has you answer it
by running a real agent, with checks confirming each step. You never
type code: every cell, command and file edit arrives by clicking an
action.

The workshops run on
[jupyterlab-workshop](https://github.com/GrahamDumpleton/jupyterlab-workshop),
a JupyterLab extension that shows the instructions in a side panel with
clickable actions that drive the session, and checks what you have done
as you go. Each workshop is a directory of a `workshop.yaml` manifest
and Markdown pages. See [OUTLINE.md](OUTLINE.md) for the design of the
collections.

They run on your own machine and nowhere else, because every step calls
the model with your own Claude login. There is no Binder, Codespaces or
JupyterLite version. One `uvx` command runs them straight from this
repository, with nothing to clone: see [What you need](#what-you-need)
and [Run the workshops](#run-the-workshops).

## The collections

The repository holds three collections, meant to be taken in order.
Each collection is a course: its workshops are numbered in the order to
take them, and the Finish dialog of each offers the next. A
[catalog](catalog.json) names every collection.

All three collections are written, and every workshop passes the
extension's self-test.

### Agent foundations with the Claude Agent SDK

Ten workshops on what an agent is and how to run one, about two and a
half hours in all, each in a live notebook.

**What an agent is**

1. **Run your first agent** (`your-first-agent`, 15 minutes). What an
   agent is: a model that only produces text, and a program around it
   that carries out what the model asks for. Send a prompt with
   `query()` and take apart the system, assistant and result messages
   that come back. Then ask a question the model cannot answer on its
   own, give it the `Read` tool, and watch it read a file to get the
   answer.
2. **Watch the agent loop** (`watching-the-agent-loop`, 15 minutes).
   What happens between the prompt and the answer. Ask a question that
   takes several tool calls, then take the run apart: a request from
   the model is only text, the SDK carries it out and sends the result
   back in the user's role, every request carries the whole
   conversation so far, and the loop ends when the model replies
   without asking for anything.
3. **Read what a run cost** (`reading-the-result`, 15 minutes). The
   message that ends every run: how it ended, how many turns and
   seconds it took, what the token counts and the cache are, what the
   dollar figure means on a subscription, and where you stand against
   your plan's limits. Then a run stopped by its turn limit, and the
   error it comes back as.

**Shaping a run**

4. **Give the agent its instructions**
   (`giving-the-agent-instructions`, 15 minutes). What a system prompt
   is. Answer one customer question under a prompt of your own, under
   the same prompt with one rule changed, and under the `claude_code`
   preset, and compare what each sent to the model.
5. **Choose a model and how hard it thinks** (`choosing-a-model`, 15
   minutes). Run one task that needs two documents read together on
   Haiku and on Sonnet, and compare turns, tokens, seconds and
   estimated cost. Then lower `effort`, and turn thinking back on to
   see what it adds. The one workshop here that leaves the smallest
   model.
6. **Decide what the agent can do** (`deciding-what-it-can-do`, 20
   minutes). Give the agent a tool that writes a file and watch the
   call be refused. Then approve it with `allowed_tools`, approve it
   with a permission mode, and take the tool away with
   `disallowed_tools`, reading what was denied from each result.

**Beyond one question**

7. **Hold a conversation** (`holding-a-conversation`, 15 minutes). Two
   calls to `query()` know nothing of each other. A `ClaudeSDKClient`
   keeps one session open and remembers, by sending the whole
   conversation again on each turn. Measure what that costs and how
   full the context window is.
8. **Pick up where you left off** (`picking-up-where-you-left-off`, 15
   minutes). Where a session is kept once the program has gone. List
   sessions and read one back, resume it from a new run, fork it
   without changing the original, and delete what you made.
9. **Stream the reply as it is written** (`streaming-the-reply`, 15
   minutes). Time a reply that arrives all at once, turn on partial
   messages and count the events one reply is made of, print the text
   as it is written, and compare the pieces with the complete message.
10. **Get data back, not prose** (`getting-data-back`, 15 minutes). Use
    an agent as a function. Describe the shape you want with a JSON
    Schema, get back a dictionary that matches it, and answer
    questions from it in ordinary Python.

### Extending an agent with the Claude Agent SDK

Nine workshops on giving an agent more to work with and tighter limits,
about two and three quarter hours in all, each in a live notebook, some
with the file the agent is given open beside it.

**More to work with**

1. **Give the agent a tool of your own** (`giving-the-agent-a-tool`,
   20 minutes). Turn a Python function into a tool with `@tool` and a
   server that runs inside your own program. The model sees only the
   tool's name, description and input, so run one question against a
   vague description and an honest one, add a second tool, and mark
   tools that only look so the SDK runs them side by side.
2. **Connect an MCP server** (`connecting-an-mcp-server`, 15 minutes).
   What the Model Context Protocol is, by using it. Have the SDK start
   a small server program of its own, read its state and tools with
   `get_mcp_status()`, ask the agent a question through it, and see
   how a server that fails to start is reported.
3. **Answer from your own data** (`answering-from-your-own-data`, 20
   minutes). Two ways to put what you know within an agent's reach.
   The agent searches and reads the shop's documents with its built-in
   tools, queries an orders database through a read-only tool of yours,
   and answers a question that needs both. The SDK has no vector store
   of its own, and the workshop says where one would go.

**Standing knowledge**

4. **Give instructions that persist** (`instructions-that-persist`, 15
   minutes). Keep house rules in a `CLAUDE.md` and load them with
   `setting_sources`. See which instruction files a session was given,
   what they add to every request, what else the option lets in, and
   why the other workshops keep it empty.
5. **Package know-how as a skill** (`packaging-know-how-as-a-skill`,
   15 minutes). A procedure the agent loads only when it needs it.
   Install a skill, see that only its description is in the context to
   begin with, watch the agent call the `Skill` tool when a refund
   comes up, and compare a request that needs it with one that does
   not.

**Control and scale**

6. **Ask before acting** (`asking-before-acting`, 20 minutes). Put a
   decision of your own in front of what an agent changes. A
   `can_use_tool` callback allows one call, refuses another with a
   reason the model reads, changes the input of a third, and answers a
   clarifying question the agent asks.
7. **Put guardrails in code** (`guardrails-in-code`, 20 minutes). What
   a prompt can only ask for and what code can enforce. Give an agent
   a rule in its system prompt and a request that argues with it, then
   enforce the rule with a `PreToolUse` hook, and log every tool call
   with a `PostToolUse` hook.
8. **Hand work to subagents** (`handing-work-to-subagents`, 20
   minutes). Have one agent give the reading of ten files to another,
   defined with `AgentDefinition`, compare what the main conversation
   holds each way, and run the two agents on different models.
9. **Keep a long session small** (`keeping-a-long-session-small`, 20
   minutes). Measure what is in the context window, fill it, compact
   it and read the summary that replaces the history, find out what
   survived, and have the definitions of twenty tools wait until they
   are looked for.

### Building a chat app with the Claude Agent SDK

Eight workshops that build a web chat application a step at a time,
about two and three quarter hours in all, with the server in a
terminal, its source in an editor and the application in a pane beside
them.

The server is written with [FastAPI](https://fastapi.tiangolo.com),
and each workshop ships the application as the one before left it, so
any of them can be taken on its own.

1. **Build the smallest chat app** (`the-smallest-chat-app`, 20
   minutes). Start a small web server, see what a chat page and its
   server say to each other, put a run of the agent behind the route
   that answers a message, and find out what the application cannot do
   yet.
2. **Stream the reply to the browser** (`streaming-to-the-browser`, 20
   minutes). Watch a reply arrive all at once, turn on partial
   messages and send each piece of text as a server-sent event, read
   the raw stream in a terminal, and have the page add each piece as
   it arrives.
3. **Keep a conversation for each visitor**
   (`one-conversation-per-visitor`, 25 minutes). Have the page keep an
   id, keep a connected client on the server for each one, restore
   what was said when the page reloads, open a second visitor beside
   the first, and pick a conversation up after the server restarts.
4. **Show the agent at work** (`showing-the-agent-at-work`, 15
   minutes). Send the page an event for each tool request and each
   result, and draw them in the conversation so that a pause reads as
   work.
5. **Approve from the browser** (`approving-from-the-browser`, 25
   minutes). Give the agent a tool that writes, put each request to
   the page and wait for an answer with a time limit, show it in the
   chat with buttons to allow or refuse, and add a button that stops a
   run.
6. **Plug in your tools** (`plugging-in-your-tools`, 20 minutes). Show
   in the page which tools the agent has, then plug in a tool for the
   stock list, one in front of the orders database and a skill for
   refund replies, and see each used from the chat.
7. **Come back to a conversation** (`coming-back-to-a-conversation`,
   20 minutes). List the sessions the SDK has kept, open an earlier
   one by its id and carry on after a restart, and branch a
   conversation into a copy that goes its own way.
8. **Show usage and set limits** (`showing-usage-and-limits`, 20
   minutes). Show what each turn sent and wrote and how full the
   conversation is, let the person in the chat choose the model, and
   put a limit on the turns one message can take.

## What you need

- **A Claude login the SDK can use.** The SDK runs Claude Code
  underneath and uses its login. Install
  [Claude Code](https://code.claude.com/docs/en/setup), run `claude`,
  and log in with a Claude Pro, Max, Team or Enterprise account. Check
  with `claude auth status`. An API key from the
  [Claude Console](https://platform.claude.com/) in `ANTHROPIC_API_KEY`
  works as well, and is used in preference to the login when it is set,
  in which case every run is billed to that key.

- **[uv](https://docs.astral.sh/uv/)**, and nothing else to install.
  It fetches Python 3.14, JupyterLab, the extension, the SDK and, for
  the chat app workshops, FastAPI.

- **macOS or Linux.** Nothing here has been tried on Windows.

## What running them costs

Every step that matters calls the model. With a subscription login
nothing is charged per run, and the runs count against your plan's
usage limits like any other use of Claude. The workshops are built to
use little: they run on Haiku, the smallest model, except in the
three places a workshop is about a larger one, and they keep each
request small. A workshop makes two to seven small runs: the ten
foundations workshops about forty between them, the nine extending
workshops about forty more, and the eight chat app workshops about
thirty five. The largest are in the two workshops that have an agent
read ten short files.

Anthropic does not allow a third party to offer claude.ai login or its
rate limits in a product of their own. Running these workshops, and
agents you write for yourself, under your own login is not that. An
application you build for other people to use runs on an API key.

## An agent acts on your machine

The agent in these workshops is real. It reads files, and in some
workshops writes them, on the machine you run it on, with your access.
Each workshop keeps it inside the workshop's own workspace directory
and gives it only the tools the step needs, and the foundations
workshops explain how that is done and why. The extension shows what a
workshop is allowed to do, and asks, before it runs anything.

The chat app workshops also start a web server on your machine, in a
terminal you can see. It listens on `127.0.0.1` only, so nothing
outside the machine can reach it, and each workshop ends by stopping
it.

## Run the workshops

### Straight from this repository

With uv installed, one command starts JupyterLab with everything the
workshops need and opens the workshop browser on this repository's
catalog. Nothing is cloned and nothing is installed that stays. Run it
in a shell where `claude` is logged in:

```
uvx --python 3.14 --from "jupyterlab-workshop[lab]" --with "claude-agent-sdk==0.2.163" --with "fastapi==0.142.2" jupyter-workshop launch --root ~/training --catalog https://raw.githubusercontent.com/GrahamDumpleton/claude-sdk-workshops/main/catalog.json
```

What each part is for:

- `--from "jupyterlab-workshop[lab]"` brings the extension, with the
  `lab` extra bringing JupyterLab along.

- `--with "claude-agent-sdk==0.2.163"` adds the SDK, at the release
  the workshops are written and tested against. Do not leave it out.
  The notebooks run in this environment, and without the SDK the first
  cell of every workshop fails on its import.

- `--with "fastapi==0.142.2"` adds FastAPI, which the chat app
  workshops write their server with. It is small: the SDK already
  brings the web server and the other libraries FastAPI is built on.
  Leave it out only if you will not take those workshops.

- `--root ~/training` is a directory of your own to keep the workshops
  in. It is created if it is not there.

- `--catalog` names this repository's catalog, which lists the three
  collections.

JupyterLab starts on a free port and opens the workshop browser with
the catalog added, which offers each collection to subscribe to. Each
workshop is fetched from this repository into `~/training/workshops`
as you open it, and stays there for the next launch. uv keeps the
environment cached, so a second launch starts in a few seconds.

To land with a collection's workshops already listed, in order, give
its index in place of the catalog. Repeat `--collection` to list
several:

```
uvx --python 3.14 --from "jupyterlab-workshop[lab]" --with "claude-agent-sdk==0.2.163" --with "fastapi==0.142.2" jupyter-workshop launch --root ~/training --collection https://raw.githubusercontent.com/GrahamDumpleton/claude-sdk-workshops/main/collections/foundations/collection.json
```

To have a shorter command to come back to, install the same thing as a
uv tool once, and launch with it from then on:

```
uv tool install --python 3.14 "jupyterlab-workshop[lab]" --with "claude-agent-sdk==0.2.163" --with "fastapi==0.142.2"
jupyter-workshop launch --root ~/training --catalog https://raw.githubusercontent.com/GrahamDumpleton/claude-sdk-workshops/main/catalog.json
```

### From a checkout

Clone the repository and start JupyterLab from the checkout. uv
installs the environment the first time:

```
git clone https://github.com/GrahamDumpleton/claude-sdk-workshops
cd claude-sdk-workshops
uv run --no-dev jupyter lab --config=jupyter_lab_config.py
```

Run from the checkout, the workshops appear under Installed in the
workshop browser, grouped under each collection and numbered in the
order to take them. The environment has the SDK and FastAPI at the
releases [pyproject.toml](pyproject.toml) pins.

### From your own JupyterLab

With the extension already installed in a JupyterLab of your own, the
workshops also need the SDK, and for the chat app workshops FastAPI,
in the environment that JupyterLab's default kernel runs in:

```
pip install "claude-agent-sdk==0.2.163" "fastapi==0.142.2"
```

Then, in the workshop browser, choose "Collections…" and enter the raw
URL of the catalog on the Catalogs tab, or of a collection's index on
the Collections tab:

```
https://raw.githubusercontent.com/GrahamDumpleton/claude-sdk-workshops/main/catalog.json
https://raw.githubusercontent.com/GrahamDumpleton/claude-sdk-workshops/main/collections/foundations/collection.json
https://raw.githubusercontent.com/GrahamDumpleton/claude-sdk-workshops/main/collections/extending/collection.json
https://raw.githubusercontent.com/GrahamDumpleton/claude-sdk-workshops/main/collections/chat-app/collection.json
```

However it is started, the trust dialog appears when a workshop opens.
It lists what the workshop's pages are allowed to do.

## What is in the repository

```
AGENTS.md                 guidance for agents writing the workshops
CLAUDE.md                 the single line @AGENTS.md
OUTLINE.md                the design of the collections
Justfile                  every common task, and the order of each collection
pyproject.toml, uv.lock   the uv project: JupyterLab, the extension, the SDK and FastAPI, pinned
jupyter_lab_config.py     the local start: opens the browser on the catalog and collections
catalog.json              names every collection, written by `just index`
collections/<name>/       the ordered index of one collection, written by `just index`
workshops/<name>/         one workshop: workshop.yaml, pages/ and files/, and for a
                          chat app workshop checks/, the scripts behind its checks
reference/                git submodules, read by agents, at the pinned releases:
  jupyterlab-workshop       the extension's docs, examples and source
  claude-agent-sdk-python   the SDK's source, examples and changelog
.mcp.json                 the jupyterlab-workshop MCP server for agents
.github/workflows/        lint on each push
```

## Writing and checking workshops

This part is for whoever writes the workshops, and works from a
checkout made with `git clone --recurse-submodules`. It uses
[just](https://just.systems/): `just install` sets the checkout up, and
`just --list` shows every recipe. Each recipe is a short `uv run`
command you can read in the [Justfile](Justfile) and run by hand. The
ones used most:

- `just lab` starts JupyterLab from the checkout.

- `just new <name>` scaffolds a workshop under `workshops/`.

- `just lint` lints the catalog, every collection index and every
  workshop, and `just lint <name>` one workshop.

- `just test <name>` self-tests one workshop in a JupyterLab of its
  own. It runs every cell for real, so it calls the model under your
  login and uses your plan. `just test-all` does every workshop, and
  spends accordingly.

- `just index` writes or refreshes every collection index and the
  catalog, in the order the Justfile gives.

- `just render <name>` renders a workshop to HTML to read its pages.

CI lints and does not self-test, since a runner has no Claude login.

## Updating the releases

- `just bump <version>` pins a new jupyterlab-workshop release, relinks
  the authoring skill and moves `reference/jupyterlab-workshop` to the
  same tag.

- `just bump-sdk <version>` pins a new claude-agent-sdk release, moves
  `reference/claude-agent-sdk-python` to the same tag, and rewrites the
  release named in the commands in this README. The SDK
  changes quickly, so read its changelog and retest the workshops
  after a bump.

- `just bump-fastapi <version>` pins a new FastAPI release and
  rewrites the release named in the commands in this README. Only the
  chat app workshops use it.
