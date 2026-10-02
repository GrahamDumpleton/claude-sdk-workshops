---
title: Two calls that do not know each other
requires: [verify:nothing-remembered]
---

# Two calls that do not know each other

Start with what does not work. The first cell tells the agent a fact
that is in no file and that it could not guess: a stock code for a
book. The agent has no tools. All it can do is take the fact in and
reply.

Every run happens inside a session, and each session has an id, which
the result reports. The cell prints it.

```{cell-insert}
:id: insert-told
:path: {{ notebook }}
:tags: [told]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "Answer in one sentence."
    ),
    tools=[],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=3,
)

tell = "The stock code for the harbour atlas is TW-4471-K. Say that you have noted it."
ask = "What is the stock code for the harbour atlas?"

async for message in query(prompt=tell, options=options):
    if isinstance(message, ResultMessage):
        told = message

print(told.result)
print("session:", told.session_id)
```

The agent said it had noted the code. Now ask for it back, with a
second call to `query()` and the same options.

```{cell-insert}
:id: insert-asked
:path: {{ notebook }}
:tags: [asked]
:run: true
async for message in query(prompt=ask, options=options):
    if isinstance(message, ResultMessage):
        asked = message

print(asked.result)
print("session:", asked.session_id)
```

It does not know. Look at the two session ids: they are different.
Each call to `query()` started a session of its own, ran one exchange
in it and ended. The second session was never sent what was said in
the first, and the model has no memory of its own to fall back on.

Nothing went wrong. That is what `query()` is: one question, one
answer, and nothing carried over.

```{verify}
:id: nothing-remembered
:label: The second call was a new session and did not know the code
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed asked
if told.session_id == asked.session_id:
    print("Both calls report the same session. Run the two cells again, in order.")
elif "TW-4471-K" in (asked.result or ""):
    print("The second call gave the code, which it was never told. Run the two cells again, in order.")
told.session_id != asked.session_id and "TW-4471-K" not in (asked.result or "")
```
