---
title: What the session was given
requires: [verify:init-read]
---

# What the session was given

Open the first message. A `SystemMessage` has a `subtype` saying what
it reports, and the one with the subtype `init` describes the session
the SDK started. Its `data` is a dictionary.

This cell makes no call to the model. It reads the messages you
already have.

```{cell-insert}
:id: insert-init
:path: {{ notebook }}
:tags: [init]
:run: true
init = next(
    message
    for message in messages
    if isinstance(message, SystemMessage) and message.subtype == "init"
)

print("model     :", init.data["model"])
print("tools     :", init.data["tools"])
print("directory :", init.data["cwd"])
print("api key   :", init.data["apiKeySource"])
```

Four things the agent was set up with:

- **model** is the full name that `haiku` stood for.

- **tools** is empty, because the options said `tools=[]`. This agent
  can do nothing but reply.

- **directory** is the agent's working directory: this workshop's own
  folder of files. An agent that is given file tools works from here.

- **api key** says where the credential came from. `none` means no API
  key was found, so the run used your Claude login.

```{verify}
:id: init-read
:label: The session had a model and no tools
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed init
if init.data["tools"] != []:
    print("The session was given tools:", init.data["tools"], "- the cell on the previous page should say tools=[].")
bool(init.data["model"]) and init.data["tools"] == []
```

```{hint}
:title: If api key shows something other than none
An API key was found, most likely in the `ANTHROPIC_API_KEY`
environment variable of the shell JupyterLab was started from, and the
SDK used it in preference to your login. The workshop works the same
way. The difference is that each run is billed to that key.
```
