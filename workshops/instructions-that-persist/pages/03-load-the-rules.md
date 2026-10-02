---
title: Load the rules
requires: [quiz:what-reaches-the-model, verify:rules-loaded]
---

# Load the rules

`setting_sources` is a list of the places the SDK may load from. One
of them is `"project"`, which stands for the directory the agent works
in. With it in the list, the SDK reads the `CLAUDE.md` there and puts
its contents in front of the model at the start of the session, ahead
of anything you ask.

Nothing else changes. The system prompt and the request are the ones
the last run used, and neither mentions the rules.

```{quiz}
:id: what-reaches-the-model
:title: What reaches the model
question: "The options name no file, and the request does not mention any rules. With `setting_sources=[\"project\"]`, how do the house rules reach the model?"
options:
  - text: "The model reads the file with a tool when it decides it needs to."
    explanation: "This agent has no tools. The file is loaded by the SDK before the model is asked anything."
  - text: "The SDK finds `CLAUDE.md` in the working directory and sends its contents with the request."
    correct: true
  - text: "They do not. A file has to be named in the system prompt to be used."
    explanation: "`CLAUDE.md` is found by its name and where it is. Nothing in the options has to mention it."
  - text: "The model was trained on the shop's rules."
    explanation: "The shop is made up, and its rules exist only in the file."
explanation: "The SDK loads the file because of where it is and what it is called. The model is sent its contents as part of every request."
```

```{cell-insert}
:id: insert-loaded
:path: {{ notebook }}
:tags: [loaded]
:run: true
loaded = await ask(["project"])

show(loaded)
```

The list now has a file of type `Project`: the `CLAUDE.md` you read.
The reply follows it. It ends with the shop's sign-off, a line the
model could not have guessed, and it should promise no date and give
the price to the cent.

You may see more than one `Project` file. The SDK loads the
`CLAUDE.md` of the working directory and of every directory above it,
so that a rule set at the top of a project holds in every part of it.
If the folder these workshops are in sits inside a project that has a
`CLAUDE.md` of its own, that file was loaded too, and its rules
reached this agent. Keep that in mind when you choose where an agent
runs.

```{verify}
:id: rules-loaded
:label: The house rules were loaded and the reply follows them
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed loaded
if not given_house_rules(loaded):
    print("The session was not given this workshop's CLAUDE.md. Check that the cell passes [\"project\"].")
elif "Fair winds" not in loaded["result"].result:
    print("The reply does not carry the shop's sign-off. Run the cell again.")
given_house_rules(loaded) and "Fair winds" in loaded["result"].result
```

```{hint}
:title: Other files the project source loads
`"project"` covers more than one file. It also loads any Markdown
files under `.claude/rules/`, which is a way to split a long set of
instructions by subject, and a `CLAUDE.md` kept at `.claude/CLAUDE.md`
in place of the top of the directory. A `CLAUDE.md` in a directory
below the working directory is loaded later, when the agent first
reads a file there.
```
