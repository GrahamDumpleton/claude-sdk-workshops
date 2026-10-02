---
title: What else the option lets in
---

# What else the option lets in

`setting_sources` takes three names, and each loads more than
instructions.

| Source | Where it looks | What it loads |
| --- | --- | --- |
| `"project"` | The working directory and the directories above it | `CLAUDE.md` and rules files, the project's settings and hooks, its skills and its subagents |
| `"user"` | The `.claude` directory in your home directory | Your own `CLAUDE.md`, settings, skills and subagents |
| `"local"` | The working directory | `CLAUDE.local.md` and local settings, the ones kept out of version control |

Leave the option out altogether and the SDK loads all three, as Claude
Code does when you run it yourself.

That default is the reason these workshops set the option to an empty
list in every cell. With it left out, an agent you run picks up
whatever you have told Claude Code at home: your own instructions,
your settings, skills you installed for other work. The agent would
behave differently on your machine than on anyone else's, and
differently next month than today, for reasons that are nowhere in its
code. An agent built for a job should be given its instructions on
purpose.

So the rule is:

- Start from `setting_sources=[]`, and say everything in code.

- Add `"project"` when the agent works on a project that carries its
  own instructions, and you want it to follow them.

- Add `"user"` only for an agent that is meant to be yours alone.

## Two things the option does not cover

Two inputs reach a session whatever the option says.

- **Notes Claude Code keeps about a project.** If Claude Code has been
  used in a directory, it may have saved notes there for itself, and
  a session started in that directory is sent the list of them. They
  showed as a file of type `AutoMem` if you had any. Passing
  `settings='{"autoMemoryEnabled": false}'` in the options turns
  that off.

- **The connectors of your Claude account**, such as mail and
  calendar, which arrive as tools. `strict_mcp_config=True` keeps
  them out, which is why every agent here sets it.

Neither matters for an agent you run for yourself. Both matter the day
an agent you wrote runs for someone else.
