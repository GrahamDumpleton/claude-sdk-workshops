# Claude Agent SDK workshops: outline

The design of the collections in this repository: how they are
organised, what each workshop covers, its name and format, and the
decisions that cut across all of them. It is a living document. Read it
before adding a workshop, and update it when one is added, changed or
dropped: the status table at the end records where each workshop
stands, and the open questions section shrinks as they are settled.

The first workshop is written. The first collection is designed in
full below. The second and third are designed to the level of what each
workshop is for, and their entries are filled out, with the user,
before the first workshop of each is written.

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

Fifteen to twenty minutes each, about three hours in all. Notebook
workshops, most with a code pane beside the notebook
showing the shipped tool, server, skill or instruction file the pages
talk about, so the learner reads what the agent is being given.

On the question this collection was asked to answer, what the SDK
provides for "knowledge": it has no vector store and no retrieval
layer of its own. An agent gets at knowledge by searching and reading
files with its built-in tools, by calling a tool or an MCP server that
fronts a database or an API, by having instructions loaded into every
session, and by loading a skill. Workshop 3 teaches the first two side
by side, 4 and 5 the others.

## The extending workshops

These entries say what each workshop is for. Each is filled out to the
detail of the foundations entries, and checked against the pinned
release, before the collection is written.

### 1. `giving-the-agent-a-tool`: Give the agent a tool of your own

How a Python function becomes something the model can ask for.

A function that looks up the stock of a book is decorated with `@tool`,
put in a server made by `create_sdk_mcp_server()`, and passed in
`mcp_servers`. The agent calls it, as `mcp__<server>__<tool>`. The
pages dwell on the part that is not code: the tool's name, description
and input schema are all the model knows of it, so writing them is
writing a prompt. The learner runs the same question against a vague
description and a clear one. Read-only tools are marked as such, which
lets the SDK run them side by side.

- Format: notebook with a code pane. Source: `custom-tools`, `@tool`
  and `create_sdk_mcp_server()` in `python`, and
  `examples/mcp_calculator.py`. Length: 20 minutes.

### 2. `connecting-an-mcp-server`: Connect an MCP server

What the Model Context Protocol is, and how an agent uses a server it
did not write.

The same stock tool, now in a small server of its own that the
workshop ships and the SDK starts as a separate process. The page says
what MCP is, a standard way for a program to offer tools to any agent,
and why that matters: the tool is written once and used from any
client. The learner connects it with a `stdio` entry in `mcp_servers`,
reads its state and tool list with `get_mcp_status()`, and sees a
server that fails to start reported there. The page names the remote
transports without using them.

- Format: notebook with a code pane. Source: `mcp`, the MCP
  configuration types in `python`, and modelcontextprotocol.io. The
  `mcp` package the server is written with is installed as a
  dependency of the SDK. Length: 20 minutes.

### 3. `answering-from-your-own-data`: Answer from your own data

How an agent gets at what you know: documents and a database.

Two questions about the shop. One is answered from its documents, by
the agent searching and reading them with `Glob`, `Grep` and `Read`,
and the page calls this what it is: the agent decides what to look for
and reads it, rather than being handed passages picked for it in
advance. The other needs the orders, which are in SQLite, and is
answered through a tool that runs a read-only query. The pages compare
the two, say when each fits, and say plainly that the SDK ships no
vector store: retrieval by similarity is something you would put
behind a tool, as the database is here.

- Format: notebook with a code pane. Source: `custom-tools`, `mcp`,
  and "Keep context efficient" in `agent-loop`. The database is made
  by a cell from a shipped SQL file, so nothing binary is committed.
  Length: 20 minutes.

### 4. `instructions-that-persist`: Give instructions that persist

How project instructions are loaded, and why they outlast the prompt.

