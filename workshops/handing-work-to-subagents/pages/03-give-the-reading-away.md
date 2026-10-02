---
title: Give the reading away
requires: [verify:reader-defined, quiz:what-comes-back, verify:work-delegated]
---

# Give the reading away

A subagent is described to the SDK with an `AgentDefinition`, and it
has four parts worth setting.

- `description` says what the subagent is for. The main agent reads it
  to decide when to hand work over, so it does the job a tool's
  description does.

- `prompt` is the subagent's own system prompt. It replaces the main
  agent's: the subagent is not sent the main agent's instructions.

- `tools` lists what the subagent may use. It can be given less than
  the main agent has. This one can find files and read them, and
  nothing else.

- `model` chooses the model it runs on, which need not be the main
  agent's.

Definitions go in the `agents` option under a name, here `reader`. The
main agent starts a subagent with a built-in tool called `Agent`, so
that tool has to be in `tools`.

The cell makes the definition, and options for a main agent that
delegates. They are the last run's options with four things changed.
It calls nothing.

```{cell-insert}
:id: insert-reader
:path: {{ notebook }}
:tags: [reader]
:run: true
reader = AgentDefinition(
    description=(
        "Reads the shop's files and reports what they say. Use it for any "
        "question that needs files to be read."
    ),
    prompt=(
        "You read files for the staff of Tidewater Books. Find the files that "
        "matter, read them, and report only the facts you were asked for, as a "
        "short list. Leave everything else out."
    ),
    tools=["Glob", "Read"],
    model="haiku",
)

delegating_options = replace(
    direct_options,
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "Do not read files yourself. Hand any reading to the reader agent, and "
        "answer in a few sentences from its report and nothing else."
    ),
    tools=["Agent", "Glob", "Read"],
    agents={"reader": reader},
    env={"CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1"},
)

print("subagents defined :", list(delegating_options.agents))
print("the reader's tools:", reader.tools)
```

Two of the four changes need a word.

`Glob` and `Read` are still in the main agent's `tools`. A subagent
can only be given tools the session has, so they have to be there,
and it is the system prompt that tells the main agent to leave the
reading alone.

The `env` line sets a variable for the Claude Code process the SDK
runs. A subagent is normally started in the background: the main
agent gets on with other things and is told when the subagent has
finished. That suits a long job in an application. In a notebook cell
that should end with the answer it is simpler for the main agent to
wait, and this setting makes it wait.

```{verify}
:id: reader-defined
:label: The subagent and the delegating options are defined
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed reader
"reader" in delegating_options.agents and "Agent" in delegating_options.tools
```

## Ask the same question

The step below opens a picture of what is about to happen.

```{file-open}
:id: open-subagent
:title: Open the picture of a subagent at work
:path: diagrams/a-subagent-at-work.md
:factory: Markdown Preview
```

```{quiz}
:id: what-comes-back
:title: What comes back
question: "The subagent reads ten files and finishes. What is added to the main agent's conversation?"
options:
  - text: "The ten files, since the main agent needs them to answer."
    explanation: "The files were read into the subagent's conversation, which the main agent never sees."
  - text: "Every message of the subagent's conversation."
    explanation: "The subagent's conversation is its own. Only the end of it is handed back."
  - text: "The subagent's final message, its report, as the result of the `Agent` tool."
    correct: true
  - text: "Nothing. The subagent answers the user directly."
    explanation: "A subagent answers the agent that started it, which then writes the answer."
explanation: "Starting a subagent is a tool call, and the report is its result. The main conversation gains the task that was set and the report that came back."
```

```{cell-insert}
:id: insert-delegated
:path: {{ notebook }}
:tags: [delegated]
:run: true
delegated = await ask(delegating_options)
```

Follow the lines. The main agent asked for one tool, `Agent`, naming
the `reader` and setting it a task. The indented lines are the
subagent at work: it listed the directory and read the files, as the
single agent did before. Then a report came back, short beside the
ten files it was made from, and the main agent answered from it.

The answer should be the same as last time. The line at the bottom is
not.

```{verify}
:id: work-delegated
:label: The main agent handed the reading to the subagent
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed delegated
if "Agent" not in delegated["main"]:
    print("The main agent did not start the subagent. Run the cell again.")
elif "Spindrift" not in delegated["result"].result:
    print("The answer does not name a supplier it should. Run the cell again.")
(
    "Agent" in delegated["main"]
    and len(delegated["inside"]) >= 1
    and "Spindrift" in delegated["result"].result
)
```

```{hint}
:title: What a subagent is not told
A subagent starts with its own `prompt`, the task the main agent
wrote for it, and nothing else of the conversation. It does not know
what the user asked, what was said earlier or what the main agent has
already found out. So the main agent has to put everything the
subagent needs into the task, and a good `description` and `prompt`
help it do that.
```
