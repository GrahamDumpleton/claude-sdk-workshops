---
title: A skill for refunds
requires: [verify:skill-installed, verify:skill-in-place, verify:skill-used]
---

# A skill for refunds

The last thing to plug in is not a function. A skill is a set of
written instructions for one kind of job, in a file called `SKILL.md`,
which the agent reads only when the job comes up. Until then all it
knows of the skill is the one line description at the top of the file.

{open}`skills/refund-reply/SKILL.md` is the shop's way of answering a
customer who wants a refund: read the returns policy, decide, and
write the reply in a set form with the returns desk's reference on it.

## Put it where the SDK looks

The SDK finds a project's skills in one place, the directory
`.claude/skills` under the agent's working directory. JupyterLab does
not show directories whose names begin with a dot, so the skill is
shipped where you can read it, and the command below copies it to
where the SDK looks.

```{execute}
:id: install-skill
:title: Copy the skill into .claude/skills
:session: client
:wait: prompt
mkdir -p .claude/skills && cp -R skills/refund-reply .claude/skills/
```

```{verify}
:id: skill-installed
:label: The skill is where the SDK looks for it
:substrate: script
:script: checks/skill_installed.py
:trigger: after:install-skill
```

## Three options

A skill needs three things in the options.

- `"Skill"` in `tools`. Opening a skill is itself a tool the model
  asks for.

- `setting_sources=["project"]`, which tells the session to read the
  project's own configuration, the `.claude` directory included. Until
  now it was an empty list, and the session read none.

- `skills=["refund-reply"]`, which names the skill the model is to be
  shown.

```{editor-replace}
:id: add-skill-tool
:title: Give the agent the Skill tool
:path: app.py
:match: tools=["Read", "Glob", "Grep", "Write"],
:save: false
tools=["Read", "Glob", "Grep", "Write", "Skill"],
```

```{editor-replace}
:id: add-skill-options
:title: Read the project's settings, and name the skill
:path: app.py
:match: setting_sources=[],
setting_sources=["project"],
    skills=["refund-reply"],
```

```{verify}
:id: skill-in-place
:label: The server restarted with the skill named
:substrate: script
:script: checks/skill_in_place.py
:trigger: after:add-skill-options
```

```{hint}
:title: What else the project setting loads
The project source reads upward. The session is given the `CLAUDE.md`
of the working directory and of every directory above it, and finds
the skills of each. If the directory this workshop is kept in belongs
to a project with instructions or skills of its own, the agent is
given those instructions too. Naming the skill in `skills`, and not
asking for all of them, keeps the model to the one that belongs here.
```

## Ask for a refund reply

A customer bought a book thirty days ago, has the receipt, and wants
a refund. Ask for the reply.

```{url-open}
:id: ask-refund
:title: Ask for a reply to a customer who wants a refund
:url: http://127.0.0.1:{{ server_port }}/?new&ask=A+customer+bought+a+book+30+days+ago%2C+has+the+receipt%2C+and+wants+a+refund.+Write+our+reply.
:pane: chat
:label: Chat
:area: chat
```

The first tool line is `Skill`, with the name of the skill. Its
result is short: the instructions themselves arrive in the
conversation as a message, and the agent then follows them, reading
the returns policy and writing the reply the way the file says. The
reference on the reply is in the skill and nowhere else, which is how
the check knows the skill was used.

```{verify}
:id: skill-used
:label: The agent opened the skill and followed it
:substrate: script
:script: checks/skill_used.py
:timeout: 150s
:trigger: after:ask-refund
```
