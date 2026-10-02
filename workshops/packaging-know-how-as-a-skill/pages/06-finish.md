---
title: What you know now
requires: [quiz:skill-or-instruction-file]
---

# What you know now

An agent can carry procedures it loads only when they are needed.

- A skill is a directory holding a `SKILL.md`: a name and a
  description in the front matter, and a body of instructions.

- The SDK finds project skills in `.claude/skills/` when
  `setting_sources` includes `"project"`. `skills=[...]` names the
  ones the model may use, and `"Skill"` in `tools` is the tool that
  loads one.

- Only the description is sent to begin with. The model asks for the
  skill when the description fits the request, and the body arrives
  as the result.

- The description is therefore what decides whether a skill is used.
  Say what it is for and when to reach for it.

- A skill is written once, as a file, and serves Claude Code as well
  as the agents you build.

```{quiz}
:id: skill-or-instruction-file
:title: Skill or instruction file
question: "Which of these belongs in a skill, and not in the project's `CLAUDE.md`?"
options:
  - text: "Every reply to a customer is signed with the shop's sign-off."
    explanation: "A rule that applies to everything the agent writes should be in front of it all the time. That is what `CLAUDE.md` is for."
  - text: "The fifteen steps for writing up the monthly author evening for the newsletter."
    correct: true
  - text: "Prices are given in dollars and cents."
    explanation: "A short rule that always applies costs little to send every time and should never be missing."
  - text: "The agent's name and what it is for."
    explanation: "That belongs in the system prompt, which your code sends with every request."
explanation: "Put what is always needed where it is always sent. Put a long procedure that is needed now and then in a skill, where it waits behind one line of description."
```

## What comes next

These last two workshops were about what an agent knows. The next
ones are about what it may do. **Ask before acting** puts a function
of yours in front of each thing the agent wants to change, to allow
it, refuse it or alter it.

Press Finish below to end the workshop.
