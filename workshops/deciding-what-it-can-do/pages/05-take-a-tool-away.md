---
title: Take a tool away
requires: [verify:tool-removed]
---

# Take a tool away

`allowed_tools` and the modes open things up. `disallowed_tools` is
the other direction: a list of tools the agent must not have. It is
applied before everything else, and nothing set elsewhere can
override it.

The fourth attempt keeps the mode that approved the write a moment
ago, and puts `Write` on that list.

```{cell-insert}
:id: insert-fourth
:path: {{ notebook }}
:tags: [fourth]
:run: true
fourth = await attempt(permission_mode="acceptEdits", disallowed_tools=["Write"])

report(fourth)
```

Look at **tools given**. `Write` is not there, although the function
still passed `tools=["Read", "Write"]`. A tool named in
`disallowed_tools` is taken out before the model is told what exists.

Now look at **tools asked for**. The model may have asked for `Write`
all the same. It was told to write a file, and it knows from its
training that agents like this one usually have a tool of that name,
so it can ask for a tool it was never offered. If it did, an error came
back saying there is no such tool in this session.

That makes this different from the first attempt. There, the tool
existed and a call to it was refused, so there was something under
**calls denied**. Here there was nothing to approve or refuse, and
that list is empty. Either way the agent could only read, and then say
that it had no way to write the file.

Use the list for what an agent must never be able to do, whatever
mode it runs in and whatever other code adds to its options later.

```{verify}
:id: tool-removed
:label: The tool was taken away and nothing was written
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed fourth
if "Write" in fourth["tools"]:
    print("The session was still given Write. Check that the cell passes disallowed_tools=[\"Write\"].")
elif fourth["written"]:
    print("The notice exists, so something wrote it. Run the cell again.")
"Write" not in fourth["tools"] and fourth["denied"] == [] and not fourth["written"]
```

```{hint}
:title: Why not just leave it out of tools
For one agent, leaving `Write` out of `tools` does the same job, and
is simpler. `disallowed_tools` is for when the list of tools is not
yours to write: a session that starts from every built-in tool, or
tools that arrive from elsewhere, which later workshops add. A deny
list says what must not be there without having to know everything
that is.
```
