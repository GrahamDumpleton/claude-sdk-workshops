---
title: What the model knows of it
requires: [verify:tool-described, quiz:what-the-model-can-tell, verify:vague-run-done]
---

# What the model knows of it

The model called your function without ever seeing it. Here is all it
was shown. This cell calls nothing. It prints the three things the SDK
sends to the model for the tool.

```{cell-insert}
:id: insert-described
:path: {{ notebook }}
:tags: [described]
:run: true
print("name        :", check_stock.name)
print("description :", check_stock.description)
print("input       :", check_stock.input_schema)
```

That is the whole of it. The input is printed as you wrote it, and
the SDK sends it on as a JSON Schema that says the same thing: one
piece of text, called `title`. The body of `check_stock`, the file it
reads and the way it compares titles are not sent. If the description
does not say something, the model does not know it.

So a description is not a comment for the next programmer. It is an
instruction to the model, read every time it decides what to do, and
writing one is writing a prompt.

```{verify}
:id: tool-described
:label: You have seen what the model is shown
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed described
"title" in check_stock.input_schema and bool(check_stock.description)
```

## The same function, described badly

To see what the description is worth, take it away. The cell below
wraps the same handler a second time, with the same name and the same
input, and a description of four words. `tool()` is used here as an
ordinary function, which is all a decorator is.

The question changes too. A customer wants to know whether the shop
has anything by an author. Look at {open}`shop/stock.csv`: it has two
of her books. Your function cannot find them, because it matches
titles and nothing else. The first description said so. This one does
not.

```{quiz}
:id: what-the-model-can-tell
:title: What the model can tell
question: "The tool is now described as \"Look up a book.\" and takes one piece of text called `title`. What does the model know about whether it can search by author?"
options:
  - text: "It knows it cannot, because the handler compares titles."
    explanation: "The model never sees the handler. Only the name, the description and the input schema reach it."
  - text: "Nothing. It has to guess from four words and the name of one field."
    correct: true
  - text: "It knows it can, because the stock file has an author column."
    explanation: "The model has not seen the file. It could only learn of the column from a tool result."
  - text: "The SDK tells it, by trying the tool first."
    explanation: "The SDK runs a tool only when the model asks for it. Nothing is tried ahead of time."
explanation: "A model with a vague description has to guess what a tool is for and what to pass. It will usually guess something, and act on what comes back."
```

```{cell-insert}
:id: insert-vague
:path: {{ notebook }}
:tags: [vague]
:run: true
vague_tool = tool("check_stock", "Look up a book.", {"title": str})(check_stock.handler)

vague_server = create_sdk_mcp_server(name="shop", version="1.0.0", tools=[vague_tool])

author_question = "A customer is asking whether we have anything by Odette Farrow. Do we?"

vague = await ask(author_question, vague_server)
```

Look at what the model passed as `title`, if it called the tool, and
at what your function said back. Then read the answer the customer
would have been given, and check it against the stock file.

A tool that is used for something it cannot do does not fail. It
returns something, and the model builds an answer on it. Whatever
happened on your run, nothing the model was shown could have told it
that a search by author would find nothing.

```{verify}
:id: vague-run-done
:label: The agent was run with the vague description
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed vague
if vague["result"].subtype != "success":
    print("The run ended with", vague["result"].subtype, "- run the cell again.")
vague["result"].subtype == "success" and vague["tools"] == ["mcp__shop__check_stock"]
```
