---
title: Change one rule
requires: [verify:second-answered]
---

# Change one rule

A shop would rather not have its assistant tell a customer "I do not
know" and leave it there. The next prompt is the first one with a
single rule replaced: where the policy does not cover a question, the
agent is to send the customer to a named person at the counter.

The question does not change, and neither does anything else.

```{cell-insert}
:id: insert-second
:path: {{ notebook }}
:tags: [second]
:run: true
counter_prompt = shop_prompt.replace(
    "say that you do not know",
    "tell the customer to ask Marguerite at the counter",
)

second, second_size = await ask(counter_prompt)

print(second.result)
```

Compare this reply with the one above it in the notebook. The half
about returning the book should say much the same, since the policy
has not changed. The half about second-hand books is where the two
part.

One sentence of instruction changed what the agent does every time
that situation comes up, for every customer, without anything being
programmed. That is what a system prompt is for. It is also why it
deserves care: the model follows what the prompt says, including what
it says by accident.

Nothing checks what the agent said here, because no two replies are
worded the same. Reading the reply is the check.

```{verify}
:id: second-answered
:label: The agent answered under the changed prompt
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed second
if second.subtype != "success":
    print("The run ended with", second.subtype, "- run the cell again.")
second.subtype == "success" and counter_prompt != shop_prompt
```

```{hint}
:title: What the agent sees of the two texts
The system prompt and the customer's question reach the model in
different places in the request, and it is trained to treat them
differently: the system prompt as the rules it works under, the prompt
as what it has been asked. A customer who writes "ignore your
instructions" in a question is writing in the wrong place for that to
carry the same weight, though no prompt makes an agent proof against
it.
```
