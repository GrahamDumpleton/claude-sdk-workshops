---
title: The same text, twice
requires: [verify:pieces-match]
---

# The same text, twice

Turning on partial messages adds to the stream and takes nothing
away. The complete `AssistantMessage` still arrives once the text is
finished, and the `ResultMessage` still ends the run. So the reply
reached your code twice: once in pieces, and once whole.

This cell calls nothing. It joins the pieces and compares them with
the text of the complete message.

```{cell-insert}
:id: insert-compared
:path: {{ notebook }}
:tags: [compared]
:run: true
joined = "".join(pieces)

print("pieces, joined   :", len(joined), "characters")
print("complete message :", len(final_text), "characters")
print("the same text    :", joined == final_text)
```

They are the same text. That tells you what each is for:

- **The pieces are for showing.** Put each on the screen as it
  arrives, and then let it go.

- **The complete message is for keeping.** It is the reply as the SDK
  records it, with its blocks intact, and it is the one to store, log
  or act on. A program that does not show progress can ignore the
  events altogether and lose nothing.

The same holds when the agent uses tools. The input the model writes
for a tool streams as pieces too, which lets an application show what
an agent is about to do while it is still deciding, and the complete
`ToolUseBlock` follows.

```{verify}
:id: pieces-match
:label: The pieces joined are the text of the complete message
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed compared
if joined != final_text:
    print("The two differ. Run the cell on the previous page again, then this one.")
bool(joined) and joined == final_text
```
