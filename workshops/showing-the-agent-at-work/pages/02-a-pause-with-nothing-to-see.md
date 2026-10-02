---
title: A pause with nothing to see
requires: [verify:worked-unseen]
---

# A pause with nothing to see

Ask something that takes more than one file to answer: which of the
shop's events are on a weekday evening, and whether the shop is still
open when each one starts. The events are in one file and the opening
hours in another. Watch the chat from the moment you click.

```{url-open}
:id: ask-events
:title: Ask which events start after the shop has closed
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Which+of+the+shop%27s+events+are+on+a+weekday+evening%2C+and+is+the+shop+still+open+when+each+one+starts%3F
:pane: chat
:label: Chat
:area: chat
```

Three dots, for longer than a short answer takes to write. The agent
was not waiting. In that time it asked for a tool several times, and
the SDK ran each one and sent the result back to the model. The
check's message says how many turns the run took.

```{verify}
:id: worked-unseen
:label: The run took several turns, and the page was told of none
:substrate: script
:script: checks/worked_unseen.py
:timeout: 150s
:trigger: after:ask-events
```

Where the model wrote something before it had finished looking, as it
sometimes does, the page ran that together with the answer in one
bubble. It has no way to know that anything happened in between.

Every step of that work passed through the server. `turn()` in
{open}`app.py` reads each message of the run from the client, and
`events_for()` decides what the page is told about each. It was
handed the model's tool requests and the results that came back, and
for each of them it yielded nothing.
