---
title: List them
requires: [verify:list-in-place, verify:page-lists, verify:listed]
---

# List them

The SDK has a function that finds its transcripts. Given a directory,
`list_sessions()` returns an entry for each session that was run
there, newest first. Each entry has the session's id and a `summary`,
a short title the SDK writes for the session from what was said in it.
It reads the files and calls no model.

## A route for the list

```{editor-insert}
:id: import-list
:title: Import the function that lists sessions
:path: app.py
:match: get_session_messages,
:position: after
:save: false
    list_sessions,
```

The route returns the id and the title of each. `include_worktrees`
is turned off to keep the list to this one directory: left on, the SDK
also looks in other checkouts of the same git repository.

```{editor-insert}
:id: add-list-route
:title: Add a route that lists the conversations
:path: app.py
:match: @app.get("/status")
@app.get("/conversations")
def list_conversations():
    return [
        {"id": session.session_id, "title": session.summary}
        for session in list_sessions(directory=str(WORKSPACE), include_worktrees=False)
    ]



```

```{verify}
:id: list-in-place
:label: The server restarted with a route that lists conversations
:substrate: script
:script: checks/list_in_place.py
:trigger: after:add-list-route
```

## A place for it in the page

{open}`page.html` gets a part that folds away under the heading,
holding a link that starts a new conversation and a place for the
list.

```{editor-insert}
:id: add-list-markup
:title: Add a fold-away list to the page
:path: page.html
:match: <main id="messages"></main>
<details>
  <summary>Conversations</summary>
  <a href="/?new">Start a new one</a>
  <nav id="list"></nav>
</details>
```

When the page loads, it asks the server for the list and makes a link
of each entry. The link is the page's own address with the
conversation's id in it, as `/?c=` followed by the id, which the page
learned to act on a moment ago.

```{editor-insert}
:id: fill-list
:title: Fill the list in as the page loads
:path: page.html
:match: // A question in the address, as in /?ask=When+do+we+open, is asked as the
  // List the conversations the server can find.
  for (const item of await (await fetch("/conversations")).json()) {
    const link = document.createElement("a");
    link.href = "/?c=" + item.id;
    link.textContent = item.title;
    if (item.id === conversation) link.className = "current";
    document.getElementById("list").append(link);
  }


```

```{verify}
:id: page-lists
:label: The page lists the conversations
:substrate: contents
:trigger: after:fill-list
contains page.html fetch("/conversations")
```

## Look at the list

Load the chat again, then click **Conversations** under the heading to
unfold it.

```{url-open}
:id: reload-chat
:title: Load the chat again
:url: http://127.0.0.1:{{ server_port }}/
:pane: chat
:label: Chat
:area: chat
```

The conversation you just had is there, in bold because it is the one
the page is showing, under a title you did not write. The SDK made
the title from the conversation.

```{verify}
:id: listed
:label: The server lists the conversation
:substrate: script
:script: checks/listed.py
:trigger: after:reload-chat
```
