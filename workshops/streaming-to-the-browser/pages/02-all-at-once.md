---
title: A reply that arrives all at once
requires: [verify:whole-reply]
---

# A reply that arrives all at once

First see the wait. The question below needs more than a line in
answer: the agent is asked to describe each of the shop's events for a
new member of staff. Watch the chat while it runs.

```{url-open}
:id: ask-events
:title: Ask for a description of the shop's events
:url: http://127.0.0.1:{{ server_port }}/?ask=Read+shop%2Fevents.md+and+describe+each+event+in+a+sentence+or+two%2C+for+a+new+member+of+staff.
:pane: chat
:label: Chat
:area: chat
```

Three dots, and then every word together. The check's message says how
long the run took.

```{verify}
:id: whole-reply
:label: The reply arrived after the run had ended
:substrate: script
:script: checks/whole_reply.py
:timeout: 150s
:trigger: after:ask-events
```

Most of that time the model was writing. The route in {open}`app.py`
lets every message of the run go by until the `ResultMessage`, which
comes when the run is over, and answers the page only then. By that
point the words had existed for seconds, a few more of them every
moment, and nobody had been shown one.

The fix has two halves. The server has to send each piece of the reply
when it gets it, and the page has to show each piece when it arrives.
