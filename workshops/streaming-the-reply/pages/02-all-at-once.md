---
title: All at once
requires: [verify:reply-arrived-whole]
---

# All at once

First, measure the wait. The agent is asked for a few paragraphs,
which is long enough to take a moment, and the cell notes how many
seconds pass before anything of the reply reaches your code.

Watch the cell while it runs. There is nothing to see until it has
finished.

```{cell-insert}
:id: insert-whole
:path: {{ notebook }}
:tags: [whole]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt="You are the assistant for Tidewater Books, a small bookshop by a harbour.",
    tools=[],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=3,
)

prompt = (
    "Write about 200 words welcoming a new customer to the shop. "
    "Plain paragraphs, with no headings."
)

whole_reply = ""
arrived = None
started = time.monotonic()

async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        arrived = time.monotonic() - started
        for block in message.content:
            if isinstance(block, TextBlock):
                whole_reply += block.text

print(f"nothing for {arrived:.1f} seconds, then {len(whole_reply)} characters at once")
print()
print(whole_reply)
```

The first line of the output is the measurement: the seconds that
passed with nothing to show, and the size of what then arrived in one
piece. The model was writing for all of that time. Your code was not
told until the reply was complete.

A few seconds is bearable. A reply three times as long takes three
times as long, and an agent that works through several tools before
it answers adds to it again.

```{verify}
:id: reply-arrived-whole
:label: The reply arrived in one piece, after a wait
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed whole
arrived is not None and len(whole_reply) > 0
```
