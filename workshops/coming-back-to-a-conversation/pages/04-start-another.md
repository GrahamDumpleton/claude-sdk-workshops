---
title: Start another
requires: [verify:second-conversation]
---

# Start another

Start a second conversation, about something else: whether a book is
in stock.

```{url-open}
:id: ask-stock
:title: Start a second conversation, about a book
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Is+the+book+Low+Water+in+stock%2C+and+which+shelf+is+it+on%3F
:pane: chat
:label: Chat
:area: chat
```

```{verify}
:id: second-conversation
:label: A second conversation has been had
:substrate: script
:script: checks/second_conversation.py
:timeout: 150s
:trigger: after:ask-stock
```

The list in the page was read as the page loaded, before this
conversation existed. Load the page again to bring it up to date.

```{url-open}
:id: reload-chat
:title: Load the chat again
:url: http://127.0.0.1:{{ server_port }}/
:pane: chat
:label: Chat
:area: chat
```

Unfold **Conversations** and there are two, the new one in bold.

Until this workshop, starting a new conversation meant losing the old
one. The page forgot the old id, and nothing else knew it. Now the
first conversation is a click away. Click it in the list if you like:
the page loads with its id in the address, and the first exchange is
on the screen again.