The shop's house rules go in a `CLAUDE.md` file in the workspace, and
`setting_sources=["project"]` loads it. The page says what the option
controls, which files it reads and from where, and why every other
workshop sets it to an empty list. It contrasts the three places an
instruction can live: the prompt, the system prompt, and a file that
is sent with every request and so survives a conversation being
summarised.

- Format: notebook with a code pane. Source: `claude-code-features`,
  `modifying-system-prompts`, and `examples/setting_sources.py`.
  Length: 15 minutes.

### 5. `packaging-know-how-as-a-skill`: Package know-how as a skill

What a skill is, and why it is not loaded until it is needed.

The shop's procedure for writing a refund reply becomes a skill, a
directory with a `SKILL.md` in the workspace. The `skills` option
makes it available, and the learner watches the agent call the `Skill`
tool when a refund comes up and not otherwise. The page explains the
design: only the skill's description is in the context to begin with,
and its body loads on use, so an agent can have many without paying
for them on every request.

- Format: notebook with a code pane. Source: `skills` and
  `claude-code-features`. Length: 20 minutes.

### 6. `asking-before-acting`: Ask before acting

How a person stays in the loop.

A `can_use_tool` callback is called when a tool needs approval. In the
notebook it decides by a rule the page shows, standing in for a person,
and the learner sees a call allowed, a call refused with a reason the
model then reads, and a call allowed with its input changed. Then the
other reason the callback is called: the agent asking a clarifying
question through `AskUserQuestion`, which the callback answers. The
chat app collection puts a real person behind the same callback.

- Format: notebook. Source: `user-input`, `permissions`, and
  `examples/tool_permission_callback.py`. Length: 20 minutes.

### 7. `guardrails-in-code`: Put guardrails in code

How hooks enforce what a prompt can only ask for.

An instruction in a prompt is a request, and the model may not follow
it. A hook is code the SDK runs at a fixed point in the loop. A
`PreToolUse` hook refuses any write outside one directory, whatever
the model was told, and a `PostToolUse` hook keeps a log of every
call. The page sets hooks beside the permission callback: the callback
is asked only when approval is needed, a hook sees every call.

- Format: notebook. Source: `hooks`, the hook types in `python`, and
  `examples/hooks.py`. Length: 20 minutes.

### 8. `handing-work-to-subagents`: Hand work to subagents

What a subagent is, and what it saves.

A task that means reading a lot to report a little is given to a
subagent defined with `AgentDefinition`: its own instructions, its own
tools, a context of its own, and only its final report returned. The
learner compares the main agent's context after doing the reading
itself and after delegating it. Each subagent can have its own model,
which is where a small model for the reading and a larger one for the
judgement pays.

- Format: notebook. Source: `subagents`, `AgentDefinition` in
  `python`, and `examples/agents.py`. This workshop may use Sonnet for
  the main agent. Length: 20 minutes.

### 9. `keeping-a-long-session-small`: Keep a long session small

What fills the context window, and what the SDK does when it is full.

`get_context_usage()` breaks the window down by what is in it. The
learner fills a session with tool results and watches the total, then
sees compaction, where older history is replaced by a summary and a
boundary message marks the place, and reads what was kept. The page
gathers the ways to stay small that the collection has already shown,
fewer tools, subagents, skills, and adds tool search, which loads tool
definitions only when they are looked for.

- Format: notebook. Source: "The context window" in `agent-loop`,
  `tool-search`, and `cost-tracking`. How to bring compaction about
  cheaply, and whether tool search works on Haiku, are to be settled
  before this is designed in detail. Length: 20 minutes.

## Topics the extending collection leaves out

- **Plugins.** A way to package skills, agents, hooks and MCP servers
  together. It teaches no new idea once those four are known. A
  candidate to add at the end if the packaging turns out to matter.

- **Remote MCP servers and their authentication.** Named in workshop
  2. They need a server to reach and credentials to hold.

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

## The chat app workshops

