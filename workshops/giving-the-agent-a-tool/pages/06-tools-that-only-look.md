---
title: Tools that only look
requires: [verify:timed-tools-defined, verify:ran-one-by-one, verify:ran-side-by-side]
---

# Tools that only look

A model can ask for several tools in one reply. Asked about three
books, it will usually ask for three lookups at once. The SDK then has
a decision to make: run them one after another, or all together.

It cannot tell from the outside whether your function changes
anything. Two calls that both write to the same record must not run at
once. So unless it is told otherwise, the SDK plays safe and runs the
calls to your tools one at a time.

A tool can say that it only looks. `@tool` takes `annotations`, and
`ToolAnnotations(readOnlyHint=True)` declares that the tool changes
nothing. Calls to tools marked that way are run side by side.

To make the difference visible, the handler in this cell waits one
second before it answers, as a slow database would, and records when
each call started and finished. It is wrapped twice, once plain and
once marked read-only. The cell calls nothing.

```{cell-insert}
:id: insert-timed
:path: {{ notebook }}
:tags: [timed]
:run: true
timings = []


async def slow_check_stock(args):
    started = time.monotonic()
    await asyncio.sleep(1)
    reply = await check_stock.handler(args)
    timings.append((args["title"], started, time.monotonic()))
    return reply


plain_server = create_sdk_mcp_server(
    name="shop",
    version="1.0.0",
    tools=[tool("check_stock", check_stock.description, {"title": str})(slow_check_stock)],
)

read_only_server = create_sdk_mcp_server(
    name="shop",
    version="1.0.0",
    tools=[
        tool(
            "check_stock",
            check_stock.description,
            {"title": str},
            annotations=ToolAnnotations(readOnlyHint=True),
        )(slow_check_stock)
    ],
)

three_books = (
    "How many copies do we have of each of these: The Ferry Almanac, Tidewater, Low Water?"
)


def show_timings(calls):
    zero = min(started for _, started, _ in calls)
    for title, started, finished in sorted(calls, key=lambda call: call[1]):
        print(f"{title:<20} started {started - zero:4.1f}s   finished {finished - zero:4.1f}s")


def overlapped(calls):
    ordered = sorted(calls, key=lambda call: call[1])
    return any(later[1] < earlier[2] for earlier, later in zip(ordered, ordered[1:]))


print("ready to time:", three_books)
```

```{verify}
:id: timed-tools-defined
:label: The timed tools are defined
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed timed
plain_server["type"] == "sdk" and read_only_server["type"] == "sdk"
```

## One at a time

First the plain tool, which says nothing about what it does.

```{cell-insert}
:id: insert-one-by-one
:path: {{ notebook }}
:tags: [one-by-one]
:run: true
timings.clear()

await ask(three_books, plain_server)

one_by_one = list(timings)

print()
show_timings(one_by_one)
```

Look at the times under the answer. Each lookup started when the one
before it had finished, though the model asked for them together.

```{verify}
:id: ran-one-by-one
:label: The plain tool's calls ran one after another
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed one-by-one
if len(one_by_one) < 2:
    print("The model made fewer than two lookups. Run the cell again.")
len(one_by_one) >= 2 and not overlapped(one_by_one)
```

## Side by side

Now the same handler behind the tool that is marked read-only.

```{cell-insert}
:id: insert-side-by-side
:path: {{ notebook }}
:tags: [side-by-side]
:run: true
timings.clear()

await ask(three_books, read_only_server)

side_by_side = list(timings)

print()
show_timings(side_by_side)
```

The lookups now start within a moment of each other and finish
together, so three slow calls take about the time of one. Nothing in
the function changed. One line told the SDK it was safe.

The annotation is a promise and nothing checks it. A tool marked
read-only that writes to a file will be run alongside others all the
same, so mark a tool only when it is true.

```{verify}
:id: ran-side-by-side
:label: The read-only tool's calls overlapped
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed side-by-side
if len(side_by_side) < 2:
    print("The model made fewer than two lookups. Run the cell again.")
elif not overlapped(side_by_side):
    print("The model asked for the books one at a time on this run. Run the cell again.")
len(side_by_side) >= 2 and overlapped(side_by_side)
```
