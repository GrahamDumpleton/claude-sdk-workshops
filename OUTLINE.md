# Claude Agent SDK workshops: outline

The design of the collections in this repository: how they are
organised, what each workshop covers, its name and format, and the
decisions that cut across all of them. It is a living document. Read it
before adding a workshop, and update it when one is added, changed or
dropped: the status table at the end records where each workshop
stands, and the open questions section shrinks as they are settled.

The first two collections are written, and their entries below say
what was built. The third is designed to the level of what each
workshop is for, and its entries are filled out, with the user, before
its first workshop is written.

## What this repository is

Guided JupyterLab workshops for the
[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)
for Python, in three collections that are each a course of their own
and are meant to be taken in order.

The first collection, **Agent foundations with the Claude Agent SDK**,
is ten workshops on what an agent is and how to run one: the loop
between a model and its tools, what a run reports and costs, how
instructions, the model and permissions shape it, and how a
conversation is held, resumed, streamed and turned into data. It
assumes Python, including `async` and `await` at the level of having
seen them, and nothing about language models beyond having used a chat
assistant.

The second, **Extending an agent with the Claude Agent SDK**, is nine
workshops on giving an agent more to work with and tighter limits: your
own tools, MCP servers, your own data, instructions that persist,
skills, approvals, hooks, subagents and long sessions. It assumes the
first collection's ideas, the loop, tools, permissions and sessions,
and restates each where it matters.

The third, **Building a chat app with the Claude Agent SDK**, is eight
workshops that build a web chat application a step at a time, putting
streaming, sessions, approvals and tools behind a browser. It assumes
the first collection, and the second for the one workshop that plugs
tools in.

The workshops teach the concepts as well as the calls. The learner is
new to agents, so each workshop says what a thing is, why it works the
way it does and what it is for, before showing the call, and the
collections ramp up: no workshop in the first collection uses a term it
has not explained, and the detailed topics wait until the plain ones
are familiar.

What is deliberately out of scope: the TypeScript SDK, which the user
ruled out; the Claude API client SDK and writing a tool loop by hand,
which is a different library; hosting the workshops anywhere but the
learner's own machine; and deploying an agent as a service, which is
held as a later collection.

## Source material

The SDK's own source and documentation are the authority, never
memory. The SDK releases several times a week at times, so every claim
is checked against the pinned release before it is taught.

- `reference/claude-agent-sdk-python`, a submodule at the tag of the
  pinned release, 0.2.163 when this was written.
  `src/claude_agent_sdk/types.py` defines every option, message, block
  and hook type, and `__init__.py` lists what is exported. `examples/`
  holds working programs for most features: `quick_start.py`,
  `streaming_mode_ipython.py` (the patterns that work in a notebook),
  `tools_option.py`, `system_prompt.py`, `include_partial_messages.py`,
  `mcp_calculator.py`, `tool_permission_callback.py`, `hooks.py`,
  `agents.py`, `setting_sources.py` and `max_budget_usd.py`.
  `CHANGELOG.md` says which release a thing arrived in.

- The documentation at https://code.claude.com/docs/en/agent-sdk/, read
  in its Markdown form by adding `.md` to a page's address. The pages
  the collections draw on, by their last path segment: `overview`,
  `quickstart`, `agent-loop`, `python` (the reference), `configuration`,
  `permissions`, `sessions`, `streaming-vs-single-mode`,
  `streaming-output`, `structured-outputs`, `modifying-system-prompts`,
  `cost-tracking`, `custom-tools`, `mcp`, `tool-search`,
  `claude-code-features`, `skills`, `user-input`, `hooks`, `subagents`
  and `todo-tracking`. https://code.claude.com/docs/llms.txt lists
  every page.

- https://code.claude.com/docs/en/authentication.md for how the login
  is found and the order credentials are tried in, which the first
  workshop explains and no workshop changes.

- https://github.com/anthropics/claude-agent-sdk-demos for complete
  applications, read for the chat app collection and not taught from.

- The Model Context Protocol's own documentation at
  https://modelcontextprotocol.io for what MCP is, beyond what the SDK's
  `mcp` page says about connecting to it.

Each workshop entry names the pages and examples it draws on.

### What was checked before the design

A short trial on 2026-10-02, with claude-agent-sdk 0.2.163 on Python
3.14 and macOS, under a Claude Max login with no API key set. The
figures are from single runs and are there for their size, not their
value.

- The SDK authenticates with the `claude` login and reports
  `apiKeySource` as `none` in the `init` message.

- `model="haiku"` ran as `claude-haiku-4-5-20251001`, and
  `model="sonnet"` as `claude-sonnet-5-5`.

- A prompt that reads one small file and answers took two turns and
  six to eight seconds on Haiku, at an estimated $0.016, with a short
  system prompt and `tools=["Read"]`. The same run with the
  `claude_code` preset and every tool cost an estimated $0.037, the
  difference being about sixteen thousand tokens of preset prompt and
  tool definitions. A turn with no tools at all cost an estimated
  $0.003. Sonnet on the first configuration cost an estimated $0.023.

- `effort="low"` was accepted with Haiku and made no visible
  difference.

- With `setting_sources=[]` and nothing else, the session still had 29
  built-in tools and four claude.ai connectors as MCP servers.
  `tools=["Read"]` cut the tools to that one, and
  `strict_mcp_config=True` removed the connectors.

- In a notebook run on a real kernel, `async for ... in query(...)`
  worked at the top level of a cell, and a `ClaudeSDKClient` connected
  in one cell answered in the next two and kept one session id, then
  disconnected in a fourth.

- The installed package is about 216 MB, nearly all of it the bundled
  Claude Code binary.

Found while writing the first workshop, on the same release:

- Left to itself, Haiku reasons before it replies. A one sentence
  answer came with two `SystemMessage` objects of subtype
  `thinking_tokens` and an `AssistantMessage` holding a `ThinkingBlock`
  with no text, and 158 of its 226 output tokens were thinking. With
  `thinking={"type": "disabled"}` the same run produced a
  `SystemMessage` (`init`), a `RateLimitEvent`, one `AssistantMessage`
  and the `ResultMessage`, and 54 output tokens.

- Under a subscription login the stream carries a `RateLimitEvent`
  whose raw data gives the fraction of the five hour and seven day
  limits used. Workshop 3 can show a learner where they stand from it.

- With no login, the run yields an `AssistantMessage` whose `error` is
  `authentication_failed` and a `ResultMessage` with `is_error` true
  and the text "Not logged in · Please run /login", and `query()` then
  raises `ResultError`.

- `tools=["Read"]` with no `allowed_tools` reads a file in the working
  directory without any approval. The kernel of a notebook in the
  workspace starts in the workspace, so that is the agent's working
  directory with no `cwd` set.

- A run with no tools took about three seconds in the self-test, and
  the run that reads a file about four.

- JupyterLab's Markdown preview renders a mermaid block, flowchart and
  sequence diagram both.

Found while writing workshops 2 to 10, on the same release. Several
changed the design, and the entries below are written to what was
found.

- **The cache is not used on a small request.** The cache counts in
  `usage` were zero on every lean run, and first appeared when a
  request passed about four thousand tokens. So workshop 3 explains
  the cache and says the counts are zero, workshop 4 shows it at work
  on the preset run, and workshops 2 and 7 show a conversation growing
  in the plain input count.

- **One reply is several messages.** A reply holding text and a tool
  request arrives as an `AssistantMessage` for each block, with the
  same `message_id` and the same `usage`. That `usage` gives the input
  the request was sent. Its output count is not final and is not used.

- **`num_turns` counts tool requests, plus one for the answer.** A
  reply that asked for two tools at once counted as two. The
  documentation's worked example counts such a reply once. Workshop 2
  says how the SDK counts and checks only that there were at least two.

- **A turn limit ends a run as the documentation says.** With
  `max_turns=1` the result had the subtype `error_max_turns`, no
  `result`, and `errors` naming the limit, and `query()` then raised
  `ResultError`.

- **The preset adds about six thousand tokens.** With one tool, the
  first request was about 1,800 tokens under a prompt of four
  sentences and about 8,100 under the `claude_code` preset. The sixteen
  thousand of the first trial was the preset and every built-in tool
  together.

- **With no system prompt the agent has no role.** Asked the bookshop
  question with `system_prompt` unset, the model said it was an AI
  assistant and not a bookshop, and read nothing.

- **Effort shows little on a small task.** `effort="low"` and
  `effort="high"` on Sonnet gave runs within the spread of two runs at
  the same setting. Setting `effort` on Sonnet also produced thinking
  tokens with `thinking` disabled, which is why workshop 5's table has
  no thinking column.

- **The starting permission mode is not fixed.** The documentation
  says a session with no `permission_mode` starts in a mode chosen by
  settings and defaults, which can be `auto`. Workshop 6 passes
  `"default"` by name.

- **A refused call is a tool result.** In `default` mode with no
  callback, a `Write` came back as a `ToolResultBlock` with `is_error`
  set, the stream carried a `SystemMessage` of subtype
  `permission_denied`, and the result listed the call in
  `permission_denials`. The run ended in `success`.

- **A model can ask for a tool it was not given.** With `Write` in
  `disallowed_tools` the session's tool list did not have it, and the
  model asked for it anyway and was told no such tool was available.
  Nothing appears in `permission_denials` for that.

- **A client reports usage a turn at a time.** On a `ClaudeSDKClient`
  each result's `usage` is that turn's, while `total_cost_usd` runs on
  through the session. `get_context_usage()` answers without a model
  call, before the first turn as well as after.

