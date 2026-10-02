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
JupyterLite version. See [What you need](#what-you-need) and
[Run locally](#run-locally).

## The collections

The repository holds three collections, meant to be taken in order.
Each collection is a course: its workshops are numbered in the order to
take them, and the Finish dialog of each offers the next. A
[catalog](catalog.json) names every collection.

No workshop is written yet. The lists below are the plan, from
[OUTLINE.md](OUTLINE.md), and each entry is filled in as its workshop
is written.

### Agent foundations with the Claude Agent SDK

Ten workshops on what an agent is and how to run one, about two and a
half hours in all, each in a live notebook.

**What an agent is**

1. **Run your first agent** (`your-first-agent`)
2. **Watch the agent loop** (`watching-the-agent-loop`)
3. **Read what a run cost** (`reading-the-result`)

**Shaping a run**

4. **Give the agent its instructions** (`giving-the-agent-instructions`)
5. **Choose a model and how hard it thinks** (`choosing-a-model`)
6. **Decide what the agent can do** (`deciding-what-it-can-do`)

**Beyond one question**

7. **Hold a conversation** (`holding-a-conversation`)
8. **Pick up where you left off** (`picking-up-where-you-left-off`)
9. **Stream the reply as it is written** (`streaming-the-reply`)
10. **Get data back, not prose** (`getting-data-back`)

### Extending an agent with the Claude Agent SDK

Nine workshops on giving an agent more to work with and tighter limits,
about three hours in all, each in a notebook, most with the code the
agent is given open beside it.

1. **Give the agent a tool of your own** (`giving-the-agent-a-tool`)
2. **Connect an MCP server** (`connecting-an-mcp-server`)
3. **Answer from your own data** (`answering-from-your-own-data`)
4. **Give instructions that persist** (`instructions-that-persist`)
5. **Package know-how as a skill** (`packaging-know-how-as-a-skill`)
6. **Ask before acting** (`asking-before-acting`)
7. **Put guardrails in code** (`guardrails-in-code`)
8. **Hand work to subagents** (`handing-work-to-subagents`)
9. **Keep a long session small** (`keeping-a-long-session-small`)

### Building a chat app with the Claude Agent SDK

Eight workshops that build a web chat application a step at a time,
about two and three quarter hours in all, with the server in a
terminal, its source in an editor and the application in a pane beside
them.

1. **Build the smallest chat app** (`the-smallest-chat-app`)
2. **Stream the reply to the browser** (`streaming-to-the-browser`)
3. **Keep a conversation for each visitor** (`one-conversation-per-visitor`)
4. **Show the agent at work** (`showing-the-agent-at-work`)
5. **Approve from the browser** (`approving-from-the-browser`)
6. **Plug in your tools** (`plugging-in-your-tools`)
7. **Come back to a conversation** (`coming-back-to-a-conversation`)
8. **Show usage and set limits** (`showing-usage-and-limits`)

## What you need

- **A Claude login the SDK can use.** The SDK runs Claude Code
  underneath and uses its login. Install
  [Claude Code](https://code.claude.com/docs/en/setup), run `claude`,
  and log in with a Claude Pro, Max, Team or Enterprise account. Check
  with `claude auth status`. An API key from the
  [Claude Console](https://platform.claude.com/) in `ANTHROPIC_API_KEY`
  works as well, and is used in preference to the login when it is set,
  in which case every run is billed to that key.

- **[uv](https://docs.astral.sh/uv/)**, which installs Python 3.14,
  JupyterLab, the extension and the pinned SDK.

- **[just](https://just.systems/)**, for the recipes below. Every
  recipe is a short `uv run` command you can read in the
  [Justfile](Justfile) and run by hand.

- **macOS or Linux.** Nothing here has been tried on Windows.

## What running them costs

Every step that matters calls the model. With a subscription login
nothing is charged per run, and the runs count against your plan's
usage limits like any other use of Claude. The workshops are built to
use little: they run on Haiku, the smallest model, except in the two
or three places a workshop is about a larger one, and they keep each
request small. A workshop makes two to four small runs.

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

## Run locally

Clone the repository with its submodules and install:

```
git clone --recurse-submodules https://github.com/GrahamDumpleton/claude-sdk-workshops
cd claude-sdk-workshops
just install
```

Then start JupyterLab from the checkout, in a shell where `claude` is
logged in:

```
just lab
```

It opens on the workshop browser with the three collections listed in
order. Without just, the two commands are `uv sync` and
`uv run jupyter lab --config=jupyter_lab_config.py`.

The workshops run on the kernel of this environment, which is where
the pinned SDK is installed. Subscribing to the catalog from another
JupyterLab works only if that environment has `claude-agent-sdk` at
the version pinned in [pyproject.toml](pyproject.toml).

## What is in the repository

```
AGENTS.md                 guidance for agents writing the workshops
CLAUDE.md                 the single line @AGENTS.md
OUTLINE.md                the design of the collections
Justfile                  every common task, and the order of each collection
pyproject.toml, uv.lock   the uv project: JupyterLab, the extension and the SDK, pinned
jupyter_lab_config.py     the local start: opens the browser on the catalog and collections
catalog.json              names every collection, written by `just index`
collections/<name>/       the ordered index of one collection, written by `just index`
workshops/<name>/         one workshop: workshop.yaml, pages/ and files/
reference/                git submodules, read by agents, at the pinned releases:
  jupyterlab-workshop       the extension's docs, examples and source
  claude-agent-sdk-python   the SDK's source, examples and changelog
.mcp.json                 the jupyterlab-workshop MCP server for agents
.github/workflows/        lint on each push
```

## Writing and checking workshops

`just --list` shows every recipe. The ones used most:

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

- `just bump-sdk <version>` pins a new claude-agent-sdk release and
  moves `reference/claude-agent-sdk-python` to the same tag. The SDK
  changes quickly, so read its changelog and retest the workshops
  after a bump.
