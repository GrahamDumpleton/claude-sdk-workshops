---
title: The Claude Code preset
requires: [quiz:how-much-larger, verify:third-answered]
---

# The Claude Code preset

The SDK is Claude Code, the coding assistant, driven from your own
program. Claude Code works under a long system prompt of its own:
how to use each tool, how to go about a piece of programming work, how
to report what it did, what to be careful of. The SDK offers that
prompt as a preset named `claude_code`.

A preset is asked for with a dictionary in place of a string. Its
`append` key adds text of yours to the end, so the agent gets Claude
Code's instructions followed by the shop's.

```{quiz}
:id: how-much-larger
:title: How much larger
question: "The next run asks the same question, with the same one tool. Only the system prompt changes, to the preset with the shop's prompt appended. How will the first request sent to the model compare in size with the first run's?"
options:
  - text: "About the same. The shop's prompt is still the part that matters."
    explanation: "The model is sent all of the system prompt on every request, whether or not this question needs it."
  - text: "A little larger, by a paragraph or so."
    explanation: "The preset is far longer than a paragraph. It is the full set of instructions for a coding assistant."
  - text: "Several times larger."
    correct: true
  - text: "Smaller, because the preset is built in and does not have to be sent."
    explanation: "Nothing is built into the model. A preset is text like any other, and it is sent with every request."
explanation: "The preset carries thousands of tokens of instructions for programming work. They are sent with every request of every turn, whatever the agent is asked."
```

```{cell-insert}
:id: insert-third
:path: {{ notebook }}
:tags: [third]
:run: true
preset_prompt = {
    "type": "preset",
    "preset": "claude_code",
    "append": shop_prompt,
}

third, third_size = await ask(preset_prompt)

print(third.result)
```

The reply reads much like the first one. The agent still answered as
the shop's assistant, from the policy, because the appended text told
it to. What changed is what it took to get there, which the next page
measures.

```{verify}
:id: third-answered
:label: The agent answered under the preset
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed third
if third.subtype != "success":
    print("The run ended with", third.subtype, "- run the cell again.")
third.subtype == "success" and third_size > 0
```
