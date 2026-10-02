---
title: An agent without the rules
requires: [verify:ask-defined, verify:rules-not-loaded]
---

# An agent without the rules

The house rules are in a file in the agent's working directory. That
alone does nothing. Whether a session is given the file is decided by
one option, `setting_sources`, and every agent in these workshops so
far has set it to an empty list.

The same request is made twice in this workshop with only that option
changed, so the first cell defines a function for the run. `ask()`
takes the value of `setting_sources`, connects a client, and does two
things with it:

- It asks the client which instruction files the session was given.
  `get_context_usage()` reports what is in the model's context, the
  text it is sent with each request, and lists those files under
  `memoryFiles`. Asking is not a call to the model.

- It sends the request, and keeps the reply and the size of the first
  request the model was sent.

The request is for a reply to a customer. It says nothing about how
the shop likes its replies written. The cell calls nothing yet.

```{cell-insert}
:id: insert-ask
:path: {{ notebook }}
:tags: [ask]
:run: true
request = (
    "A customer has written to ask whether her order of The Ferry Almanac, "
    "which costs twelve and a half dollars, has come in yet. It has not. "
    "Write the reply, in three sentences or fewer."
)


async def ask(setting_sources):
    options = ClaudeAgentOptions(
        model="haiku",
        system_prompt=(
            "You are the assistant for Tidewater Books, a small bookshop. "
            "You write replies to customers for the staff to send."
        ),
        tools=[],
        setting_sources=setting_sources,
        strict_mcp_config=True,
        thinking={"type": "disabled"},
        max_turns=3,
    )
    run = {"first_request": None}
    async with ClaudeSDKClient(options=options) as client:
        context = await client.get_context_usage()
        run["files"] = context["memoryFiles"]
        run["categories"] = {entry["name"]: entry["tokens"] for entry in context["categories"]}
        await client.query(request)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage) and run["first_request"] is None:
                usage = message.usage
                run["first_request"] = (
                    usage["input_tokens"]
                    + usage["cache_creation_input_tokens"]
                    + usage["cache_read_input_tokens"]
                )
            elif isinstance(message, ResultMessage):
                run["result"] = message
    return run


def show(run):
    here = Path.cwd().resolve()
    print("instruction files the session was given:")
    for entry in run["files"]:
        path = Path(entry["path"]).resolve()
        where = path.relative_to(here) if path.is_relative_to(here) else path
        print(f"  {entry['type']:<8} {entry['tokens']:>5} tokens  {where}")
    if not run["files"]:
        print("  none")
    print()
    print(run["result"].result)


def project_files(run):
    return [entry for entry in run["files"] if entry["type"] == "Project"]


def given_house_rules(run):
    rules = (Path.cwd() / "CLAUDE.md").resolve()
    return any(Path(entry["path"]).resolve() == rules for entry in project_files(run))


print("ready to ask")
```

```{verify}
:id: ask-defined
:label: The function that runs the agent is defined
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed ask
callable(ask) and Path("CLAUDE.md").exists()
```

## The run every workshop has made so far

`setting_sources=[]` tells the SDK to load nothing from the file
system: no instruction files, no settings, nothing but what the
options say.

```{cell-insert}
:id: insert-plain
:path: {{ notebook }}
:tags: [plain]
:run: true
plain = await ask([])

show(plain)
```

No file of type `Project` is listed, and the reply was written without
the house rules. Read it against {open}`CLAUDE.md`. It is a reasonable
reply from an assistant that was told nothing about how this shop
signs off, what it may promise, or how it writes a price.

```{verify}
:id: rules-not-loaded
:label: The session was given no project instructions
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed plain
project_files(plain) == [] and plain["result"].subtype == "success"
```

```{hint}
:title: If a file of another type is listed
You may see a line of type `AutoMem`. Claude Code keeps notes of its
own about a project it has been used in, and a session started inside
that project is sent the list of them whatever `setting_sources` says.
It is not one of the files this workshop is about, and a later page
says how it is turned off.
```
