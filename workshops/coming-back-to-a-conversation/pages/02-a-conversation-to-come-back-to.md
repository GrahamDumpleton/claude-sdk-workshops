---
title: A conversation to come back to
requires: [verify:page-takes-id, verify:first-conversation]
---

# A conversation to come back to

To come back to a conversation, something has to say which one. The
page already knows two ways to choose: it keeps the id it made up, in
the browser's storage, and an address ending in `/?new` forgets that
id and makes up another. It needs a third: an address that names a
conversation.

The two lines below add it to {open}`page.html`. An address with
`c=` and an id replaces the id in the browser's storage, and from
there the page does what it always does: it asks for that
conversation's history, and sends its messages there.

```{editor-insert}
:id: take-id-from-address
:title: Take a conversation's id from the address
:path: page.html
:match: if (params.has("new")) localStorage.removeItem("conversation");
:position: after
// /?c=<id> swaps it for the id of another conversation.
if (params.has("c")) localStorage.setItem("conversation", params.get("c"));
```

```{verify}
:id: page-takes-id
:label: The page takes a conversation's id from its address
:substrate: contents
:trigger: after:take-id-from-address
contains page.html params.has("c")
```

## Start it

Now start a conversation under the id chosen on the welcome page,
{var}`first_conversation`, and ask about the book club and what a
ticket for an author evening costs.

```{url-open}
:id: ask-club
:title: Start a conversation about the shop's events
:url: http://127.0.0.1:{{ server_port }}/?c={{ first_conversation }}&ask=When+is+the+Harbour+book+club%2C+and+what+does+an+author+evening+ticket+cost%3F
:pane: chat
:label: Chat
:area: chat
```

The server had never seen that id, so it made a conversation for it,
and the SDK's session took the id for its own.

```{verify}
:id: first-conversation
:label: The first conversation has been had, under the chosen id
:substrate: script
:script: checks/first_conversation.py
:timeout: 150s
:trigger: after:ask-club
```

Think about where that conversation now is. The page has its id, in
the browser's storage. The server is holding a client for it, for as
long as the server runs. And the SDK has written it to a transcript, a
file under your home directory, filed by the directory the agent works
in.

The transcript is the only one of the three that lasts, and it is the
only one that is not tied to a single browser or a single run of the
server. Everything on the pages that follow is built on those files.

One thing follows from where they are kept. The SDK files transcripts
by the path of the working directory, and does not remove them when
this workshop is restarted. If you have taken this workshop before,
the conversations from that time are still there, and you will see
them listed.
