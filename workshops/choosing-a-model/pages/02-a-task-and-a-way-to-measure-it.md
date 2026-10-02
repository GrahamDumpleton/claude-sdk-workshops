---
title: A task and a way to measure it
requires: [verify:haiku-ran]
---

# A task and a way to measure it

A fair comparison needs a task where the model has something to get
wrong. The workshop ships two of the bookshop's documents,
{open}`shop/returns-policy.md` and {open}`shop/loyalty-scheme.md`, and
the task is a question that neither answers alone. The returns policy
gives the usual rule. The loyalty scheme changes it for members, and
changes it in more than one way. A right answer needs both documents,
read together.

The agent is not told which files to read. It has `Glob`, which lists
files by name, and `Read`.

## One function for every run

The same task is going to be run four times with one or two options
changed, so the first cell defines the task and a function that runs
it. The function takes a label for the run, the model, and the two
options the later pages change. It keeps a row of figures for each
run, and `show()` prints the rows as a table.

This cell calls nothing yet.

```{cell-insert}
:id: insert-task
:path: {{ notebook }}
:tags: [task]
:run: true
task = (
    "A customer with a Tide Card bought a book 30 days ago for $28 and has "
    "the receipt. Can they return it, and what exactly do they get back?"
)

rows = {}


async def run_task(label, model, thinking={"type": "disabled"}, effort=None):
    options = ClaudeAgentOptions(
        model=model,
        system_prompt=(
            "You are the assistant for the staff of Tidewater Books, a small bookshop. "
            "The shop's documents are in the shop directory. Work out the answer from "
            "them, and answer in two or three sentences."
        ),
        tools=["Glob", "Read"],
        setting_sources=[],
        strict_mcp_config=True,
        thinking=thinking,
        effort=effort,
        max_turns=12,
    )
    files_read = []
    thinking_blocks = 0
    async for message in query(prompt=task, options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            model_name = message.data["model"]
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name == "Read":
                    files_read.append(block.input.get("file_path", "").split("/")[-1])
                elif isinstance(block, ThinkingBlock):
                    thinking_blocks += 1
        elif isinstance(message, ResultMessage):
            result = message
    usage = result.usage
    rows[label] = {
        "model": model_name,
        "ended": result.subtype,
        "read": files_read,
        "turns": result.num_turns,
        "in": usage["input_tokens"]
        + usage["cache_creation_input_tokens"]
        + usage["cache_read_input_tokens"],
        "out": usage["output_tokens"],
        "thinking blocks": thinking_blocks,
        "thinking tokens": (usage.get("output_tokens_details") or {}).get("thinking_tokens", 0),
        "seconds": result.duration_ms / 1000,
        "cost": result.total_cost_usd,
    }
    return result


def show():
    print(f"{'run':<20}{'model':<28}{'turns':>6}{'in':>8}{'out':>7}{'secs':>7}{'est. $':>9}")
    for label, row in rows.items():
        print(
            f"{label:<20}{row['model']:<28}{row['turns']:>6}{row['in']:>8}"
            f"{row['out']:>7}{row['seconds']:>7.1f}{row['cost']:>9.4f}"
        )


print("ready to run:", task)
```

## The small model first

`model="haiku"` is what every run in these workshops has used. The
short name stands for a full model name, which the session reports
when it starts and the table shows.

```{cell-insert}
:id: insert-haiku
:path: {{ notebook }}
:tags: [haiku]
:run: true
answer = await run_task("haiku", "haiku")

print(answer.result)
print()
print("read:", rows["haiku"]["read"])
print()
show()
```

Before looking at the numbers, check the answer against the two
documents yourself. A right answer has three parts:

- Yes, the book can come back. A member has 37 days, not 23.

- It comes back as shop credit of $28 and not as a refund, because day
  30 is past the usual 23.

- The 28 points earned on the book come off the card.

The line under the answer lists the files the model read. A run that
never opened the loyalty scheme cannot have got this right, whatever
it said. Whether this run did is for you to read: a small model gets
a job like this right on some runs and not on others.

The columns of the table are the figures every result carries: the
turns the run took, the tokens the model was sent and wrote, the
seconds, and the estimated cost at API prices, which on a subscription
is a measure of size and not a charge.

```{verify}
:id: haiku-ran
:label: The task ran on the small model
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed haiku
if rows["haiku"]["ended"] != "success":
    print("The run ended with", rows["haiku"]["ended"], "- run the cell again.")
rows["haiku"]["ended"] == "success" and "haiku" in rows["haiku"]["model"]
```