- **Auto-memory gets past `setting_sources=[]`.** When the working
  directory is inside a project that Claude Code keeps auto-memory
  for, the session is sent that project's memory index:
  `get_context_usage()` lists it under "Memory files". It was 81
  tokens here. `settings='{"autoMemoryEnabled": false}'` and the
  environment variable `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` each removed
  it. See the open questions.

- **Sessions behave as documented.** `list_sessions()`,
  `get_session_messages()`, `resume`, `fork_session` and
  `delete_session()` all worked on transcripts in the workspace's
  project directory. A session's `summary` is a generated title.

- **Stream events arrive around the complete message.** With
  `include_partial_messages=True` a text reply gave a `message_start`,
  a `content_block_start`, about a hundred `content_block_delta`
  events, then the complete `AssistantMessage`, then
  `content_block_stop`, `message_delta` and `message_stop`. The joined
  deltas equalled the message's text.

- **Structured output is a tool call.** With `output_format` set, the
  model's last act was to call a tool named `StructuredOutput` with
  the data as its input. `structured_output` held the dictionary and
  `result` the same data as JSON text. Haiku met the schema each time.

- **A second self-test in place does not finish.** `jupyter workshop
  test --in-place` on a directory that already held the state of an
  earlier run was still going after four minutes and was stopped. The
  likely cause is the Restart or Continue dialog a reopened workshop
  shows. Test on a copy, which is what the tool does by default.

Found while writing the extending collection, on the same release,
which bundles Claude Code 2.1.286. The entries further down are
written to these.

- **A tool of your own needs approving.** A call to an SDK MCP tool
  with no `allowed_tools` entry was refused as `Write` is, with a
  `permission_denied` message, whether or not the tool was marked
  read-only. `tools=[]` leaves MCP tools in place.

- **A vague description gets a tool misused.** With a title lookup
  described as "Look up a book.", Haiku passed an author's name as the
  title on three runs of three and reported that the shop had nothing
  by her. With a description that said the tool matches whole titles
  only, it asked for a title on three of three and made no call.

- **`readOnlyHint` is what lets calls overlap.** Three calls asked for
  in one reply, each waiting a second, started a second apart without
  the annotation and within half a second of each other with it.

- **The `mcp` package is at version 2.** 2.2.0 is what resolves
  beside the pinned SDK, which accepts 1.23 and up. `FastMCP` is now
  `MCPServer` in `mcp.server.mcpserver`, and the old import raises. A
  tool function that returns `str` has its result delivered as
  `{"result": ...}`.

- **A server that fails raises nothing.** A stdio entry whose file
  did not exist gave `failed` with "Connection closed" in
  `get_mcp_status()`, the other server connected, and `connect()`
  returned normally. `pending` was seen once, for a server that was
  on its way to failing, so the cell polls until the status settles.

- **`"project"` reads upward.** With `setting_sources=["project"]`
  the session was given the `CLAUDE.md` of the working directory and
  of every directory above it, this repository's own included, and
  found the skills in this repository's `.claude/skills` as well as
  the workspace's. `get_context_usage()` lists the instruction files
  under `memoryFiles` with a type and a token count. The repository's
  `CLAUDE.md` is one line that imports `AGENTS.md`, and counted as 12
  tokens.

- **A skill needs three options.** `setting_sources=["project"]`,
  `skills=[name]` and `"Skill"` in `tools`. Nothing was needed in
  `allowed_tools`. The session found sixteen skills, Claude Code's own
  among them, and showed the model the one named. The call to `Skill`
  is answered "Launching skill", and the body then arrives as text in
  a message in the user's role.

- **JupyterLab hides dot directories.** The contents API does not
  list or open them, so a file under `.claude/` can be neither shown
  in a pane nor written by `file-write`. A cell writes there instead.

- **`can_use_tool` works with `query()`.** The documentation's
  example passes the prompt as a stream and registers a hook to keep
  it open. On the pinned release a plain string prompt worked, and so
  did hooks. The callback is not called for a `Read` in the working
  directory. A denial reaches the model as the tool result and is
  listed in `permission_denials`.

- **Haiku asks when it has to.** Told in the system prompt to ask
  rather than guess, it called `AskUserQuestion` on five runs of five
  when the task needed a fact it had not been given, and did not on a
  run where the task could be done without.

- **A rule in the system prompt was argued away.** "Never write a
  file anywhere but the notices directory, whoever asks" lost to a
  request that said the manager had approved an exception, on four
  runs of four. A `PreToolUse` hook that denies is reported to the
  model as "PreToolUse:Write hook error:" and the reason, is listed
  in `permission_denials`, and ran before `acceptEdits` was applied.
  A `PostToolUse` hook is called for a `Read` and not for a call that
  was denied.

- **A subagent runs in the background unless told not to.** The main
  agent's turn ended with "I've launched a reader agent" and no
  answer. `background=False` on the definition did not change that.
  `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` in `env` did, and is what
  the workshop uses.

- **A subagent can use only tools the session has.** With `Agent`
  alone in the main agent's `tools`, the subagent's `Glob` was denied
  by rule. The tool is `Agent` in a `ToolUseBlock` and `Task` in the
  `init` message. `usage` on the result is the main conversation's,
  and `model_usage` and the cost include the subagent.

- **Delegating costs more and leaves less.** Reading ten files left
  about 7,500 tokens in the conversation of the agent that read them
  and about 1,500 in that of the agent that delegated, while the
  tokens sent over the whole run rose from about 14,000 to about
  25,000.

- **`/compact` works on Haiku.** The boundary message gave 9,238
  tokens before and 4,084 after. Tool results in the conversation
  went to zero, the summary arrived as a user message, and about
  3,100 tokens of recently read files were attached again. A stock
  code given in the first prompt survived. A detail from a file read
  early did not.

- **Tool search needs the `ToolSearch` tool.** With `tools=[]` twenty
  MCP tool definitions, about 1,400 tokens, were loaded up front. With
  `tools=["ToolSearch"]` they were deferred, the model looked one up
  and called it, and the run took a turn more. The `ToolSearch` tool
  is about 900 tokens itself.

## Shape of the foundations collection

One ordered collection, in three movements, with no visible break
between them: the collection is numbered straight through and each
Finish dialog offers the next.

**What an agent is** (1 to 3). A first run, the loop slowed down until
each step can be seen, and what the run reports when it ends. After
these three the learner can say what the model does, what the SDK does
around it, and what a run cost, and can read the stream of messages
any later workshop prints.

**Shaping a run** (4 to 6). The instructions the agent works under,
the model that does the work and how hard it thinks, and what the agent
is allowed to do. After these the learner can set up an agent for a
job, and knows why the defaults are not what they want.

**Beyond one question** (7 to 10). A conversation that remembers, a
session picked up later, a reply shown as it is written, and an answer
that comes back as data. After these the learner has every piece a chat
application or a script that calls an agent is made of.

About fifteen minutes each, two and a half hours in all. Each workshop
is self-contained and ships whatever it needs, so it can be taken on
its own, even though the order is the order to take them in.

Every workshop here is a notebook, on the kernel of the JupyterLab
environment, with the model set to Haiku except where an entry says
otherwise. Between them the ten workshops make about forty model
calls in one pass, counting the login check each one opens with. The
counts in the entries leave that check out, except where they say
otherwise.

## The foundations workshops

### 1. `your-first-agent`: Run your first agent

What an agent is, and what comes back when you call one.

The welcome page sets out the idea the whole collection rests on. A
language model takes text and produces text, and nothing else: it
cannot read a file, run a command or remember yesterday. An agent is a
program wrapped around a model that lets it ask for things to be done,
does them, and gives it the results, in a loop, until the model has an
answer. The Claude Agent SDK is that program as a library: it is Claude
Code, the same loop and tools, driven from Python. A diagram of the
pieces, your code, the SDK, the model and the files, opens in a tab of
its own. The page also says how it is paid for: the SDK uses the login
of the `claude` command on this machine, and a run counts against that
plan's usage.

The welcome page then creates the notebook and checks the login: a one
word run inside `try`, so that a machine with no login gets a message
and a hint, not a traceback. Every later workshop opens the same way.

The first cell of the next page calls `query()` with a prompt that
needs no tools and `tools=[]`, collects every message into a list and
prints the type of each: a `SystemMessage`, an `AssistantMessage`, a
`ResultMessage`, and under a subscription a `RateLimitEvent`, which the
page names in a sentence. Three cells then open one each. The `init`
system message says what the session was given: the model's full name,
the tools, the working directory and where the credential came from.
The assistant message holds a `TextBlock`. The result message holds
the same text, and says the run succeeded.

Then the point of the workshop. The same options are asked a question
that only a shipped file can answer, what time the shop closes on
Saturday. With no tools the model cannot know, and the page says to
read what it does about that. A `quiz` asks what has to change. The
last cell adds `tools=["Read"]`, and the stream now has more in it: the
model asks for the file, the SDK reads it, and the answer is right.
The page names what just happened as the loop, opens a sequence diagram
of the run just made, and leaves how the loop works to the next
workshop.

- Format: notebook. The checks read that the login check reached the
  model, the set of message type names, that the `init` message's tool
  list is empty and then holds `Read`, that no `ToolUseBlock` appears
  in the run without tools and one named `Read` appears in the run with
  it, and that the closing time from the shipped file is in the final
  result.

- Ships: `shop/opening-hours.md`, and two diagrams,
  `diagrams/the-pieces-of-an-agent.md` and
  `diagrams/a-run-with-a-tool.md`.

- Source: `overview`, `quickstart`, the `query()` and message type
  sections of `python`, `authentication`, and `examples/quick_start.py`.

