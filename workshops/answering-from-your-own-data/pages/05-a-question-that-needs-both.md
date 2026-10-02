---
title: A question that needs both
requires: [quiz:who-chooses-the-source, verify:answered-from-both]
---

# A question that needs both

Real questions do not arrive sorted by where the answer is kept. A
customer wants to return a book he ordered. Whether he may depends on
when he ordered it, which is a record, and on how long the shop allows,
which is in a document.

This time the agent is given everything: the three file tools and the
orders server.

```{quiz}
:id: who-chooses-the-source
:title: Who chooses the source
question: "The agent has file tools and a database tool, and the question needs both. What decides which is used for which part?"
options:
  - text: "The SDK, which sends questions about orders to the database."
    explanation: "The SDK does not read the question. It carries out the requests the model makes."
  - text: "The order the tools are listed in the options."
    explanation: "The order makes no difference to which tool is asked for."
  - text: "The model, from the system prompt and the description of each tool."
    correct: true
  - text: "Your code, which has to split the question in two first."
    explanation: "Nothing splits the question. It goes to the model whole."
explanation: "The model decides, one request at a time, from what it has been told about each tool. That is why the system prompt said where the documents are and the tool's description said what the database holds."
```

```{cell-insert}
:id: insert-both
:path: {{ notebook }}
:tags: [both]
:run: true
return_question = (
    "Barnaby Quill wants to return the copy of The Ferry Almanac he ordered. "
    "He has the receipt, and today is 2 October 2026. Can he have a refund?"
)

statements.clear()

both = await ask(
    return_question,
    tools=["Glob", "Grep", "Read"],
    mcp_servers={"orders": orders_server},
)
```

Follow the requests. The agent looked the order up in the database to
find its date, and went to the documents for the rule on returns. No
code of yours said which to use for what. Then it put the two
together.

The right answer has three parts, and you can check each: the order
was placed on 12 September, the returns policy allows 23 days with a
receipt, and 2 October is the twentieth day. The arithmetic on dates
is the model's own, and a small model can slip on it, so read what it
said.

```{verify}
:id: answered-from-both
:label: The agent used the database and the documents in one run
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed both
if "mcp__orders__query_orders" not in both["calls"]:
    print("The model did not query the orders. Run the cell again.")
elif not any(name in both["calls"] for name in ("Read", "Grep")):
    print("The model did not look in the documents. Run the cell again.")
(
    "mcp__orders__query_orders" in both["calls"]
    and any(name in both["calls"] for name in ("Read", "Grep"))
    and both["result"].subtype == "success"
)
```
