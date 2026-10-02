---
title: Which to use
requires: [verify:runs-compared]
---

# Which to use

The three runs are still in the notebook. This cell calls nothing. It
sets them side by side: what each used, how many turns it took, and
how many tokens the model was sent over the whole run. A token is a
piece of text about the size of a short word, and it is the unit usage
is counted in.

```{cell-insert}
:id: insert-compared
:path: {{ notebook }}
:tags: [compared]
:run: true
compared = {}

for label, run in [("documents", documents), ("records", records), ("both", both)]:
    compared[label] = {
        "tools": sorted(set(run["calls"])),
        "turns": run["result"].num_turns,
        "sent": tokens_sent(run["result"]),
    }

for label, row in compared.items():
    print(f"{label:<10} turns {row['turns']:>2}   tokens sent {row['sent']:>6}   {row['tools']}")
```

Both of the first two runs answered one short question, and the run
on the documents was most likely sent several times what the run on
the records was. Some of that is the three file tools, whose
definitions go with every request, and the extra turn it took to find
the right file. The rest is in the nature of reading. A file that is
read goes into the conversation whole and is sent again with every
request after it, while a query sends back only the rows that answer
it.

## Two ways, and when each fits

| | Search and read files | Query through a tool |
| --- | --- | --- |
| Suits | Prose: policies, handbooks, notes, source code | Records: orders, customers, stock, logs |
| The agent needs | `Glob`, `Grep`, `Read` and to be told where to look | A tool of yours, with the layout in its description |
| What reaches the model | Whole files, or the lines a search matched | The rows that answer the query |
| Good at | Following a question wherever the documents lead | Counting, adding, filtering, joining |
| Grows with | The size of what is read | The size of the answer |

## What the SDK does not have

You may have expected a third way: a store that documents are loaded
into ahead of time, cut into passages, so that the passages most like
a question can be fetched and handed to the model. That is usually
called a vector store, and the method retrieval-augmented generation.

The SDK does not ship one. An agent built on it finds things by
looking, as you saw on the first run, and for a body of documents that
fits on a disk and can be searched by word that works well, because
the agent can read around what it finds and look again.

Where searching by word is not enough, for a very large body of documents or
for questions that share no words with their answers, retrieval by
similarity is something you put behind a tool, as the database is
here. A function takes a question, asks your index, and returns the
passages. To the agent it is one more tool with a description.

```{verify}
:id: runs-compared
:label: The three runs were compared
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed compared
len(compared) == 3 and all(row["sent"] > 0 for row in compared.values())
```
