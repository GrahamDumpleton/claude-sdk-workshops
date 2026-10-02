---
title: Put the skill where the SDK looks
requires: [verify:skill-installed]
---

# Put the skill where the SDK looks

A skill is a directory with a file named `SKILL.md` in it. There is
nothing to register and nothing to pass in code: the SDK finds skills
by where they are. For a project, that place is `.claude/skills/` in
the agent's working directory, with a directory for each skill:

```text
.claude/skills/refund-reply/SKILL.md
```

The file has two parts, and you have read both.

- **The front matter**, between the `---` lines. `name` is what the
  skill is called, and `description` says what it is for and when to
  use it. The description is the only part the model is shown to
  begin with, so it does the job a tool's description does: it is how
  the model decides.

- **The body**, everything after. It is ordinary Markdown, written to
  be followed, and can be as long as the procedure needs.

The skill is shipped with this workshop in a plain `skills` folder,
because JupyterLab does not show directories whose names begin with a
dot and you would not have been able to open it. This cell copies it
to where the SDK looks.

```{cell-insert}
:id: insert-install
:path: {{ notebook }}
:tags: [install]
:run: true
installed = Path(".claude/skills/refund-reply")

shutil.copytree("skills/refund-reply", installed, dirs_exist_ok=True)

skill_text = (installed / "SKILL.md").read_text()
front_matter, body = skill_text.split("---\n", 2)[1:]

print("installed at         :", installed / "SKILL.md")
print("front matter, words  :", len(front_matter.split()))
print("body, words          :", len(body.split()))
```

The last two lines count the words in each part. Keep the two sizes in
mind: the difference between them is what a skill saves.

```{verify}
:id: skill-installed
:label: The skill is where the SDK looks for it
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed install
(installed / "SKILL.md").exists() and len(body.split()) > len(front_matter.split())
```

```{hint}
:title: Other places a skill can live
A skill in `.claude/skills/` under your home directory is a personal
one, found when `setting_sources` includes `"user"`. A skill's
directory can also hold other files beside `SKILL.md`, such as a
template or a script, which the body tells the agent to read or run
when the procedure reaches that step. They cost nothing until then.
```
