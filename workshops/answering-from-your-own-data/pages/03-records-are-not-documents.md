---
title: Records are not documents
requires: [verify:database-built]
---

# Records are not documents

The shop's orders are a different kind of thing. {open}`data/orders.sql`
describes two tables, customers and orders, and fills them with a
month of orders. In a real shop they would be in a database that is
already running. Here a cell builds one, in SQLite, a database that is
a single file and comes with Python.

```{cell-insert}
:id: insert-database
:path: {{ notebook }}
:tags: [database]
:run: true
database = Path("orders.db")
database.unlink(missing_ok=True)

connection = sqlite3.connect(database)
connection.executescript(Path("data/orders.sql").read_text())
connection.commit()

order_count = connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
customer_count = connection.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

connection.close()

print("database  :", database)
print("orders    :", order_count)
print("customers :", customer_count)
```

The agent's file tools are no use on this. A database file is not
text, so `Read` and `Grep` find nothing in it they can use. Even where
the records can be read, as they can in the `.sql` file, reading is
the wrong way to answer most questions about them. Which customer
ordered the most copies is an addition over every row. A model asked
to do that sum in its head will often get it wrong, and a table of a
million rows would not fit in what it can be sent in any case.

Questions about records are answered by queries, and a database
answers a query exactly. So the agent needs a way to run one.

```{verify}
:id: database-built
:label: The orders database was built
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed database
database.exists() and order_count == 12 and customer_count == 5
```