These entries are one step short of the extending entries: they say
what each workshop adds. The collection is designed in detail, starting
with the choice of web framework, once the first two are written.

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
in foundations workshop 5, and possibly subagents and structured
output. One pass through the foundations collection is about forty
calls, each a cent or two at API prices by the trial's figures.

**Every run is isolated and lean.** Every options object sets
`setting_sources=[]`, `strict_mcp_config=True`, `tools` to exactly what
the step needs, a short `system_prompt` of the workshop's own,
`thinking={"type": "disabled"}`, and a `max_turns` a little above what
the step should take. The first two keep the learner's own
instructions, skills and claude.ai connectors out of the run, so every
learner gets the same agent. The rest keep the request small, and
turning thinking off also keeps the stream to the messages the pages
explain. A workshop that teaches one of these options relaxes that one,
against files it ships, and says so. The first workshop names the three
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
A workshop gets one only where it earns its place, and a flowchart is
laid out left to right, which fits a wide tab better than a tall one.

**Concept before call.** Each page says what a thing is and why,
before the cell that uses it. The collections exist to teach how agents
work to someone new to them, and the SDK is the means.

**A running example.** The workshops share a small fictional bookshop,
Tidewater Books: a few Markdown documents (opening hours, a returns
policy, a staff handbook, events, a loyalty scheme) and, from the
extending collection on, a small SQLite database of books and orders.
Each workshop ships the files it uses, so none depends on another. The
documents hold details chosen to be unguessable, an odd closing time, a
returns window of an unusual length, so that a right answer shows the
file was read.

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
same run several times with one option changed, as workshops 4, 5 and
6 do, the first cell defines a function that makes the run and the
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

- **The running example.** Tidewater Books was proposed and has not
  been confirmed by the user. The alternative raised was material from
  the user's own work, such as the wrapt documentation.

- **Sessions left in the learner's history.** Every run writes a
  transcript under the Claude configuration directory, filed under the
  workspace's path. Whether the workshops should keep these out, by an
  option that turns persistence off if the pinned release has one, or
  clean up after themselves, or leave them, is not decided. Only the
  sessions workshop needs them kept. As written, that workshop deletes
  the two sessions it makes on purpose, and every other run of every
  workshop, the login checks included, leaves its transcript.

- **The web framework for the chat app.** The SDK is asynchronous, so
  the server is an ASGI one. Starlette with server-sent events is the
  proposal, since it adds the least beside the subject. It is added to
  `pyproject.toml` when the collection is designed. Whether a terminal
  the extension opens finds the project environment's Python is to be
  checked then.

- **What Haiku cannot do.** Compaction and tool search are to be tried
  on Haiku before their workshops are designed in detail. Structured
  output was tried and works. Effort made no visible difference on
  Haiku in the trial, which is why foundations workshop 5 shows it on
  Sonnet, where it made little on a task of that size either.

- **Auto-memory in the agent's context.** A session whose working
  directory is inside a project with Claude Code auto-memory is sent
  that project's memory index, whatever `setting_sources` says. That is
  the author's checkout, and any learner who uses Claude Code in the
  directory the workshops are kept in. It breaks the rule that every
  learner gets the same agent, by a small amount. One more option on
  every agent, `settings='{"autoMemoryEnabled": false}'`, closes it,
  at the price of a fourth line in every cell that the first workshop
  has to explain. Not decided. Workshop 7 tells the learner what the
  "Memory files" line is if they see it.

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
| 1 | `giving-the-agent-a-tool` | Outlined |
| 2 | `connecting-an-mcp-server` | Outlined |
| 3 | `answering-from-your-own-data` | Outlined |
| 4 | `instructions-that-persist` | Outlined |
| 5 | `packaging-know-how-as-a-skill` | Outlined |
| 6 | `asking-before-acting` | Outlined |
| 7 | `guardrails-in-code` | Outlined |
| 8 | `handing-work-to-subagents` | Outlined |
| 9 | `keeping-a-long-session-small` | Outlined |

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
