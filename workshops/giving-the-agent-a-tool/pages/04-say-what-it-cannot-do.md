---
title: Say what it cannot do
requires: [verify:clear-run-done]
---

# Say what it cannot do

Now the same question, to the tool as it was first written. Its
description said three things the short one left out: what comes
back, what the tool cannot search by, and what to do when the title is
not known.

```{cell-insert}
:id: insert-clear
:path: {{ notebook }}
:tags: [clear]
:run: true
clear = await ask(author_question, shop_server)

print()
print("vague description, the model passed :", vague["inputs"])
print("clear description, the model passed :", clear["inputs"])
```

Compare the two runs. The function is the same, the question is the
same, and the only thing that changed is a paragraph of English. With
the limits written down, the model has what it needs to tell that this
tool cannot answer the question, and to say so or ask for a title
rather than pass an author where a title belongs.

A description that earns its place says:

- what the tool does, in the words a request would use;

- what it returns, so the model knows what it can answer from it;

- what it cannot do, so that it is not used for that;

- what form the input takes, where that is not obvious.

The agent still cannot answer the customer. It knows that now, which
is better than a wrong answer, and the next page gives it what it
lacks.

```{verify}
:id: clear-run-done
:label: The agent was run with the clear description
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed clear
if clear["result"].subtype != "success":
    print("The run ended with", clear["result"].subtype, "- run the cell again.")
clear["result"].subtype == "success" and clear["tools"] == ["mcp__shop__check_stock"]
```

```{hint}
:title: Describing the input as well
`{"title": str}` is the short way to give an input schema, and it has
no room for a description of each field. `@tool` also accepts a full
JSON Schema, the form **Get data back, not prose** used, where every
property can carry a `description` and a field can be limited to a
list of values with `enum`. Those descriptions are sent to the model
too.
```