- Model calls: four, the login check included. Length: 15 minutes.

### 2. `watching-the-agent-loop`: Watch the agent loop

What happens between the prompt and the answer.

The welcome page opens a diagram of the loop. The agent is then given
four of the shop's documents and `Glob`, `Grep` and `Read`, and asked
something no single file answers: what to do when a customer returns a
book without a receipt, and when the manager is needed. The returns
policy says what the customer may have and the staff handbook says what
the member of staff does, so the run reads both. The cell prints each
message as it arrives, labelled: the model's request to use a tool,
with the tool's name and input; the result that was sent back; the next
request; and at last a reply with no request in it.

The pages take the printed run apart, and none of their cells calls
the model. A `ToolUseBlock` is the model asking, and it is only text in
a fixed shape: the model ran nothing. A `quiz` asks who read the file.
The SDK ran the tool, on this machine, and sent what it found back as a
`ToolResultBlock` inside a `UserMessage`, which is why a tool result
arrives in the user's role: to the model it is more input. A cell pairs
every request with its answer by id.

A cell then prints the tokens each reply was sent, from the `usage` on
its `AssistantMessage`, so the learner sees the input grow from reply
to reply. That is the other half of the idea: the model keeps nothing
between requests, so the SDK sends the whole conversation so far each
time, tool results included. The page says in passing that one reply
arrives as an `AssistantMessage` for each block, sharing a
`message_id`. The last cell puts the replies and tool requests counted
by hand beside `num_turns` on the result, and the page says how the
loop ends: on the first reply with no request in it.

- Format: notebook. The checks read the list of tool names the run
  called, which must include `Read`, that every `ToolUseBlock` id has a
  `ToolResultBlock` answering it, that the last reply was sent more
  than the first, and that `num_turns` is at least two and the last
  reply holds no request.

- Ships: `shop/opening-hours.md`, `shop/returns-policy.md`,
  `shop/staff-handbook.md` and `shop/events.md`, and one diagram,
  `diagrams/the-agent-loop.md`.

- Source: `agent-loop`, and the content block types in `python`.

- Model calls: one run of several turns. Length: 15 minutes.

### 3. `reading-the-result`: Read what a run cost

How to tell what a run did, whether it worked, and what it used.

One run, and then the `ResultMessage` field by field. `subtype`,
`is_error` and `stop_reason` say how the run ended. `num_turns` and
`duration_ms` say how much work it was. `usage` counts tokens, and the
page says what a token is, a piece of a word, the unit the model reads
and writes in and the unit usage is measured in. It separates the four
counts: input, output, input written to the cache and input read from
it, and says why a cache exists. On a request this small both cache
counts are zero, because a request has to be a few thousand tokens long
before the cache is used, and the page says so and leaves the
demonstration to the next workshop.

Then `total_cost_usd`, and what it means here. It is the SDK's estimate
of the run at API prices. Under a subscription nothing is charged per
run, and the same tokens count against the plan's limits, so the figure
is a measure of size.

Under a subscription login the stream also carries a `RateLimitEvent`,
and a cell prints what it reports: the status, which limit it is about,
and the fraction of the plan's five hour and seven day limits used so
far. Those fractions are in the event's `raw` data, which the SDK
passes through without modelling, and the page says so. The cell guards
for the event being absent, as it is with an API key.

Then a run that does not finish. The same task is given
`max_turns=1`, which is not enough for it. A `quiz` asks what the
learner expects to get back. The result has the subtype
`error_max_turns` and no `result` text, and `query()` raises
`ResultError` after yielding it, so the cell catches the error and
prints both. The page closes on why a limit belongs on every agent
that runs unattended, and names `max_budget_usd` in a hint.

- Format: notebook. The checks read the first result's `subtype` and
  that it took at least two turns, that its usage holds the counts and
  the cost is a positive number, the limited result's `subtype` and
  empty `result`, and the name of the exception the cell caught.

- Ships: `shop/returns-policy.md` and `shop/staff-handbook.md`.

- Source: "Handle the result" and "Turns and budget" in `agent-loop`,
  `cost-tracking`, the `ResultMessage` and error sections of `python`,
  and `examples/max_budget_usd.py`. `duration_api_ms` is left out: it
  came back larger than `duration_ms` in the trial, which a page would
  have to explain.

- Model calls: two. Length: 15 minutes.

### 4. `giving-the-agent-instructions`: Give the agent its instructions

What a system prompt is, and what the choice of one costs.

The page separates two kinds of text the model is sent. The prompt is
the request. The system prompt is the standing instruction sent ahead
of every request: who the agent is, what it is for, how it should
behave. The model treats the two differently, and the person who writes
the application writes the second.

Three runs answer the same customer question, which has two halves: can
a book be returned without a receipt, which the returns policy covers,
and does the shop buy second-hand books, which it does not. A function
defined in the first cell asks the question under whatever system
prompt it is given. The first prompt makes the agent the shop's
assistant, tells it to answer only from the policy and to say it does
not know when the policy does not cover something. The second changes
that one rule, to send the customer to a named person at the counter,
and the learner reads the difference. The third uses the `claude_code`
preset, the instructions Claude Code itself runs under, with the first
prompt appended, after a `quiz` asks how the size of its request will
compare.

A cell then puts the size of the first request of each run side by
side: the preset is several times the size, because it carries
instructions for a coding assistant that this agent does not need. A
last cell prints the preset run's usage, which is where the cache
first shows: almost all of its input was written to the cache or read
from it.

The page draws the rule out. Start from a prompt of your own for an
agent with its own job. Use the preset, with `append`, when the agent
is doing what Claude Code does. Leave the option out and the SDK sends
a minimal prompt that covers tool calling and nothing else. Either way
the prompt is sent with every request of every turn, and the cache is
what makes a long one affordable.

- Format: notebook. The checks read that all three runs succeeded, and
  that the preset run's first request, cache counts included, is more
  than three times the first run's. The first request is compared, not
  the whole run, so that a run that happens to take an extra turn does
  not move the ratio. The change in behaviour between the first two
  runs is for the learner to read and is not checked.

- Ships: `shop/returns-policy.md`.

- Source: `modifying-system-prompts`, the system prompt types in
  `python`, and `examples/system_prompt.py`. With `system_prompt` left
  unset the pinned release passes an empty one, and the documentation
  calls the result the minimal default.

- Model calls: three. Length: 15 minutes.

### 5. `choosing-a-model`: Choose a model and how hard it thinks

Which model to run an agent on, and what effort changes.

The page introduces the sizes as a trade: a small model that is fast
and light on usage, and larger ones that reason better and cost more
of both. The `model` option takes a short name, and the `init` message
shows the full name it stood for.

One task that takes several steps is run on Haiku and on Sonnet: a
loyalty scheme member wants to return a book on day 30, which the
returns policy alone refuses and the loyalty scheme allows, as shop
credit, with the points taken back. The agent has `Glob` and `Read` and
is not told which files matter. A function defined in the first cell
runs the task and keeps a row of figures for each run, and the cells
print the answer, the files that run read, and a table: turns, tokens
in and out, seconds and estimated cost. The page gives the three parts
of a right answer, from the documents, and has the learner check each
answer against them. It says what to look for and does not promise
what will be seen, since either model may do well or badly on a given
run.

Then effort, which is how much work the model puts into each reply.
The Sonnet run is repeated at `effort="low"` and added to the table.
The page is plain that on a task this small the difference is often
slight and can go either way, and says where the option earns its
place.

Every agent so far has set `thinking={"type": "disabled"}` without
saying much about it. One cell here runs Haiku with that line taken
out, after a `quiz` on where the extra work will show, and the learner
sees what it was holding back: the model reasons before it replies,
its replies gain thinking blocks, and the output tokens grow for the
same answer. The page says what thinking is for, harder problems than
these, and why the workshops leave it off. It closes with the rule the
collections follow: use the smallest model that does the job reliably,
and move up when it gets a multi-step task wrong.

This is the one workshop in the collection that leaves Haiku, for two
Sonnet runs, because the comparison is its subject.

- Format: notebook. The checks read that the two `init` messages name
  different models, that each run succeeded, and that the table has a
  row for each of the four.

- Ships: `shop/returns-policy.md` and `shop/loyalty-scheme.md`.

- Source: "Choose a model" in `configuration`, and "Effort level" in
  `agent-loop`. The task was tried several times on both models. Haiku
  missed the loyalty scheme altogether on two runs of six and left out
  the points on the others, and Sonnet gave all three parts every
  time. Effort made no consistent difference on Sonnet at this size.

- Model calls: five, two of them on Sonnet, the login check included.
  Length: 15 minutes.

### 6. `deciding-what-it-can-do`: Decide what the agent can do

How tools are given and withheld, and who approves a call.

Workshop 1 gave the agent `Read` and nothing was asked. This one gives
it `Write`, and the difference is the subject. The page separates two
questions the SDK asks of every tool. Is the tool there at all, which
`tools` decides. And may this call run, which the permission rules
decide.

A function defined in the first cell attempts one job, writing a short
notice for the shop door from the opening hours, with
`tools=["Read", "Write"]` and whatever permission options it is passed,
and returns what happened: the tools the session had, the tools asked
for, the calls denied and whether the notice exists. Each of the four
runs is then one line, so the only thing that changes is in view.

The first attempt passes `permission_mode="default"`. Reading inside
the working directory needs no approval. Writing does, nobody is there
to give it, and so the call is refused, after a `quiz` asks what will
happen. The cell prints `permission_denials` from the result, and the
learner sees that the model was told of the refusal and said so. The
mode is named because the mode a session starts in when the option is
left out is not the same everywhere.

