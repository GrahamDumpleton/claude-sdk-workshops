---
title: What the SDK sent back
requires: [verify:every-request-answered]
---

# What the SDK sent back

When the SDK has run a tool it sends the model what the tool found, as
a `ToolResultBlock`. Each one carries a `tool_use_id`, the id of the
request it answers.

The cell pairs every request with its answer.

```{cell-insert}
:id: insert-answers
:path: {{ notebook }}
:tags: [answers]
:run: true
answer_for = {block.tool_use_id: block for block in answers}

unanswered = []

for request in requests:
    answer = answer_for.get(request.id)
    if answer is None:
        unanswered.append(request.name)
        continue
    print(request.name, request.input)
    print("   ->", str(answer.content)[:90], "...")

print("requests without an answer:", unanswered)
```

Every request has an answer, and the answer is text: the list of files
that `Glob` matched, or the lines of the file that `Read` opened. A
tool result is always turned into text, because text is the only thing
a model can be sent.

## Why it arrives as a user message

Look back at the cell that made the run. It found the tool results
inside a `UserMessage`, the type that carries what the user says. You
said nothing during the run, and yet there they are.

A conversation with a model has two sides. What the model produces is
on the assistant's side. Everything it is sent is on the user's side.
A tool result is something the model is sent, so it goes in a message
in the user's role, written by the SDK on your behalf. To the model, a
tool result is simply more input.

```{verify}
:id: every-request-answered
:label: Every request the model made was answered
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed answers
if unanswered:
    print("These requests have no answer:", unanswered, "- run the cell on the second page again, then this one.")
bool(requests) and unanswered == []
```

```{hint}
:title: When a tool fails
A tool that fails still gets an answer. The `ToolResultBlock` carries
the error as its text and has `is_error` set, and the model reads it
like any other result. It may try something else, which is the loop
doing its job.
```
