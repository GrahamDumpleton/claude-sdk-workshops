---
title: What it cost
requires: [verify:cost-read]
---

# What it cost

The result carries one more number, in dollars.

```{cell-insert}
:id: insert-cost
:path: {{ notebook }}
:tags: [cost]
:run: true
cost = result.total_cost_usd

print("total_cost_usd :", cost)
print("in cents       :", round(cost * 100, 2))
```

Be careful what you read into it. `total_cost_usd` is an estimate, made
by the SDK on this machine: the token counts from the last page
multiplied by the published price of each kind of token on the model
that was used. It is what the run would cost someone paying for the API
by the token.

With a subscription login, nobody is charged that amount. A
subscription is a fixed price with limits on how much can be used in a
period of time, and the tokens of this run counted towards those
limits. So here the figure is a measure of size. It is still the
handiest single number for comparing two runs, and later workshops use
it for that.

```{verify}
:id: cost-read
:label: The result carries an estimated cost
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed cost
isinstance(cost, float) and cost > 0
```

## Where you stand against your plan

For a subscriber the question that matters is how much of the plan is
used. The service says so during a run, and the SDK passes it on as a
`RateLimitEvent`, a message in the stream beside the others. The first
cell of the workshop kept every message, so the event is there to be
read.

```{cell-insert}
:id: insert-limits
:path: {{ notebook }}
:tags: [limits]
:run: true
events = [message for message in messages if isinstance(message, RateLimitEvent)]

if not events:
    print("This run carried no rate limit event. A run on an API key does not.")

for event in events:
    info = event.rate_limit_info
    print("status :", info.status)
    print("limit  :", info.rate_limit_type)
    for name, window in info.raw.get("unifiedWindows", {}).items():
        print(name, "used :", format(window.get("utilization", 0), ".0%"))
```

- **status** is `allowed` while there is room, `allowed_warning` when a
  limit is close, and `rejected` once it has been reached.

- **limit** names the limit the status is about. A plan has more than
  one: `five_hour` is a limit on use within any five hours, and
  `seven_day` on use within a week.

- The lines after that give the share of each limit used so far, where
  the service reports it. They come from `raw`, the event as the
  service sent it, which the SDK passes through without describing, so
  what it holds may change.

One small run moves those figures very little, which is the point of
running the workshops on the smallest model.
