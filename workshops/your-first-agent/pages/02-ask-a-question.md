---
title: Ask a question
requires: [verify:stream-seen]
---

# Ask a question

`query()` runs an agent once. You give it a prompt, which is the
request, and options, which set the agent up. It does not hand back a
string. It hands back messages, one at a time, as the run goes on, so
you read it with `async for`. A notebook cell can use `async for` and
`await` directly.

The options here are the fewest that make a small, predictable agent:

- `model="haiku"` picks the smallest and cheapest model.

- `system_prompt` is the standing instruction the agent works under:
  who it is and how to answer.

- `tools=[]` gives it no tools at all, for now.

- `max_turns=3` stops a run that goes wrong.

The cell collects every message into a list and prints the type of
each.

```{cell-insert}
:id: insert-first-run
:path: {{ notebook }}
:tags: [first-run]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt="You are the assistant for Tidewater Books, a small bookshop. Answer in one or two sentences.",
    tools=[],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=3,
)

messages = []

async for message in query(prompt="What is a bookshop for?", options=options):
    messages.append(message)

kinds = [type(message).__name__ for message in messages]

for kind in kinds:
    print(kind)
```

One question produced several messages, of three kinds that matter:

- A `SystemMessage` came first. It is the SDK reporting how the
  session was set up, before the model has said anything.

- An `AssistantMessage` is the model's reply.

- A `ResultMessage` came last. It says the run is over and how it
  went.

You probably also see a `RateLimitEvent`. With a subscription login the
service reports where you stand against your plan's limits, and the SDK
passes that on.

```{verify}
:id: stream-seen
:label: The run produced system, assistant and result messages
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed first-run
missing = {"SystemMessage", "AssistantMessage", "ResultMessage"} - set(kinds)
if missing:
    print("The run did not produce:", ", ".join(sorted(missing)), "- run the cell again.")
not missing
```

```{hint}
:title: What the other three options are for
`setting_sources=[]` and `strict_mcp_config=True` keep your own Claude
configuration out of the run. Without them the agent would load the
instructions, skills and connected services you have set up for
yourself, and would behave differently on your machine than on anyone
else's.

`thinking={"type": "disabled"}` turns off a step in which the model
reasons privately before it answers. These tasks do not need it, and it
adds to the usage of every run.

Every agent in these workshops sets all three. Later workshops come
back to each of them.
```