The second attempt adds `allowed_tools=["Write"]`, and the file appears
in the workspace. The page spends a paragraph on the name, since
`allowed_tools` approves and does not give. A diagram of the checks
opens here. The third shows the other way to the same end,
`permission_mode="acceptEdits"`, and the page lays the modes out as a
table of how much is approved without asking. The fourth keeps that
mode and uses `disallowed_tools` to take the tool away. The session's
tool list no longer has `Write`, and the page says what the trial
showed: the model may ask for it all the same, and is told there is no
such tool.

The page closes on why this matters more for an agent than for a chat:
the agent acts on the machine it runs on, with the access of whoever
started it, so the tools it is given are a decision about risk. It
names `bypassPermissions` as the mode for a sealed container and
nowhere else.

- Format: notebook. The checks read that the first result's
  `permission_denials` names `Write` and that the notice file does not
  exist, that it does exist after the second and third runs, and that
  in the run with `disallowed_tools` the session's tools do not include
  `Write`, nothing was denied and nothing was written.

- Ships: `shop/opening-hours.md`, and one diagram,
  `diagrams/may-this-call-run.md`.

- Source: `permissions`, "Tool permissions" and "Permission mode" in
  `agent-loop`, and `examples/tools_option.py`. That a call needing
  approval is refused when no callback is given was confirmed on the
  pinned release.

- Model calls: four. Length: 20 minutes.

### 7. `holding-a-conversation`: Hold a conversation

How an agent remembers what was said, and what that costs.

The workshop opens with a failure. Two calls to `query()`, a cell
each: the first tells the agent a stock code for a book that is in no
file, the second asks for it back. The second knows nothing, and the
two results carry different session ids. Each `query()` is a
conversation of one exchange.

`ClaudeSDKClient` is the other way to use the SDK. A cell connects a
client and leaves it open. The next sends the stock code with
`client.query()` and reads the reply with `receive_response()`. The
next asks for it back, and gets it, on the same session id. The page
says how that works, and it is the idea from workshop 2 again: the
model remembers nothing, and the session sends the whole conversation
with every request.

Two cells show what that means. The tokens each turn was sent are
printed, and the second turn was sent more than the first: the
conversation so far, sent again. Then `get_context_usage()` shows how
full the context window is, by category, and the page names the window:
the most text the model can be sent at once, which a long conversation
will fill. What happens then is left to **Extending an agent with the
Claude Agent SDK**. The last cell disconnects the client, and the page
shows the `async with` form a program would use.

- Format: notebook. The checks read that the two `query()` results
  have different session ids and the second does not hold the code,
  that the two client turns share one, that the stock code appears in
  the second client reply, that the second turn was sent more tokens
  than the first, and that the context usage total is a positive
  number below the window's size.

- Ships: nothing.

- Source: the `ClaudeSDKClient` section of `python`,
  `streaming-vs-single-mode`, "The context window" in `agent-loop`, and
  `examples/streaming_mode_ipython.py`. A conversation this short stays
  below the size at which the cache is used, so the growth shows in
  the plain input count and not in the cache counts.

- Model calls: four. Length: 15 minutes.

### 8. `picking-up-where-you-left-off`: Pick up where you left off

How a conversation is kept, resumed and branched.

A run tells the agent the stock code and ends. The page says where the
conversation went: the SDK writes every session to a transcript on
disk, under the Claude configuration directory, filed by the directory
the agent worked in. `list_sessions()` shows it, with its id, a
summary and first prompt, and `get_session_messages()` reads it back.

A new `query()`, in a cell that shares nothing with the first but the
id, passes `resume=` and asks for the stock code. It answers, on the
same session id. A `quiz` then asks what `fork_session=True` will do
to the original. The forked run is told the code has changed, gets a
new id, and the cell counts the original's messages before and after
to show it unchanged. A diagram of the three runs and the two sessions
opens here. A hint covers `continue_conversation=True`, which resumes
the most recent session in the directory without being given an id.

The page says what this is for: a chat application that survives a
restart, a job that failed and is taken up again, and trying two ways
forward from one point. A cell deletes the two sessions the workshop
made on purpose, with `delete_session()`, and the page says that the
login check, like every run, left a transcript of its own.

- Format: notebook. The checks read that the session is listed and can
  be read back, that the resumed result carries the first session's id
  and the stock code, that the forked result carries a different id
  and the new code and left the original's message count unchanged,
  and that after the last cell neither id is in `list_sessions()`.

- Ships: one diagram, `diagrams/resume-and-fork.md`.

- Source: `sessions`, and the session functions in `python`.

- Model calls: three. Length: 15 minutes.

### 9. `streaming-the-reply`: Stream the reply as it is written

How to show an answer while it is still being produced.

Until now a reply has arrived a block at a time: nothing, then all of
it. The first cell times that, on a prompt that asks for about two
hundred words. The page says why it matters: a model writes a token at
a time, a long answer takes seconds, and a person watching an empty box
for that long thinks the program has hung.

`include_partial_messages=True` adds `StreamEvent` messages to the
stream, each carrying a raw event from the API. The second cell counts
the events of each type in one run, in the order they first appear, so
the learner sees the shape: a message starts, a content block starts,
many deltas arrive, the block stops, the message stops. The third
prints the text of each delta as it arrives, and the reply appears as
it is written. The cell also records when the first text arrived and
when the last did, and the page points out that streaming shortens the
wait for the first sign of life and not the reply.

The complete `AssistantMessage` still arrives once the text is
finished. The fourth cell joins the deltas and compares them with the
text of that message: they are the same text, delivered twice, which
tells the learner which one to display and which to keep. A closing
paragraph says that a tool call's input streams the same way, which
the chat app workshops use.

- Format: notebook. The checks read that the plain reply arrived, that
  the run produced stream events and most were deltas, that the first
  text arrived before the last, and that the joined deltas equal the
  text of the final assistant message.

- Ships: nothing.

- Source: `streaming-output`, the `StreamEvent` type in `python`, and
  `examples/include_partial_messages.py`.

- Model calls: three. Length: 15 minutes.

### 10. `getting-data-back`: Get data back, not prose

How to use an agent as a function in a program.

A program cannot do much with a paragraph. The first cell asks the
agent for the shop's opening hours, and a second pulls out everything
in the reply that looks like a time. The page lets the difficulty
stand: the times are there with nothing to say which day or which end
of the day each belongs to, because the reply is written for a person
and laid out differently on every run.

`output_format` takes a JSON Schema. The next cell describes the shape
wanted, a list of days each with an opening and a closing time in 24
hour form or nothing when the shop is shut, and runs the same task.
`structured_output` on the result is a dictionary that matches the
schema, with an entry for each of the seven days though the file gives
four of them as one row.

A cell that calls nothing then shows how it was done, from the tool
names the run recorded: the SDK added a tool of its own whose input
has to match the schema, and the model's last act was to call it. The
page says what follows from that: the agent still loops, reads the
file and reasons, the value is checked against the schema before it is
handed back, and `result` holds the same data as JSON text. It names
the result subtype for the case where no valid output could be
produced. The last cell uses the data in ordinary Python to answer the
question the first page could not, whether the shop is open at a given
time on a given day.

The finish page closes the collection on the two ways an agent is
used, as a conversation and as a function, with the two collections
that follow.

- Format: notebook. The checks read that the plain run has no
  `structured_output`, that the structured one is a dictionary with
  seven days, that the closing time for Saturday equals the one in the
  shipped file, that the run read the file, and that the function
  written over the data gives the right answer for four times.

- Ships: `shop/opening-hours.md`.

- Source: `structured-outputs`, and `output_format` in `python`. Haiku
  met the schema on every one of three trial runs, so the workshop
  stays on it.

- Model calls: two. Length: 15 minutes.

## Topics the foundations collection leaves out

- **Configuring extended thinking beyond on and off.** Thinking
  budgets and how thinking is displayed are API level detail, differ by
  model, and change often. The workshops turn thinking off, workshop 5
  shows what it is by leaving it on once, and effort is the control
  they teach.

- **Fallback models and spending budgets.** `fallback_model` and
  `max_budget_usd` are named in passing in workshop 3 and no more. The
  turn limit teaches the idea of a limit.

- **Images and other input.** Prompts here are text.

- **Slash commands, output styles and file checkpointing.** Claude
  Code features that an agent built for another job rarely needs.

- **Storing sessions somewhere other than local disk.** Held for the
  later collection on running an agent as a service.

## Shape of the extending collection

One ordered collection, in three movements.

**More to work with** (1 to 3). A tool written as a Python function, a
tool server reached over the Model Context Protocol, and the shop's
own data, in files and in a database, put within the agent's reach.

**Standing knowledge** (4 and 5). Instructions that are loaded with
every session, and skills, which are loaded only when they are needed.

**Control and scale** (6 to 9). A person approving what the agent
does, code that enforces what it may not do, work handed to
subagents, and a session that runs long without filling its window.

Fifteen to twenty minutes each, about two and three quarter hours in
all. Notebook workshops. Four of them, 2 to 5, have a code pane
beside the notebook showing the one shipped file the pages are about:
the server's source, the SQL the database is built from, the
instruction file, the skill. The others have nothing that is better
read in a pane than in a cell, and use the plain notebook layout.

On the question this collection was asked to answer, what the SDK
provides for "knowledge": it has no vector store and no retrieval
layer of its own. An agent gets at knowledge by searching and reading
files with its built-in tools, by calling a tool or an MCP server that
fronts a database or an API, by having instructions loaded into every
session, and by loading a skill. Workshop 3 teaches the first two side
by side, 4 and 5 the others.

