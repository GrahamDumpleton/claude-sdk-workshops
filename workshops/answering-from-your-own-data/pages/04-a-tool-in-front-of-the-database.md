---
title: A tool in front of the database
requires: [verify:writes-refused, verify:answered-from-database]
---

# A tool in front of the database

The tool is a function of yours, made with `@tool` and put in a server
with `create_sdk_mcp_server()`, the way **Give the agent a tool of
your own** did it. It takes one piece of text, a SQL statement, runs
it, and returns the rows.

Two things about it are worth reading closely.

- **The description carries the layout of the database.** The model
  has never seen the tables. It can only write a query that works if
  it is told what tables and columns there are and what they mean,
  and the description is the one place to tell it.

- **The database is opened read-only.** `mode=ro` in the connection
  string makes SQLite itself refuse anything that would change the
  data. The description says the tool is read-only too, but that only
  informs the model. The connection is what makes it true.

The cell defines the tool, then calls its handler directly with a
statement that deletes every order, to show what the database does
with it. No model is involved.

```{cell-insert}
:id: insert-tool
:path: {{ notebook }}
:tags: [tool]
:run: true
statements = []


@tool(
    "query_orders",
    "Run one SQL SELECT statement on the shop's orders database, which is SQLite, "
    "and return the rows. The database is read-only. Tables: "
    "customers(customer_id, name, tide_card: 1 for a member of the loyalty scheme, "
    "0 otherwise) and orders(order_id, customer_id, title, quantity, "
    "price_cents: the price of one copy in cents, ordered_on: the date as YYYY-MM-DD).",
    {"sql": str},
    annotations=ToolAnnotations(readOnlyHint=True),
)
async def query_orders(args):
    statements.append(args["sql"])
    try:
        connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
        try:
            cursor = connection.execute(args["sql"])
            columns = [column[0] for column in cursor.description or []]
            rows = cursor.fetchmany(50)
        finally:
            connection.close()
    except sqlite3.Error as error:
        return {
            "content": [{"type": "text", "text": f"The query failed: {error}"}],
            "is_error": True,
        }
    return {"content": [{"type": "text", "text": json.dumps({"columns": columns, "rows": rows})}]}


orders_server = create_sdk_mcp_server(name="orders", version="1.0.0", tools=[query_orders])

refused = await query_orders.handler({"sql": "DELETE FROM orders"})

print("is_error :", refused.get("is_error"))
print("it said  :", refused["content"][0]["text"])
```

The delete was refused by the database, and the handler turned the
refusal into a result marked as an error. Had a model sent that
statement, it would have been told the same thing, and no order would
have been lost.

That is a pattern to keep. Whatever a tool must never do, make it
impossible in the tool, and do not rely on the model having been
asked not to.

```{verify}
:id: writes-refused
:label: The database refuses to be changed through the tool
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed tool
remaining = sqlite3.connect(database).execute("SELECT COUNT(*) FROM orders").fetchone()[0]
refused.get("is_error") is True and remaining == 12
```

## A question the records answer

Now the agent is given the tool and no file tools at all, and asked
something that takes a query to answer.

```{cell-insert}
:id: insert-records
:path: {{ notebook }}
:tags: [records]
:run: true
orders_question = (
    "Which customer ordered the most books in September, counting copies, and how many?"
)

statements.clear()

records = await ask(orders_question, tools=[], mcp_servers={"orders": orders_server})
```

The line that begins `the model asks` is the SQL the model wrote. It
had the question and the description of the tables, and from those it
worked out a query that joins the two tables and adds up the copies.
The database did the arithmetic. The model read one row and wrote a
sentence.

Check the answer against {open}`data/orders.sql` if you like. One
customer's three orders come to more copies than anyone else's.

```{verify}
:id: answered-from-database
:label: The agent answered by querying the database
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed records
if not statements:
    print("The model did not run a query. Run the cell again.")
elif "Ottoline" not in records["result"].result:
    print("The answer does not name the customer the data gives. Run the cell again.")
len(statements) >= 1 and "Ottoline" in records["result"].result
```

```{hint}
:title: Is it safe to let a model write SQL
Here, yes, because of how the tool is built: the connection cannot
write, the tool returns at most fifty rows, and the database holds
nothing the member of staff asking may not see. Take any of those away
and the answer changes. A tool that takes SQL gives the model
everything the connection can reach, so give the connection only what
the agent's user is allowed. Where that is hard to arrange, offer
narrower tools, such as one that looks up a single customer's orders,
and write the queries yourself.
```
