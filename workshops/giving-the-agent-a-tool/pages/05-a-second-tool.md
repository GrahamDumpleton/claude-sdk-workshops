---
title: A second tool
requires: [verify:second-tool-used]
---

# A second tool

A server holds as many tools as you give it. The agent is told about
all of them, and chooses between them by their descriptions.

This cell adds a tool that searches by author, and makes a server that
holds both. Each description says what its tool is for, and the first
one already says what it is not for, so the two do not compete.

```{cell-insert}
:id: insert-second-tool
:path: {{ notebook }}
:tags: [second-tool]
:run: true
@tool(
    "books_by_author",
    "List every book in the shop's stock list by one author, given the author's "
    "name. Returns each title with its stock code and the number of copies in "
    "stock. Use it when you have an author and no title.",
    {"author": str},
)
async def books_by_author(args):
    wanted = args["author"].strip().lower()
    found = [
        f"{book['title']}: stock code {book['stock_code']}, {book['copies']} in stock"
        for book in load_stock()
        if book["author"].lower() == wanted
    ]
    text = "\n".join(found) or f"No books by {args['author']!r} are in the stock list."
    return {"content": [{"type": "text", "text": text}]}


both_server = create_sdk_mcp_server(
    name="shop", version="1.0.0", tools=[check_stock, books_by_author]
)

both = await ask(author_question, both_server)

print()
print("tools the agent had :", both["tools"])
```

The agent had two tools this time, and the last line names them.
`allowed_tools=["mcp__shop__*"]` in `ask()` approved both: the star
stands for every tool of the server. To approve one tool only, write
its full name.

The customer gets a right answer at last, and both of the author's
books are in it.

```{verify}
:id: second-tool-used
:label: The agent chose the tool that searches by author
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed second-tool
if "mcp__shop__books_by_author" not in both["calls"]:
    print("The model did not ask for books_by_author. Run the cell again.")
elif "Salt on the Wind" not in both["result"].result:
    print("The answer does not name both books. Run the cell again.")
(
    "mcp__shop__books_by_author" in both["calls"]
    and len(both["tools"]) == 2
    and "Salt on the Wind" in both["result"].result
)
```

## One tool or several

The fix here was a new tool, not a cleverer one. Small tools that each
do one thing, named and described for what they do, are easier for a
model to choose between than one tool with a mode for everything.
Every tool's description is sent with every request, though, so each
one costs a little, and a later workshop in this set comes back to
what to do when there are many.