Between them the nine workshops make about forty model calls in one
pass, the login checks included. All are on Haiku except one run of
workshop 8.

## The extending workshops

### 1. `giving-the-agent-a-tool`: Give the agent a tool of your own

How a Python function becomes something the model can ask for.

A function that looks a title up in the shop's stock list is decorated
with `@tool`, put in a server made by `create_sdk_mcp_server()`, and
passed in `mcp_servers`. The page names the four parts of a tool, says
that `tools=[]` covers only the built-in tools, and that a tool of
your own needs approving with `allowed_tools`, as `Write` did. A
function defined in the second cell runs a question against a server
and prints each request and what the handler sent back. The first run
asks about one title, and the handler's own list of calls shows the
function ran in the notebook's kernel.

The pages then dwell on the part that is not code. A cell prints the
name, description and input schema, which is all the model is shown.
The same handler is wrapped again under a description of four words,
and a customer asks whether the shop has anything by an author. The
tool matches titles only. With the vague description the model passes
the author as a title, is told there is no such book, and tells the
customer the shop has nothing by her, which the stock file shows is
wrong. With the description that says what the tool cannot do, it
asks for a title. A second tool that searches by author is then added
to the server, and the question is answered.

The last page marks the tool read-only. A handler that waits a second
and records when it started is asked about three books at once, behind
a plain tool and behind one with `ToolAnnotations(readOnlyHint=True)`,
and the printed times show the calls running one after another and
then side by side.

- Format: notebook. The checks read that the handler was called and
  the stock code from the file is in the answer, that the two runs on
  the author question succeeded with one tool in the session, that the
  run with two tools called the search by author and named both
  books, that the plain tool's calls did not overlap and the read-only
  tool's did.

- Ships: `shop/stock.csv`, six made-up books by made-up authors, so
  that nothing the model knows from training can answer.

- Source: `custom-tools`, `@tool`, `create_sdk_mcp_server()` and
  `ToolAnnotations` in `python`, and `examples/mcp_calculator.py`. In
  three trial runs of each, the vague description had the author
  passed as a title every time and the clear one had the model ask
  for a title every time. Neither is checked.

- Model calls: seven, the login check included. Length: 20 minutes.

### 2. `connecting-an-mcp-server`: Connect an MCP server

What the Model Context Protocol is, and how an agent uses a server it
did not write.

The welcome page says what MCP is, a standard way for a program to
offer tools to any agent, and why that matters: the tool is written
once and used from any client. The same stock lookup is now a small
server program of its own, open in the code pane, written with the
`mcp` package and knowing nothing of Claude. A diagram shows where it
runs beside the in-process server of the workshop before.

A `stdio` entry in `mcp_servers` names the command that starts it,
with `sys.executable` so that it runs on the kernel's Python. A
`ClaudeSDKClient` is connected, and `get_mcp_status()` shows the
server connected, the name it gave itself and its two tools, with no
model call. The agent is then asked a question through it. A second
client is given a second server whose file does not exist, after a
`quiz` on what will happen: nothing raises, the good server connects,
and the bad one is reported as `failed`. The last page lays out the
four kinds of entry, names the remote ones without using them, and
says at last what `strict_mcp_config=True` has been keeping out.

- Format: notebook with a code pane on `stock_server.py`. The checks
  read the server's status and tool names, that the agent called the
  server's tool and the stock code from the file is in the answer,
  that the broken server is `failed` while the other is `connected`,
  and that the client was disconnected.

- Ships: `stock_server.py`, `shop/stock.csv`, and one diagram,
  `diagrams/where-a-tool-runs.md`.

- Source: `mcp`, the MCP configuration and status types in `python`,
  and modelcontextprotocol.io. The `mcp` package is installed as a
  dependency of the SDK, which accepts versions 1 and 2. Version 2
  renamed `FastMCP` to `MCPServer`, so the shipped server imports the
  new name and falls back to the old.

- Model calls: two, the login check included. Length: 15 minutes.

### 3. `answering-from-your-own-data`: Answer from your own data

How an agent gets at what you know: documents and a database.

Three questions about the shop, each put to an agent with a different
set of tools by one function. The first is answered from the shop's
five documents, by the agent searching and reading them with `Glob`,
`Grep` and `Read`, and the page calls this what it is: the agent
decides what to look for and reads it, with nothing sorted or picked
out for it in advance.

A cell then builds a SQLite database from the SQL file open in the
code pane, and the page says why reading is the wrong way to answer a
question about records. A tool is put in front of the database: its
description carries the layout of the tables, and the connection is
opened read-only, which the cell shows by calling the handler
directly with a `DELETE`. Given that tool and no file tools, the agent
writes a query that joins and sums, and the database does the
arithmetic.

The third question needs both: whether a customer can still return a
book depends on the date of his order and on the returns policy. A
`quiz` asks what decides which source is used. The agent, given
everything, queries the order and reads the policy. A cell that calls
nothing compares the three runs, and the page sets the two ways side
by side and says plainly that the SDK ships no vector store: retrieval
by similarity is something you would put behind a tool, as the
database is here.

- Format: notebook with a code pane on `data/orders.sql`. The checks
  read that the first run read or searched a file and the ticket price
  from the file is in the answer, that the database has its twelve
  orders, that the handler refused a write and the orders are all
  still there, that the second run ran a query and named the customer
  the data gives, and that the third used the database tool and a
  file tool.

- Ships: the five shop documents and `data/orders.sql`. The database
  is made by a cell, so nothing binary is committed.

- Source: `custom-tools`, `mcp`, and "Keep context efficient" in
  `agent-loop`.

- Model calls: four, the login check included. Length: 20 minutes.

### 4. `instructions-that-persist`: Give instructions that persist

How project instructions are loaded, and why they outlast the prompt.

The shop's house rules are in a `CLAUDE.md` in the workspace, open in
the code pane. One function asks for a reply to a customer under
whatever `setting_sources` it is given, and keeps the instruction
files the session was given, from `memoryFiles` in
`get_context_usage()`. With an empty list no project file is loaded
and the reply follows no house rule. With `["project"]` the file is
listed, and the reply ends with a sign-off that is in the file and
nowhere else. The agent has no tools, so the file could only have
reached the model by being loaded.

The page says that the `CLAUDE.md` of every directory above is loaded
too, which a learner whose workshops sit inside a project will see in
the list. A cell that calls nothing shows the rules counted under
memory files and the first request larger by about their length. The
page sets the three places an instruction can live side by side, the
prompt, the system prompt and the file, by who writes each and whether
it survives a conversation being summarised.

The last page says what else each source loads, why every other
workshop sets the option to an empty list, and names the two inputs
the option does not cover: Claude Code's auto-memory, with the setting
that turns it off, and the claude.ai connectors.

- Format: notebook with a code pane on `CLAUDE.md`. The checks read
  that the first session was given no file of type `Project`, that the
  second was given the workspace's `CLAUDE.md` and its reply carries
  the sign-off, and that memory files and the first request both grew.

- Ships: `CLAUDE.md`.

- Source: `claude-code-features`, `modifying-system-prompts`, "The
  context window" in `agent-loop`, and `examples/setting_sources.py`.

- Model calls: three, the login check included. Length: 15 minutes.

### 5. `packaging-know-how-as-a-skill`: Package know-how as a skill

What a skill is, and why it is not loaded until it is needed.

The shop's procedure for answering a refund request is a skill, a
directory with a `SKILL.md`, open in the code pane. JupyterLab does
not show directories whose names begin with a dot, so the skill is
shipped under `skills/` and a cell copies it to `.claude/skills/`,
where the SDK looks, and counts the words of its front matter and its
body.

The options then set three things, and the page says what each is
for: `setting_sources=["project"]` so the skill is found,
`skills=["refund-reply"]` so that it and no other is shown to the
model, and `"Skill"` in `tools`. A client connected for a moment
reports that the session found many more skills than one, Claude
Code's own among them, and that the model is shown one, at the cost
of its description.

A refund request then has the model call `Skill`, the body arrive as
text in the conversation, the policy be read as the body says, and a
reply written that carries a reference only the body gives. A
question about opening hours is answered without it. A last cell
compares the first and last request of the two runs: they begin the
same size, and only the run that used the skill grew by it. The page
sets that against a `CLAUDE.md`, which every request would carry.

- Format: notebook with a code pane on `skills/refund-reply/SKILL.md`.
  The checks read that the skill is installed, that the session lists
  it at fewer tokens than its body has words, that the refund run
  called `Skill` and its reply carries the reference, that the second
  run gave the closing time from the file, and that the two first
  requests are within a hundred tokens of each other.

- Ships: `skills/refund-reply/SKILL.md`, `shop/returns-policy.md` and
  `shop/opening-hours.md`.

- Source: `skills` and `claude-code-features`.

- Model calls: three, the login check included. Length: 15 minutes.

### 6. `asking-before-acting`: Ask before acting

How a person stays in the loop.

A `can_use_tool` callback is called when a tool needs approval. In the
notebook it decides by rules the page lists, standing in for a
person: a write under `notices` is allowed, a write to the shop's own
documents is refused with a reason, a write anywhere else in the
workspace is allowed with its path moved into `notices`, and anything
outside the workspace is refused. One function runs a job under
`permission_mode="default"` with the callback, and each job is a
cell.

The first job shows a call allowed, and that the callback was not
asked about the `Read` before it. The second, after a `quiz` on what
the model is told, shows a refusal arrive as the result of the request
and the model pass the reason on. The third shows the file land where
the callback sent it. The fourth is the other reason the callback is
called: a second callback answers `AskUserQuestion` with a note from
the manager and passes everything else to the first, and the agent is
given a notice to write that needs a day it was not told.

