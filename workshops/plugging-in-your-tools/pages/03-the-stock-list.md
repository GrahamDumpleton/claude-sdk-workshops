---
title: The stock list
requires: [verify:stock-in-place, verify:stock-answered]
---

# The stock list

The shop's stock is in {open}`shop/stock.csv`: a title, an author, a
stock code, the number of copies and a shelf, on a line for each book.
The agent could read the file as it reads the others. A tool is the
better fit: it looks up one title and returns one line, however long
the list grows.

{open}`shop_tools.py` holds the tool, and it is the same shape as any
tool written for the SDK.

- `@tool` takes a name, a description and the shape of the input, and
  decorates the function that does the work, the handler.

- The description is written for the model, which reads it to decide
  when the tool fits. This one also says what the tool cannot do, so
  that the model does not try.

- `create_sdk_mcp_server()`, at the bottom of the file, groups the
  tools into a server. It runs inside your own program: when the model
  asks for the tool, the SDK calls your function.

Nothing in the file knows about the web. A tool that worked in a
notebook works here unchanged.

## Hand it to the agent

The server imports the group of tools.

```{editor-insert}
:id: import-shop-server
:title: Import the shop's tools
:path: app.py
:match: OPTIONS = ClaudeAgentOptions(
:save: false
from shop_tools import shop_server


```

Then two options. `mcp_servers` hands the group to the agent under a
name, here `shop`. The agent then knows each tool by a longer name:
the letters `mcp`, the server's name and the tool's name, joined by
double underscores.

`allowed_tools` approves the stock tool ahead of time. A tool of your
own needs approval before it runs, as `Write` does, because the SDK
cannot know what your function does. This one only looks, so it is
approved by name once and for all, and nobody is asked each time.

```{editor-insert}
:id: add-shop-server
:title: Give the agent the tools, and approve the stock tool
:path: app.py
:match: setting_sources=[],
    mcp_servers={"shop": shop_server},
    allowed_tools=["mcp__shop__check_stock"],
```

```{verify}
:id: stock-in-place
:label: The server restarted with the shop's tools plugged in
:substrate: script
:script: checks/stock_in_place.py
:trigger: after:add-shop-server
```

## Ask about a book

```{url-open}
:id: ask-stock
:title: Ask whether Tidewater is in stock
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Is+the+book+Tidewater+in+stock%2C+and+what+is+its+stock+code%3F
:pane: chat
:label: Chat
:area: chat
```

The line under the heading has grown by two names, and one of them
appeared in the chat as a tool line, drawn exactly as `Read` is. The
page needed no change. To the server a tool of yours arrives in the
stream as a request and a result, like any other.

```{verify}
:id: stock-answered
:label: The agent looked the book up with the shop's tool
:substrate: script
:script: checks/stock_answered.py
:timeout: 150s
:trigger: after:ask-stock
```
