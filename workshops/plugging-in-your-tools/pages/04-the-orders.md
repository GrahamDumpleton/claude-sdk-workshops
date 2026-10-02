---
title: The orders
requires: [quiz:not-approved, verify:orders-in-place, verify:orders-answered]
---

# The orders

The line under the heading listed two tools from the shop's server,
and only one of them has been approved. The other,
`mcp__shop__query_orders`, is further down {open}`shop_tools.py`. It
runs one SQL statement on the shop's orders and returns the rows.

Two things about it are worth reading.

- The database is opened read-only, by the `mode=ro` in the line that
  connects to it. A statement that tries to change an order is refused
  by the database itself, whatever the model was told.

- The description gives the layout of the tables. The model has never
  seen this database, and the description is all it has to write a
  query from.

In a real shop the database would already be running somewhere. Here
`build_database()` makes one when the file is imported, from
{open}`data/orders.sql`, as the file `orders.db` beside the server.

```{quiz}
:id: not-approved
question: The agent has the orders tool and it is not in `allowed_tools`. What happens if the model asks for it now?
options:
  - { text: "The tool runs, because it is in a server the agent was given", explanation: "Being given a tool and being approved to use it are separate. An unapproved call needs someone to say yes." }
  - { text: "The call goes to your callback, which refuses anything that is not a notice", correct: true }
  - { text: "The model cannot ask, because an unapproved tool is hidden from it", explanation: "The line in the chat showed the tool in the session's list. The model can ask for anything in that list." }
explanation: "A call that nothing has approved is put to `can_use_tool`. The method from the last workshop refuses every tool but `Write`, so the model would be told no."
```

Approve it, beside the first.

```{editor-replace}
:id: approve-orders
:title: Approve the orders tool as well
:path: app.py
:match: allowed_tools=["mcp__shop__check_stock"],
allowed_tools=["mcp__shop__check_stock", "mcp__shop__query_orders"],
```

```{verify}
:id: orders-in-place
:label: The server restarted with both tools approved
:substrate: script
:script: checks/orders_in_place.py
:trigger: after:approve-orders
```

## Ask about the orders

A question that takes an addition over every order to answer, in the
same conversation as the last.

```{url-open}
:id: ask-orders
:title: Ask which customer ordered the most copies
:url: http://127.0.0.1:{{ server_port }}/?ask=Which+customer+ordered+the+most+books+in+September%2C+counting+copies%3F
:pane: chat
:label: Chat
:area: chat
```

The tool line shows the SQL the model wrote. It had your question and
the description of the tables, and from those it worked out a query
that joins the two tables and adds up the copies. The database did the
arithmetic, and the model read one row and wrote a sentence.

```{verify}
:id: orders-answered
:label: The agent answered by querying the orders
:substrate: script
:script: checks/orders_answered.py
:timeout: 150s
:trigger: after:ask-orders
```