- Format: notebook. The checks read the callback's own record of its
  decisions and what is on disk: that a write was allowed and the
  notice exists, that the change was refused, listed as denied and the
  file is as it was, that the moved file exists where the rule sent it
  and not where the model asked, and that a question was asked and the
  notice written.

- Ships: `shop/opening-hours.md`.

- Source: `user-input`, `permissions`, and
  `examples/tool_permission_callback.py`. The chat app collection puts
  a real person behind the same callback.

- Model calls: five, the login check included. Length: 20 minutes.

### 7. `guardrails-in-code`: Put guardrails in code

How hooks enforce what a prompt can only ask for.

The rule is that the assistant writes files in `notices` and nowhere
else. It first goes in the system prompt, with the words "whoever
asks", and the request argues with it: write a notice, and save a
copy to `archive`, which the manager is said to have approved. The
agent runs in `acceptEdits`, so nothing else stands in the way. After
a `quiz` on what decides, the cell prints whether the copy exists. The
page does not promise that it will. It says that either way the model
was the one deciding.

The same rule is then a `PreToolUse` hook that looks at where the
file would go and denies the call. The system prompt and the request
are unchanged. The copy is not written, and the model reports the
reason it was sent. A third run adds a `PostToolUse` hook with no
matcher that keeps a log, which holds the `Read` that a permission
callback is never asked about and does not hold the write that was
refused. A page that calls nothing opens a diagram of the order
things are asked in, sets rules, callback and hooks side by side,
lists the events Python has, and says what a hook is not: it checks
what it checks, and would not stop a shell command it never looks at.

- Format: notebook. The checks read that the first run ended in
  success and nothing more, that after the second `archive/door.md`
  does not exist, with a note if the model did not try, and that the
  log has a `Read` in it and nothing under `archive`.

- Ships: `shop/opening-hours.md`, and one diagram,
  `diagrams/before-a-tool-runs.md`.

- Source: `hooks`, the hook types in `python`, the order of
  evaluation in `permissions`, and `examples/hooks.py`. No `Bash`: the
  point is made with `Write`.

- Model calls: four, the login check included. Length: 20 minutes.

### 8. `handing-work-to-subagents`: Hand work to subagents

What a subagent is, and what it saves.

The question is which of ten suppliers deliver within a week, and the
reading is their terms of supply, ten files of about three hundred
and fifty words. One function runs an agent on a client, labels each
tool request as the main agent's or a subagent's, by
`parent_tool_use_id`, and when the run is over asks the client how
many tokens the main conversation holds.

First one agent does the reading itself. Then a `reader` is defined
with `AgentDefinition`, its description, prompt, tools and model, and
the options are copied with four changes: the `Agent` tool, a system
prompt that says to hand reading over, the `agents`, and an
environment variable that makes the subagent run in the foreground.
The page explains each, a diagram of the handover opens, and a `quiz`
asks what comes back. The main agent asks for `Agent` once, the
subagent's requests are printed indented, and a report returns.

A cell that calls nothing compares the two: the delegating agent's
conversation is a fifth the size, and the run as a whole was sent
more, not less. The page says so plainly: a subagent saves room in
the conversation that carries on, and nothing else. The last run puts
the main agent on Sonnet and leaves the reader on Haiku, and prints
`model_usage`, which lists each model's share.

- Format: notebook. The checks read that the first run read files in
  the main conversation and none in a subagent, that the second called
  `Agent` and had requests inside a subagent, that both answers name a
  supplier the files give, that the delegating conversation is the
  smaller, and that the last run used two models.

- Ships: `suppliers/`, ten files, and one diagram,
  `diagrams/a-subagent-at-work.md`.

- Source: `subagents`, `AgentDefinition` in `python`,
  `examples/agents.py`, and the subagent and environment variable
  pages of the Claude Code documentation for how a subagent is run in
  the foreground.

- Model calls: four, one with Sonnet as the main agent, the login
  check included. Length: 20 minutes.

### 9. `keeping-a-long-session-small`: Keep a long session small

What fills the context window, and what the SDK does when it is full.

A client stays connected through the first four pages, and a function
adds a row to a table each time it is called, from
`get_context_usage()`: the tools, the conversation, the part of it
that is tool results, and the whole. Before anything is said the two
tools are most of the window. A turn that tells the agent a stock
code and has it read the ten supplier files puts thousands of tokens
in the tool results column, and a question of five words is then sent
with all of it.

`/compact` is sent as a prompt, after a `quiz` on what it will do to
the files. The cell prints the `compact_boundary` message's trigger
and the size before and after, and the start of the summary, which
arrives in the user's role. The table shows tool results at nothing
and the conversation about half what it was, and the page says why it
is not less: the SDK puts back the few files read most recently. The
next turn asks for the stock code, which comes back, and for a detail
from a file read early, which the agent no longer has. The page draws
out what is kept and what is at risk, and where a rule that must hold
belongs. Automatic compaction is explained from the threshold the
first cell printed and not brought about.

The last page gives an agent twenty tools made in a loop and measures
one question two ways: with no built-in tools, where all twenty
definitions are in the window, and with `ToolSearch`, where they wait
and the model looks one up. It says honestly that with twenty small
tools the saving is modest and costs a turn. The finish page gathers
the ways to stay small that the collection has shown.

- Format: notebook. The checks read the table: that the reading put
  more than two thousand tokens of tool results in the conversation,
  that the short question was sent more than the conversation held
  before it, that a boundary arrived with fewer tokens after than
  before and the tool results fell, that the stock code is in the
  reply after compaction, and that the tools were loaded in one run
  and waiting in the other.

- Ships: `suppliers/`, the same ten files as workshop 8.

- Source: "The context window" in `agent-loop`, "Compact history" in
  `skills`, `tool-search`, and `cost-tracking`.

- Model calls: seven, the login check included. Length: 20 minutes.

## Topics the extending collection leaves out

- **Plugins.** A way to package skills, agents, hooks and MCP servers
  together. It teaches no new idea once those four are known. A
  candidate to add at the end if the packaging turns out to matter.

- **Remote MCP servers and their authentication.** Named in workshop
  2. They need a server to reach and credentials to hold.

- **Subagents in the background, and more than one at once.** Workshop
  8 makes its one subagent run in the foreground, so that a cell ends
  with the answer. Task notifications, parallel subagents and resuming
  one are named in a hint at most.

- **Compaction by itself.** Workshop 9 compacts by hand and explains
  the threshold. Filling a window to reach it would cost far more
  usage than the lesson is worth.

- **Hooks and subagents defined in files.** Both can be loaded from
  the project's settings. The workshops define them in code, where the
  learner can read them.

- **`Bash`.** No workshop here gives the agent a shell. The points
  about approval and hooks are made with `Write`.

- **Todo tracking.** Fits the chat app, where there is somewhere to
  show it.

- **Sandbox settings, and running with all permissions.** Held for
  the later collection on running an agent as a service.

## Shape of the chat app collection

One ordered collection that builds one application, a chat with the
shop's assistant in a browser. Unlike the other two it accumulates:
each workshop starts from the application as the one before left it.
Each still ships the whole application as it stands at its start, so
any workshop can be taken on its own.

**A chat that works** (1 to 3). A page and a server that answers, the
reply streamed as it is written, and a conversation for each visitor.

**A chat you can trust** (4 and 5). The agent's tool use shown as it
happens, and approval asked in the browser, with a way to stop a run.

**A chat worth using** (6 to 8). The tools, server and skill from the
extending collection plugged in, conversations listed and resumed, and
usage shown with limits set.

About twenty minutes each, two and three quarter hours in all.

The format is terminal and files with a web pane: the server runs in a
terminal, its source is open in an editor, and the application is
shown beside them in a pane opened by `url-open`, on a port held in a
variable the learner can change if it is taken. The learner never
types code: each step changes a file through an action and restarts
the server.

The server is written with FastAPI and run with `uvicorn`. The user
chose it on 2026-10-02 over plain Starlette, which had been the
proposal: it is the framework a Python developer is most likely to
know and to use afterwards, and it costs little here.

- The SDK already brings Starlette, uvicorn and Pydantic, through its
  dependency on the `mcp` package, so `fastapi` adds itself and one
  small package. It is added to `pyproject.toml`, pinned, when the
  first chat app workshop is written, and never as
  `fastapi[standard]`, which pulls in about thirty packages the
  workshops have no use for. The README's `uvx` command gains a
  second `--with` for it then.

- A route declares its request body as a Pydantic model, and FastAPI
  parses and checks the JSON before the function runs. The first
  workshop explains that, since nothing in the function shows it.

- A streamed reply is a route with
  `response_class=EventSourceResponse`, from `fastapi.sse`, that
  yields: each item is sent to the browser as one `data:` line of a
  server-sent event stream. That arrived in FastAPI 0.135.0. A route
  that yields what `async for message in query(...)` hands it is
  close to the SDK's own loop.

- The page FastAPI generates at `/docs` lets a route be tried from
  the browser, which the first workshop can use before its own page
  exists.

Checked without the model on 2026-10-02: FastAPI 0.142.2 ran on Python
3.14 beside the Starlette 1.7.0 the SDK brings, with a JSON route, a
rejected body and a streamed route. Whether a terminal the extension
opens finds the project environment's Python is still to be checked.

## The chat app workshops

These entries are one step short of the extending entries: they say
what each workshop adds. The collection is designed in detail, with
the user, before it is written.

