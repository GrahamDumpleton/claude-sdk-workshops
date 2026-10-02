---
title: Branch one
requires: [verify:fork-in-place, verify:page-branches, verify:branched]
---

# Branch one

Sometimes the wish is not to carry a conversation on, but to go back
to where it was and ask something else, keeping what came after. A
fork does that. It makes a new session that starts with a copy of
another's history and has an id of its own. The original is left as
it was, and the two go their own ways from there.

## A route that copies

The SDK's `fork_session()` copies a transcript under a new id and
returns the id. It works on the files, and calls no model.

```{editor-insert}
:id: import-fork
:title: Import the function that forks a session
:path: app.py
:match: get_session_info,
:save: false
    fork_session,
```

```{editor-insert}
:id: add-fork-route
:title: Add a route that branches a conversation
:path: app.py
:match: @app.get("/status")
@app.post("/fork")
def fork(which: Which):
    branch = fork_session(str(which.conversation), directory=str(WORKSPACE))
    return {"conversation": branch.session_id}



```

```{verify}
:id: fork-in-place
:label: The server restarted with a route that branches a conversation
:substrate: script
:script: checks/fork_in_place.py
:trigger: after:add-fork-route
```

## A link for it

The page gets a link in its list, **Branch from this one**. Like the
others it is the page's own address, this time with `branch=` and the
id of the conversation to copy.

```{editor-insert}
:id: add-branch-link
:title: Add a link that branches the conversation
:path: page.html
:match: <nav id="list"></nav>
  <a id="branch">Branch from this one</a>
```

```{editor-insert}
:id: point-branch-link
:title: Point the link at this conversation
:path: page.html
:match: for (const item of await (await fetch("/conversations")).json()) {
  document.getElementById("branch").href = "/?branch=" + conversation;
```

A page loaded with such an address asks the server for the copy, and
takes the new id for its own before it does anything else. The rest
follows as before: the history it then asks for is the copy's.

```{editor-insert}
:id: branch-on-load
:title: Branch as the page loads, when the address says so
:path: page.html
:match: // Show what has been said in this conversation so far.
  // /?branch=<id> copies that conversation and carries on in the copy.
  if (params.has("branch")) {
    const response = await post("/fork", {conversation: params.get("branch")});
    conversation = (await response.json()).conversation;
    localStorage.setItem("conversation", conversation);
  }


```

```{verify}
:id: page-branches
:label: The page can branch a conversation
:substrate: contents
:trigger: after:branch-on-load
contains page.html post("/fork", {conversation: params.get("branch")})
```

## Branch the first conversation

The step below branches the first conversation and asks a new
question in the branch.

```{url-open}
:id: ask-in-branch
:title: Branch the first conversation and ask about story time
:url: http://127.0.0.1:{{ server_port }}/?branch={{ first_conversation }}&ask=And+when+is+story+time%3F
:pane: chat
:label: Chat
:area: chat
```

The page shows the first conversation's history, and the new question
below it.

```{verify}
:id: branched
:label: The branch went on, and the original was left as it was
:substrate: script
:script: checks/branched.py
:timeout: 150s
:trigger: after:ask-in-branch
```

Once the reply is in, load the page again to bring its list up to
date.

```{url-open}
:id: reload-chat
:title: Load the chat again
:url: http://127.0.0.1:{{ server_port }}/
:pane: chat
:label: Chat
:area: chat
```

Unfold **Conversations** and there is one more entry, in bold, with a
title that marks it as a fork. Open the original from the list: the
question about story time is not in it.

A fork copies what was said, and nothing else. Any file the agent
wrote in the original conversation is still the same file, in the
same place, for both.
