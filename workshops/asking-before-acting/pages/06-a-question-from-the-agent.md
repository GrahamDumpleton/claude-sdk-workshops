---
title: A question from the agent
requires: [verify:question-answered]
---

# A question from the agent

Approval is one reason an agent stops for a person. The other is that
it does not know something and ought to ask.

There is a built-in tool for that, `AskUserQuestion`. The model calls
it with one or more questions, each with a few answers to choose from.
The tool does nothing by itself. A call to it always comes to your
callback, and your callback supplies the answers by allowing the call
with them added to its input:

```python
PermissionResultAllow(
    updated_input={"questions": tool_input["questions"], "answers": {...}}
)
```

`answers` maps the text of each question to the answer given: the
label of one of the choices offered, or words of your own.

This cell defines a second callback. It answers a question with a note
the manager left, and passes everything else to the callback you
already have. Then it gives the agent a job with a hole in it: a
notice that has to name a day, and a request that does not say which.

```{cell-insert}
:id: insert-fourth
:path: {{ notebook }}
:tags: [fourth]
:run: true
managers_note = "Thursday 8 October"

questions = []


async def answer_or_approve(tool_name, tool_input, context):
    if tool_name != "AskUserQuestion":
        return await approve(tool_name, tool_input, context)
    answers = {}
    for question in tool_input["questions"]:
        questions.append(question)
        choices = [option["label"] for option in question["options"]]
        print("  the agent asks   :", question["question"])
        print("  it offers        :", choices)
        print("  the answer given :", managers_note)
        answers[question["question"]] = managers_note
    return PermissionResultAllow(
        updated_input={"questions": tool_input["questions"], "answers": answers}
    )


stocktake = Path("notices/stocktake.md")

fourth = await attempt(
    "Write a notice for the door, to notices/stocktake.md, saying which day "
    "next week the shop is closed for stocktaking.",
    callback=answer_or_approve,
    tools=("Read", "Write", "AskUserQuestion"),
)

print()
print(stocktake.read_text() if stocktake.exists() else "no notice was written")
```

The agent had been told, in its system prompt, to ask and not to
guess. It asked which day, with choices of its own making. The
callback answered in words that were not among the choices, the model
was sent the answer as the result of its request, and the notice was
written with it.

In an application this is a dialog: the question and its choices are
shown, the person picks one or types their own, and the callback
returns what they said. The run waits for as long as that takes.

```{verify}
:id: question-answered
:label: The agent asked a question and the callback answered it
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed fourth
if not questions:
    print("The agent did not ask a question on this run. Run the cell again.")
elif not stocktake.exists():
    print("The notice was not written. Run the cell again.")
len(questions) >= 1 and stocktake.exists()
```

```{hint}
:title: What the tool list had to hold
`AskUserQuestion` is a built-in tool like `Read`, so it has to be in
`tools` for the model to be able to ask at all. An agent given a short
list of tools and no way to ask will guess. Whether it asks also
depends on being told to: the system prompt here says so in a
sentence.
```
