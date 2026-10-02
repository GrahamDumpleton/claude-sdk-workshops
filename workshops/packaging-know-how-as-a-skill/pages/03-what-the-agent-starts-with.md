---
title: What the agent starts with
requires: [verify:only-the-description]
---

# What the agent starts with

Three options put the skill within the agent's reach, and each does a
different job.

- `setting_sources=["project"]` lets the SDK look in the working
  directory, which is how the skill is found. It also loads the
  project's instruction files, as **Give instructions that persist**
  showed.

- `skills=["refund-reply"]` names the skills the model may use. A
  session finds more skills than yours: Claude Code comes with some of
  its own. Naming the ones you want keeps the rest out of the model's
  sight. `skills="all"` would enable every one that is found, and
  `skills=[]` none.

- `"Skill"` in `tools` gives the agent the built-in tool that loads a
  skill. A skill is not itself a tool. The model asks for the `Skill`
  tool and says which skill it wants. The other two tools, `Glob` and
  `Read`, are for finding and reading the shop's documents.

This cell makes the options, connects a client long enough to ask
what is in the model's context, and disconnects. No model is called.

```{cell-insert}
:id: insert-context
:path: {{ notebook }}
:tags: [context]
:run: true
options = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "The shop's documents are in the shop directory. Do what is asked and nothing more."
    ),
    tools=["Glob", "Read", "Skill"],
    setting_sources=["project"],
    skills=["refund-reply"],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=10,
)

async with ClaudeSDKClient(options=options) as client:
    context = await client.get_context_usage()

skills_found = context["skills"]["totalSkills"]
skills_enabled = {entry["name"]: entry["tokens"] for entry in context["skills"]["skillFrontmatter"]}

print("skills the session found   :", skills_found)
print("skills the model is shown  :", skills_enabled)
```

The session found more skills than the one you installed, and the
model is shown one: `refund-reply`. The number beside it is what it
costs to have the skill available, in tokens, the unit the model reads
in. A token is about the size of a short word, and that number is the
size of the description alone.

The body is not there. It is on disk, where it costs nothing, and
that is the design: an agent can have fifty skills and carry fifty
short descriptions, and never pay for a body it does not use.

```{verify}
:id: only-the-description
:label: The model starts with the description and not the body
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed context
if "refund-reply" not in skills_enabled:
    print("The session did not find the skill. Run the cell on the page before, then this one again.")
"refund-reply" in skills_enabled and skills_enabled["refund-reply"] < len(body.split())
```
