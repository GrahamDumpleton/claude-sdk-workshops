---
title: How the loop ends
requires: [verify:turns-counted]
---

# How the loop ends

Look at the last reply in the list the cell just printed. Every reply
before it held a `ToolUseBlock`. The last one holds only a `TextBlock`.

That is the whole rule. The SDK looks at each reply from the model. If
there is a request in it, the SDK carries the request out, adds the
result to the conversation and asks again. If there is no request, the
run is over, and the text of that reply is the answer. Nothing else
decides how long a run is: the model goes on asking until it thinks it
has enough.

Each time round is called a turn. The `ResultMessage` that ends the
run counts them in `num_turns`. The cell puts that beside two counts
of your own.

```{cell-insert}
:id: insert-turns
:path: {{ notebook }}
:tags: [turns]
:run: true
last_reply = list(replies.values())[-1]

print("replies from the model :", len(replies))
print("requests for a tool    :", len(requests))
print("turns, says the result :", result.num_turns)
print("the last reply held    :", ", ".join(last_reply["blocks"]))
```

As the SDK counts them, the turns are the tool requests plus one: a
turn for each request, and a last turn for the answer. When the model
asks for one tool at a time, that is also the number of replies. A
model may ask for two tools in a single reply, when it can see it
needs both, and then there are fewer replies than turns.

A run that only answers a question takes one turn. This one took
several, and nothing in your code said how many.

```{verify}
:id: turns-counted
:label: The run took more than one turn and ended on an answer
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed turns
if "ToolUseBlock" in last_reply["blocks"]:
    print("The last reply still held a request. Run the cell on the second page again, then the ones after it.")
result.num_turns >= 2 and "ToolUseBlock" not in last_reply["blocks"]
```

```{hint}
:title: What stops a loop that never ends
A model that keeps asking would keep the loop going. The `max_turns`
option in the first cell is the guard: the run is stopped when it has
taken that many turns. The next workshop makes a run hit that limit to
show what comes back.
```
