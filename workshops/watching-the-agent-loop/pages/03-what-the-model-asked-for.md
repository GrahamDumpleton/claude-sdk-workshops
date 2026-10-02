---
title: What the model asked for
requires: [verify:request-seen, quiz:who-read-the-file]
---

# What the model asked for

Every line that began "the model asks" was a `ToolUseBlock`, a block
inside one of the model's replies. Open the first one. This cell calls
nothing. It reads what the run left behind.

```{cell-insert}
:id: insert-request
:path: {{ notebook }}
:tags: [request]
:run: true
first_request = requests[0]

print("type  :", type(first_request).__name__)
print("id    :", first_request.id)
print("name  :", first_request.name)
print("input :", first_request.input)
```

That is all a request is: three pieces of data.

- **name** is the tool the model wants used.

- **input** is what it wants the tool given, such as a pattern to
  match or a file to read.

- **id** labels the request, so that the answer can say which request
  it belongs to.

The model wrote this, in the same way it writes a sentence. It is text
in a fixed shape that a program can read. Writing it ran nothing: no
file was opened and no directory was listed. A model cannot do those
things. It can only say that it would like them done.

```{verify}
:id: request-seen
:label: The first request names a tool and its input
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed request
bool(first_request.id) and bool(first_request.name) and isinstance(first_request.input, dict)
```

```{quiz}
:id: who-read-the-file
:title: Who read the file
question: "Later in the run the model asked for `Read` on one of the shop's documents, and the contents came back. What read the file?"
options:
  - text: "The model, on Anthropic's servers."
    explanation: "The model is a service that takes text and returns text. It has no access to this machine, and the file never left it except as text in a later request."
  - text: "The SDK, on this machine."
    correct: true
  - text: "The notebook cell, in its `async for` loop."
    explanation: "The cell only printed the messages as they went past. It opened no file."
  - text: "Nothing did. The model already knew what the file said."
    explanation: "The details in the answer are in the shop's documents and nowhere else. The model had to be sent them."
explanation: "The model asks and the SDK does. The SDK read the file, on this machine, with the access of whoever started JupyterLab. That is why the tools an agent is given matter: they decide what it can touch."
```