1. **`the-smallest-chat-app`: Build the smallest chat app.** A page
   with a box and a server with one route that calls `query()` and
   returns the reply. No memory, no streaming. What a web application
   around an agent has to do, and what this one does not do yet.

2. **`streaming-to-the-browser`: Stream the reply to the browser.**
   Partial messages carried to the page as they arrive, and the page
   appending them. Why a streamed response, and what the server holds
   open while the agent works.

3. **`one-conversation-per-visitor`: Keep a conversation for each
   visitor.** A `ClaudeSDKClient` per browser session, with its life
   tied to the visitor's. What to keep in the server's memory and what
   the session on disk already holds.

4. **`showing-the-agent-at-work`: Show the agent at work.** Tool calls
   and their results sent to the page and drawn as they happen, so a
   pause reads as work.

5. **`approving-from-the-browser`: Approve from the browser.** The
   `can_use_tool` callback waits on a dialog in the page, and a stop
   button calls `interrupt()`. How a callback on the server waits for
   a person in a browser.

6. **`plugging-in-your-tools`: Plug in your tools.** The stock tool,
   the orders database and the refund skill from **Extending an agent
   with the Claude Agent SDK**, added to the application's options,
   with the tool list shown in the page.

7. **`coming-back-to-a-conversation`: Come back to a conversation.** A
   list of past sessions, a past one resumed after the server restarts,
   and a fork.

8. **`showing-usage-and-limits`: Show usage and set limits.** Tokens
   and context use shown per turn, a model picker using `set_model()`,
   and a turn limit, so the application can be left running.

- Source for all eight: `streaming-output`, `streaming-vs-single-mode`,
  `sessions`, `user-input`, `todo-tracking`, `cost-tracking`, the
  `ClaudeSDKClient` section of `python`, and the demos repository.

## Topics the chat app collection leaves out

- **Authentication and more than one user.** The application runs on
  the learner's own machine for the learner. Anthropic's terms do not
  allow a third party to offer claude.ai login or its rate limits in a
  product, so an application for other people runs on an API key, and
  the README says so.

- **Deployment.** Containers, scaling, and sessions shared between
  hosts are a later collection.

- **A front end framework.** The page is plain HTML and a little
  JavaScript, since the subject is the server side.

## Naming

Directory names are short kebab-case phrases naming the question, not
the mechanism, with no numeric prefix. The collection index carries the
order, and unnumbered names stay stable as workshops are inserted,
split or moved. Titles are sentence case and read as what the learner
will do.

Names are unique across every collection in this repository, because
all workshops share the one `workshops/` directory the extension
lists, and distinct from the names in the sibling workshop
repositories, because a learner may have several subscribed in one
JupyterLab and the browser matches a local directory to a collection by
name. The siblings checked on 2026-10-02 were decorator-workshops,
wrapture-workshops, wrapt-workshops, wsgi-workshops, tachyon-workshops
and the jupyterlab-workshop showcase. None of the 27 names here is
taken by any of them. The nearest are the `your-first-...` names in
three of them, so the first workshop here is `your-first-agent` and no
other name here starts that way.

The repository is named claude-sdk-workshops. The collection ids, the
catalog and the pages call the subject by its full name, the Claude
Agent SDK, since "Claude SDK" could as well mean the API client
library.

## Later collections

Candidates, none designed.

- **Running an agent as a service.** Hosting, the subprocess the SDK
  runs, sessions stored where more than one host can reach them, the
  sandbox, secure deployment, and traces and metrics through
  OpenTelemetry. It needs an API key and somewhere to deploy to, which
  is why it is not among the first three.

- **Plugins**, as a short addition to the extending collection or a
  collection of its own if there is enough to say.

- **File checkpointing**, for agents that edit files and need to undo.

A TypeScript version of the workshops was considered and ruled out by
the user on 2026-10-02. Nothing here is named or laid out to leave
room for one.

## Decisions that cut across the workshops

**Local only, on the learner's own login.** The workshops call the
model with the `claude` login of whoever started JupyterLab, so they
run on the learner's own machine and nowhere else. There is no Binder,
Codespaces or JupyterLite configuration and no analytics. The README
says what a learner needs: Claude Code installed and logged in on a
paid plan, or an API key in the environment, which the SDK uses in
preference when it is set.

**One environment for every workshop.** The other workshop
repositories install the subject into an environment of its own per
workshop. Here the SDK is a dependency of the project, pinned in
`pyproject.toml`, and every notebook runs on the JupyterLab
environment's kernel. The package is about 216 MB because it bundles
Claude Code, and 27 copies would be several gigabytes. The cost is that
whoever starts JupyterLab has to bring the SDK with it. A checkout does
that through `uv`. The route most learners take, `uvx` with
`jupyter-workshop launch` on the catalog's address and no checkout,
does it with `--with "claude-agent-sdk==<release>"`, which the README
spells out; the first workshop passed its self-test in an environment
made that way. Someone subscribing from a JupyterLab of their own
installs the SDK into it themselves.

**The pin and the reference move together.** `claude-agent-sdk` is
pinned exactly, `reference/claude-agent-sdk-python` is at the same
release's tag, and the README names the same release in the commands a
learner copies. `just bump-sdk` moves all three. The SDK moves fast, so
a bump is followed by reading the changelog and retesting, not assumed
safe.

**Haiku unless the entry says otherwise.** Every options object sets
`model="haiku"`. The tasks are small and tightly scoped, the learner's
plan pays for every run, and the trial showed the small model does
them. The exceptions are named in their entries: the model comparison
in foundations workshop 5, and one run of extending workshop 8, where
the main agent is on Sonnet and its subagent on Haiku. One pass
through the foundations collection is about forty calls, and one
through the extending collection about forty more, each a cent or two
at API prices by the trial's figures, and three to five cents for the
runs that read ten files. Haiku did everything the first two
collections needed: structured output, custom tools, skills,
subagents, compaction and tool search all worked on it. Effort made no
visible difference on Haiku in the trial, which is why foundations
workshop 5 shows it on Sonnet, where it made little on a task of that
size either. The user reviewed both collections on 2026-10-02 and
confirmed the split: Haiku for nearly everything, Sonnet for those few
runs.

**Every run is isolated and lean.** Every options object sets
`setting_sources=[]`, `strict_mcp_config=True`, `tools` to exactly what
the step needs, a short `system_prompt` of the workshop's own,
`thinking={"type": "disabled"}`, and a `max_turns` a little above what
the step should take. The first two keep the learner's own
instructions, skills and claude.ai connectors out of the run, so every
learner gets the same agent. The rest keep the request small, and
turning thinking off also keeps the stream to the messages the pages
explain. A workshop that teaches one of these options relaxes that one,
against files it ships, and says so: extending workshops 4 and 5 set
`setting_sources=["project"]`, and tell the learner that the files of
the directories above the workspace are loaded with it. The first workshop names the three
it does not explain in a hint, and foundations workshop 5 is where
thinking is turned back on and looked at.

**Every workshop checks the login first.** The welcome page of each
workshop runs the imports and then a one word run inside `try`, with a
check and a hint on how to log in. Workshops are self-contained, so
each one has to stand up to a machine that is not logged in, and
without the check the first call ends in a traceback.

**The agent stays in the workspace and is given little.** The working
directory is the workshop's workspace. No workshop uses
`bypassPermissions`, `WebSearch` or `WebFetch`. `Write` and `Edit`
appear from foundations workshop 6 on, and `Bash` only in workshops
about approvals and hooks, for commands the page names. This is a real
agent on the learner's machine, and the workshops are where the habit
of giving it the least it needs is formed.

**Checks read structure, never the model's words.** No two runs say the
same thing, so a check compares what a run did: which tools it called,
how it ended, whether an id is the same or different, whether data has
the right shape. Where the content matters, the workshop ships a file
holding a fact that could not be guessed, or tells the agent one, and
checks that it comes back. No quiz asks what the model will say.

**Prose does not quote output.** Pages say what a run does and what to
look for, and describe tokens and costs by size and direction. A
screenshot or a quoted reply would be wrong for most learners.

**Model calls take seconds, and pages say so.** The rule in the other
repositories that a cell should not pause is not one these can keep: a
run takes a few seconds, and more when it takes several turns. The
welcome page says so at the first model call, and each step makes one
run where it can.

**Diagrams in files of their own.** Where a picture of how the pieces
fit, or of the order things happen in, says it better than prose, the
workshop ships a Markdown file with a mermaid diagram under
`diagrams/` and a page opens it in JupyterLab's Markdown preview, in a
tab of the main area. The instructions panel is too narrow for one. The
user asked for this on 2026-10-02 and left where to use it to
judgement. The first workshop has two, one of the components and one
of a run. Workshop 2 has the loop, workshop 6 the checks made before
a tool runs, and workshop 8 the sessions left by a resume and a fork.
In the extending collection, workshop 2 has where a tool runs,
workshop 7 the order of hooks, rules and callback, and workshop 8 a
subagent at work.
A workshop gets one only where it earns its place, and a flowchart is
laid out left to right, which fits a wide tab better than a tall one.

**Concept before call.** Each page says what a thing is and why,
before the cell that uses it. The collections exist to teach how agents
work to someone new to them, and the SDK is the means.

**A running example.** The workshops share a small fictional bookshop,
Tidewater Books: a few Markdown documents (opening hours, a returns
policy, a staff handbook, events, a loyalty scheme) and, from the
extending collection on, a stock list of six made-up books, a month of
orders as SQL that a cell builds a SQLite database from, and the terms
of supply of ten suppliers.
Each workshop ships the files it uses, so none depends on another. The
documents hold details chosen to be unguessable, an odd closing time, a
returns window of an unusual length, so that a right answer shows the
file was read. The user confirmed the bookshop on 2026-10-02, over the
alternative of material from his own work, such as the wrapt
documentation. The chat app collection keeps it.

