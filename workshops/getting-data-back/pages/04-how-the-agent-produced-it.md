---
title: How the agent produced it
requires: [verify:mechanism-read]
---

# How the agent produced it

A model produces text, so something had to turn text into a
dictionary and make sure it fitted. The run you just made recorded the
tools the model asked for. This cell calls nothing. It prints them,
with what the result holds.

```{cell-insert}
:id: insert-mechanism
:path: {{ notebook }}
:tags: [mechanism]
:run: true
print("tools the model asked for :", tool_calls)
print("how the run ended         :", structured.subtype)
print("result is a               :", type(structured.result).__name__)
print("structured_output is a    :", type(hours).__name__)
print()
print(structured.result[:76], "...")
```

The first tool in the list is `Read`, which you gave the agent. The
last is one you did not. When `output_format` is set, the SDK adds a
tool of its own whose input has to match your schema, and tells the
model to finish by calling it. So the agent's final answer is a
request to use a tool, like every other request it has made, with the
data as the input.

That is why the shape can be trusted. A tool's input is data in a
fixed form, and the SDK checks it against the schema before the run
ends. If it does not fit, the model is told what was wrong and tries
again. Only a value that fits is handed to you as `structured_output`.

Two more things the output shows:

- `result` is still a string. It holds the same data written out as
  JSON text, for code that wants the text.

- The agent still looped. It read the file first, as it did on the
  earlier run. Asking for data changes how a run ends, not how it gets
  there.

If the model cannot produce a value that fits after several tries,
the run ends with the subtype `error_max_structured_output_retries`
and no data, so a program checks the subtype here as it would on any
run.

```{verify}
:id: mechanism-read
:label: The agent read the file and returned checked data
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed mechanism
"Read" in tool_calls and structured.subtype == "success" and isinstance(structured.result, str)
```
