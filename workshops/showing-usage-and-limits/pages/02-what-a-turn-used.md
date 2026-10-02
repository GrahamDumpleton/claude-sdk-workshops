---
title: What a turn used
requires: [verify:usage-in-place, verify:page-shows-usage, verify:usage-shown]
---

# What a turn used

The `ResultMessage` that ends each turn carries a `usage` dictionary,
and on a client that stays connected it covers that one turn. Four of
its counts matter.

- `input_tokens`, `cache_creation_input_tokens` and
  `cache_read_input_tokens` add up to what the model was sent, over
  every request the turn made. The three differ in how they are
  charged, and the last two are about the cache, described below.

- `output_tokens` is what the model wrote.

## Send the counts to the page

The `done` event is the natural place for them. In {open}`app.py`,
`events_for()` adds the three input counts together as `sent`, and
gives the output count as `written`.

```{editor-replace}
:id: usage-in-done
:title: Put what the turn used in the done event
:path: app.py
:regex: true
:match: ^        yield \{"type": "done", "ended": message\.subtype, .*$
:save: false
        usage = message.usage or {}
        yield {
            "type": "done",
            "ended": message.subtype,
            "seconds": round(message.duration_ms / 1000, 1),
            "sent": usage.get("input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0),
            "written": usage.get("output_tokens", 0),
        }
```

The server keeps the same figure with its record of the run.

```{editor-replace}
:id: note-usage
:title: Keep what was sent with the run
:path: app.py
:regex: true
:match: ^            runs\.append\(summary\(message, resumed=self\.resumed, calls=self\.calls, answers=self\.answers\)\)$
            runs.append(
                summary(
                    message,
                    resumed=self.resumed,
                    calls=self.calls,
                    answers=self.answers,
                    sent=event["sent"],
                )
            )
```

```{verify}
:id: usage-in-place
:label: The server restarted, and reports what each turn used
:substrate: script
:script: checks/usage_in_place.py
:trigger: after:note-usage
```

## A line for them in the page

{open}`page.html` gets a line under the conversation, and `send()`
fills it in when the turn is done. If the run ended any way but well,
the line says how.

```{editor-insert}
:id: add-status-line
:title: Add a line under the conversation
:path: page.html
:match: <main id="messages"></main>
:position: after
<p id="status"></p>
```

```{editor-insert}
:id: fill-status-line
:title: Fill the line in when a turn is done
:path: page.html
:match: if (!written) reply.remove();
:position: after
      document.getElementById("status").textContent =
        `${event.seconds}s, ${event.sent} tokens sent, ${event.written} written` +
        (event.ended === "success" ? "" : `, ended: ${event.ended}`);
```

```{verify}
:id: page-shows-usage
:label: The page shows what a turn used
:substrate: contents
:trigger: after:fill-status-line
contains page.html event.sent
```

## Ask something

```{url-open}
:id: ask-lamp-keeper
:title: Ask whether The Lamp Keeper is in stock
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Is+the+book+The+Lamp+Keeper+in+stock%3F
:pane: chat
:label: Chat
:area: chat
```

The line under the conversation shows the turn. Look at the two
counts side by side: the model was sent thousands of tokens and wrote
a few dozen. A short question is not a small request. With it went
the standing instructions, the description of every tool, and
whatever the project's settings add, and all of that goes again with
every request, of which this turn made at least two.

```{verify}
:id: usage-shown
:label: A turn was made, and its usage was reported
:substrate: script
:script: checks/usage_shown.py
:timeout: 150s
:trigger: after:ask-lamp-keeper
```

```{hint}
:title: What the cache does to the cost
Most of what is sent is the same from one request to the next, and
the service that runs the model keeps a recent request's beginning
for a few minutes. A request that starts the same way is charged a
fraction of the usual price for the part that repeats. That is the
cache, and it is why the three input counts are kept apart: tokens
read from the cache cost much less than tokens sent fresh, and tokens
written to it a little more.

Added together they are the size of what the model was sent, which is
what the page shows. The price is a separate question, and the result
answers it too.
```

```{hint}
:title: Why the page shows tokens and not money
The result also carries `total_cost_usd`, an estimate of what the
session has cost at the prices of the API. On a subscription nothing
is charged for each run, and the same tokens count against the plan's
usage limits, so a figure in dollars would be about a bill that is
never sent. Tokens are true either way.
```
