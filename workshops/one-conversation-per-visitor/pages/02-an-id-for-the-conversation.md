---
title: An id for the conversation
requires: [verify:id-in-place]
---

# An id for the conversation

Before the server can keep a conversation for each visitor, it has to
be able to tell their messages apart. To the server a message is a
request like any other, with nothing in it to say who sent it, or what
was said before. So the page will say: every message it sends will
carry an id, the same one each time.

## The page makes one up

The id is a UUID, a long random value that no two pages will choose
alike. The page makes one up the first time it loads and keeps it in
`localStorage`, storage the browser gives each site and keeps between
visits, so that the page finds the same id again when it is reloaded.

One more thing in these lines: an address ending in `/?new` forgets the
stored id, which starts a new conversation.

```{editor-insert}
:id: add-id
:title: Give the page an id for its conversation
:path: page.html
:match: function post(path, body) {
// This page's conversation has an id, kept in the browser's storage so that
// a reload carries on with it. /?new forgets it and starts another.
if (params.has("new")) localStorage.removeItem("conversation");
let conversation = localStorage.getItem("conversation") || crypto.randomUUID();
localStorage.setItem("conversation", conversation);


```

The id goes to the server beside the message.

```{editor-replace}
:id: send-id
:title: Send the id with every message
:path: page.html
:match: post("/chat", {message: text})
post("/chat", {conversation, message: text})
```

## The server expects it

On the server, `Ask` says what a message from the page must look like.
It gains a second field. Declared as a `UUID`, the field is checked by
FastAPI before the route runs: a request with no id, or with something
that is not a UUID, is refused.

```{editor-insert}
:id: import-uuid
:title: Import the UUID type
:path: app.py
:match: from pathlib import Path
:position: after
:save: false
from uuid import UUID
```

```{editor-insert}
:id: ask-has-id
:title: Expect an id with every message
:path: app.py
:match: message: str
    conversation: UUID
```

The server restarted. It now insists on the id, and does nothing with
it yet: the route still starts a new session for every message.

```{verify}
:id: id-in-place
:label: The page sends an id and the server expects one
:substrate: script
:script: checks/id_in_place.py
:trigger: after:ask-has-id
```

```{hint}
:title: Why not a cookie
A cookie is the usual way for a browser to say who it is, and it is
the wrong tool here for a reason that has to do with these workshops.
The chat is shown in a frame inside JupyterLab, and a browser will not
keep a cookie for a framed page unless the frame and the page around
it are served from the same host name. An id the page keeps and sends
for itself works wherever the page is shown.

In an application of your own, with people logging in, the id of a
conversation would be tied to the account on the server, and would
not be something a page could make up.
```