**Learners never type code.** Every cell, command and file edit
arrives through an action.

**Notebook first.** The first two collections are notebooks because a
notebook shows what an agent run is made of: each message is an object
the learner can open. The chat application waits for the third
collection, where its server and browser code have ideas the learner
already holds to hang on.

**Self-contained workshops.** A workshop restates what it builds on in
a sentence and ships what it needs. The chat app workshops ship the
application as it stood at the end of the one before.

**Sessions are written under the home directory.** The SDK records
each session's transcript under the Claude configuration directory,
outside the workspace. It is the one thing a workshop leaves outside
its own directory. The sessions workshop deletes the two it makes on
purpose and tells the learner that every run leaves one; see the open
questions for the rest.

**A function for a run that is repeated.** Where a workshop makes the
same run several times with one option changed, as foundations
workshops 4, 5 and 6 and most of the extending workshops do, the first
cell defines a function that makes the run and the
later cells are one line each, so that what changed is all there is to
read. Workshops that make one run of each kind write the options out
in full.

**Options are copied, not rewritten.** A cell that needs the earlier
options with one field changed uses `dataclasses.replace`, as in
`replace(options, max_turns=1)`, which shows the one difference.

**Done.** A workshop is done when lint is clean, `just test <name>`
is green, it is in the index and the README, and its row in the status
table says so. The self-test calls the model, so it is run for the
workshop being worked on and not for all of them on every change.

## Collections and the repository

**Why one repository.** The three collections share a subject, a
running example, the pinned SDK and the rules in `AGENTS.md`, and they
are meant to be taken in order.

**Layout.** Every workshop lives flat under `workshops/`. Each
collection has an index at `collections/<name>/collection.json`, and
`catalog.json` at the root names the three in order. `just index`
writes the indexes and the catalog; the catalog recipe names the
indexes one by one, since their order is not alphabetical.

**Where the order lives.** In the Justfile, as the list of workshop
names each `index-<collection>` recipe passes to the indexer.

**Ids.** `grahamdumpleton.me/claude-agent-sdk/foundations`,
`grahamdumpleton.me/claude-agent-sdk/extending` and
`grahamdumpleton.me/claude-agent-sdk/chat-app`. An id is a
collection's identity to anyone subscribed and never changes.

**How they are run.** `just lab` starts JupyterLab on the workshop
browser with the three collections added for the session and the
catalog. There is no hosted form.

**CI.** `.github/workflows/test.yml` lints the catalog, the indexes
and every workshop. It does not self-test, because a runner has no
Claude login and the workshops call the model at every step.

**On GitHub, private.** The repository is at
`https://github.com/GrahamDumpleton/claude-sdk-workshops`, private
while the workshops are being written. The Justfile, the indexes and
the README use that address.

## Extension features the workshops use

Settled from the extension's documentation at the pinned release, so
that each workshop does not rediscover them.

**Notebook pages.** The welcome page creates the notebook with
`notebook-create`, which uses the JupyterLab environment's kernel
since no workshop declares an environment. Each later step is one
`cell-insert` with a tag and `:run: true`, checked by a
`learner-kernel` verify triggered by `cell-executed <tag>`. Pages gate
on those verifies. An action may run for up to 300 seconds in the
self-test before it is reported as failed, which a model call is far
inside.

**Top level await.** A cell writes `async for message in query(...)`
and `await client.query(...)` directly. The SDK's
`examples/streaming_mode_ipython.py` is written the same way.

**The layout.** A custom `notebook` layout with one placeholder area,
never the built-in layouts, which open a terminal. With a code pane,
two columns: the placeholder, and a `code` area listing the shipped
files.

**Shipped files.** Under `files/`, copied into the workspace on first
open, before the opening layout is applied. The kernel starts in the
workspace, so `shop/opening-hours.md` is the path a cell and the agent
both use, as the first workshop confirmed.

**Hidden directories.** The contents API of the Jupyter server does
not list, open or write files under a directory whose name begins with
a dot. So nothing under `.claude/` can be shipped to a pane or written
by `file-write`. Extending workshop 5 ships its skill under `skills/`
and a cell copies it into `.claude/skills/`.

**Diagrams.** `file-open` with `:factory: Markdown Preview` opens a
shipped Markdown file rendered, mermaid blocks included, as a tab
beside the notebook. Without `area` it joins the notebook's area, which
gives it the full width.

**The login check and preflight.** The manifest lists `claude` under
`requires.tools` as optional, and the welcome page shows a note under
`{when} "claude" in missing_tools`. The SDK carries its own Claude
Code, so the command is needed only to log in.

**The web pane.** `url-open` with `pane` shows a page in an iframe in
the main area and reloads it each time it runs. The chat app workshops
use it for the application, with the port in a `number` variable.

**Capabilities.** `write-files` and `kernel-exec` for the notebook
workshops, with `terminal` added for the chat app workshops.

## Known blockers

None at present.

## Open questions

- **Sessions left in the learner's history.** Every run writes a
  transcript under the Claude configuration directory, filed under the
  workspace's path. Only the sessions workshop needs them kept. As
  written, that workshop deletes the two sessions it makes on purpose,
  and every other run of every workshop, the login checks included,
  leaves its transcript. The user looked at this on 2026-10-02, called
  it not ideal, and chose to leave the workshops as they are for now.

  What was found, for when it is taken up: the Python SDK has no
  option for it, and its documentation says to set the environment
  variable `CLAUDE_CODE_SKIP_PROMPT_HISTORY=1` for the Claude Code
  process. On the pinned release that wrote no transcript, whether set
  through the `env` option or in the kernel's `os.environ`, and the
  session could not then be listed or resumed. A `ClaudeSDKClient`
  conversation, `/compact`, `get_context_usage()` and a subagent all
  still worked with it set. The change would be one line in the
  imports cell of every workshop but the sessions one, a paragraph in
  each welcome page's hint about the options, and two paragraphs of
  the sessions workshop.

- **A `CLAUDE.md` inside the repository.** Extending workshop 4 ships
  its house rules as `files/CLAUDE.md`. Claude Code loads a
  `CLAUDE.md` below the directory it was started in when it reads a
  file beside it, so an agent working on that workshop's files is
  given the shop's house rules as instructions. They are harmless to
  it. The alternative, having a page write the file, was passed over
  so that the file could sit in the code pane from the start.

- **Auto-memory in the agent's context.** A session whose working
  directory is inside a project with Claude Code auto-memory is sent
  that project's memory index, whatever `setting_sources` says. That is
  the author's checkout, and any learner who uses Claude Code in the
  directory the workshops are kept in. It breaks the rule that every
  learner gets the same agent, by a small amount. One more option on
  every agent, `settings='{"autoMemoryEnabled": false}'`, closes it,
  at the price of a fourth line in every cell that the first workshop
  has to explain. Not decided. Foundations workshop 7 tells the
  learner what the "Memory files" line is if they see it, and
  extending workshop 4 names the setting that turns it off without
  using it.

- **When the repository goes public.** It is private for now. The
  README's clone command and the collection addresses work for others
  only once it is public.

## Status

The writing order is the collection order. The first workshop of the
foundations collection settles the manifest, the layout, the shape of
a page with a model call, and the checks, and each later one adds one
idea to a format that already works. Workshops 7 and 8 of the
foundations collection are written together, since the second resumes
what the first explains.

Foundations:

| # | Workshop | Status |
| --- | --- | --- |
| 1 | `your-first-agent` | Done |
| 2 | `watching-the-agent-loop` | Done |
| 3 | `reading-the-result` | Done |
| 4 | `giving-the-agent-instructions` | Done |
| 5 | `choosing-a-model` | Done |
| 6 | `deciding-what-it-can-do` | Done |
| 7 | `holding-a-conversation` | Done |
| 8 | `picking-up-where-you-left-off` | Done |
| 9 | `streaming-the-reply` | Done |
| 10 | `getting-data-back` | Done |

Extending:

| # | Workshop | Status |
| --- | --- | --- |
| 1 | `giving-the-agent-a-tool` | Done |
| 2 | `connecting-an-mcp-server` | Done |
| 3 | `answering-from-your-own-data` | Done |
| 4 | `instructions-that-persist` | Done |
| 5 | `packaging-know-how-as-a-skill` | Done |
| 6 | `asking-before-acting` | Done |
| 7 | `guardrails-in-code` | Done |
| 8 | `handing-work-to-subagents` | Done |
| 9 | `keeping-a-long-session-small` | Done |

Chat app:

| # | Workshop | Status |
| --- | --- | --- |
| 1 | `the-smallest-chat-app` | Outlined |
| 2 | `streaming-to-the-browser` | Outlined |
| 3 | `one-conversation-per-visitor` | Outlined |
| 4 | `showing-the-agent-at-work` | Outlined |
| 5 | `approving-from-the-browser` | Outlined |
| 6 | `plugging-in-your-tools` | Outlined |
| 7 | `coming-back-to-a-conversation` | Outlined |
| 8 | `showing-usage-and-limits` | Outlined |

The status words:

- **Outlined:** named and scoped here, with the entry still to be
  filled out and checked against the pinned release.

- **Planned:** designed in the outline, not yet written.

- **Written:** the pages exist and lint is clean.

- **Done:** `just test <name>` is green, and the workshop is in the
  index and the README.
