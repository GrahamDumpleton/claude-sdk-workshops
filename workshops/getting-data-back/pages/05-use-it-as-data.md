---
title: Use it as data
requires: [verify:data-used]
---

# Use it as data

Now the question the first page could not answer. With the hours as
data, it takes a few lines of ordinary Python, and no model: look the
day up, and compare the time with the opening and closing times. Times
written as `HH:MM` compare correctly as text.

```{cell-insert}
:id: insert-used
:path: {{ notebook }}
:tags: [used]
:run: true
by_day = {entry["day"]: entry for entry in hours["days"]}


def is_open(day, time):
    entry = by_day[day]
    if entry["opens"] is None:
        return False
    return entry["opens"] <= time < entry["closes"]


for day, time in [
    ("Saturday", "16:30"),
    ("Saturday", "17:00"),
    ("Sunday", "11:30"),
    ("Monday", "12:00"),
]:
    print(day, time, "->", "open" if is_open(day, time) else "closed")
```

Check the four answers against {open}`shop/opening-hours.md`. The
shop shuts early on a Saturday, and the code knows it, because the
agent read it in the file and returned it as a value.

The agent was called once. Every question after that was answered by
your own code, instantly and for nothing, and the same way each time.
That is the pattern for using an agent inside a program: let the agent
do the part that needs reading and judgement, get its conclusion back
as data, and do the rest in code.

```{verify}
:id: data-used
:label: Code answered from the data the agent returned
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed used
(
    is_open("Saturday", "16:30")
    and not is_open("Saturday", "17:00")
    and is_open("Sunday", "11:30")
    and not is_open("Monday", "12:00")
)
```
