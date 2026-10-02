---
title: Thinking
requires: [quiz:what-thinking-adds, verify:thinking-ran]
---

# Thinking

Every agent in these workshops has been given
`thinking={"type": "disabled"}`, with a promise to come back to it.

Thinking is a step in which the model reasons to itself before it
replies. It writes out its working, as you might on scrap paper, and
then writes the reply. The working is output like any other: the model
produces it a token at a time, it takes time, and it is counted. It is
not part of the answer, and the SDK reports it apart from the answer.

Left to itself, the small model thinks before most of its replies. The
workshops turn that off. This run leaves it on, by passing
`thinking=None`, which is the same as not setting the option at all.

```{quiz}
:id: what-thinking-adds
:title: What thinking adds
question: "The task and the model are the same as in the first run. With thinking left on, where does the extra work show in the figures?"
options:
  - text: "In the input, because the model is sent its own reasoning to read."
    explanation: "Thinking is something the model writes, not something it is sent at the start. The instructions, the question and the files are the same as before."
  - text: "In the output, because the model writes its reasoning as well as its replies."
    correct: true
  - text: "In the model's name, because thinking needs a larger model."
    explanation: "The model is the same one. Thinking is an option on a run, not a different model."
  - text: "Nowhere. Thinking happens inside the model and is not counted."
    explanation: "Reasoning is written out a token at a time like everything else the model produces, and every token it writes is counted."
explanation: "Thinking is output. The model writes its reasoning before each reply, so the output tokens are where it shows."
```

```{cell-insert}
:id: insert-thinking
:path: {{ notebook }}
:tags: [thinking]
:run: true
answer = await run_task("haiku, thinking", "haiku", thinking=None)

print(answer.result)
print()
for label in ("haiku", "haiku, thinking"):
    row = rows[label]
    print(
        f"{label:<18} thinking blocks: {row['thinking blocks']:<3}"
        f" thinking tokens: {row['thinking tokens']:<6} output tokens: {row['out']}"
    )
print()
show()
```

The three lines under the answer compare the two runs on the small
model.

- **Thinking blocks** are a kind of block you have not met. A reply
  from the model can open with a `ThinkingBlock` ahead of its text or
  its request for a tool. The first run had none.

- **Thinking tokens** are the part of the output that was reasoning.
  They are included in the output tokens beside them.

The reasoning itself is not shown in these runs. What is reported is
that it happened and what it used.

Thinking is for problems that need working out: a plan with many
steps, a subtle bug, a judgement between close options. Reading a
shop's documents and reporting what they say is not one of those, so
here it adds output and seconds without changing much. That is why
the workshops leave it off, and it keeps the stream of messages to the
kinds the pages explain.

```{verify}
:id: thinking-ran
:label: The task ran with thinking left on
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed thinking
row = rows["haiku, thinking"]
if row["ended"] != "success":
    print("The run ended with", row["ended"], "- run the cell again.")
elif row["thinking tokens"] == 0 and row["thinking blocks"] == 0:
    print("The model did not think on this run, which it is free to do. Run the cell again to see a run where it does.")
row["ended"] == "success" and len(rows) == 4
```
