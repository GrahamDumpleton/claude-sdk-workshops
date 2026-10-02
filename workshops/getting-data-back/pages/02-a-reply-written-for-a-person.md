---
title: A reply written for a person
requires: [verify:prose-kept]
---

# A reply written for a person

Suppose a program needs to know whether the bookshop is open at a
given time, to decide whether to send a customer there today. The
hours are in {open}`shop/opening-hours.md`, so it asks an agent that
can read the file.

```{cell-insert}
:id: insert-prose
:path: {{ notebook }}
:tags: [prose]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for Tidewater Books, a small bookshop. "
        "Answer from the shop's documents."
    ),
    tools=["Read"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=8,
)

question = "What are the shop's opening hours? They are in shop/opening-hours.md."

async for message in query(prompt=question, options=options):
    if isinstance(message, ResultMessage):
        prose = message

print(prose.result)
```

A person can read that and tell at once whether the shop is open at
five on a Saturday. Now try it as a program. The result is a string,
so the cell does what code can do with a string: it searches for
everything that looks like a time.

```{cell-insert}
:id: insert-scraped
:path: {{ notebook }}
:tags: [scraped]
:run: true
times_found = re.findall(r"\d{1,2}:\d{2} ?[ap]m", prose.result)

print("times found in the reply :", times_found)
print("structured_output        :", prose.structured_output)
```

The times are all there, and the code has no idea what any of them
means. Which is an opening time and which a closing time, which day
each belongs to, where the day the shop is shut went: all of that was
in how the reply was laid out, as a table or a list or a sentence.
The layout is different on every run, because the model words each
reply afresh. Code written to pick this reply apart would break on
the next one.

The second line is the field this workshop is about. A result has a
`structured_output` beside its `result`, and on an ordinary run it is
empty.

```{verify}
:id: prose-kept
:label: The agent answered in prose, with no structured output
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed scraped
if prose.subtype != "success":
    print("The run ended with", prose.subtype, "- run the first cell on this page again.")
prose.subtype == "success" and prose.structured_output is None
```
