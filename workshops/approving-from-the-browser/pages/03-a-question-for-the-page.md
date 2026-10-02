---
title: A question for the page
requires: [verify:callback-in-place]
---

# A question for the page

The SDK has a place for someone to ask. The `can_use_tool` option
names an `async` function of yours, and the SDK calls it whenever a
tool call needs approval and nothing has given it. The function is
handed the tool's name and the input the model wants to pass, and
answers by returning one of two objects:

- `PermissionResultAllow()` lets the call run.

- `PermissionResultDeny(message=...)` stops it, and the message goes
  to the model as the result of its request.

The run waits while the function decides, for as long as it takes.
That is what makes this possible: the function can put the question to
a person and wait for the answer.

Here the function is a method of `Conversation`, because the question
has to reach the page of the conversation it came from. It is built in
a few small steps and then the method itself. The file is saved, and
the server restarted, by the last step on this page.

## What it needs

`uuid4` makes an id for each question, and the two result types are
what the function returns.

```{editor-replace}
:id: import-uuid4
:title: Import a way to make ids
:path: app.py
:match: from uuid import UUID
:save: false
from uuid import UUID, uuid4
```

```{editor-insert}
:id: import-results
:title: Import the two answers a callback can give
:path: app.py
:match: ResultMessage,
:save: false
    PermissionResultAllow,
    PermissionResultDeny,
```

## Somewhere to wait

A person takes seconds to answer, or minutes, or has gone to lunch.
The function needs something to wait on that another part of the
server can complete. Python's `asyncio` has exactly that, called a
future: an object that stands for a value that has not arrived yet.
One piece of code awaits it, and another sets its result.

The server keeps the futures it is waiting on in a dictionary, under
the id of the question each belongs to. It also sets how long a
question may wait.

```{editor-replace}
:id: add-questions
:title: Add a place for questions that are waiting
:path: app.py
:regex: true
:match: ^WORKSPACE = .*\nstarted = .*\nruns = .*\nconversations = .*$
:save: false
APPROVAL_SECONDS = 45  # how long the page has to answer a question from the agent
WORKSPACE = Path.cwd().resolve()  # the directory the server runs in, where the agent works
started = time.time()  # when this server process began
runs = []  # what the server has kept about each run since it started
conversations = {}  # conversation id -> the Conversation the server is holding
questions = {}  # question id -> the future its answer will arrive in
```

## A way to reach the page

A turn puts its events on the queue of whichever request is listening.
The callback needs that queue too, so each turn now keeps it on the
conversation, with a list of the answers the turn was given.

```{editor-replace}
:id: keep-listener
:title: Keep each turn's listener and answers
:path: app.py
:match: self.calls = []
:save: false
self.calls, self.answers, self.listener = [], [], listener
```

```{editor-replace}
:id: note-answers
:title: Keep the answers with the run
:path: app.py
:match: calls=self.calls))
:save: false
calls=self.calls, answers=self.answers))
```

## The callback

Now the method. Read it in three parts.

**Rules first.** Before it asks anyone, it applies the rules that need
no person. The shop lets the assistant write notices and nothing else,
so any tool but `Write` is refused outright, and so is any path
outside the `notices` directory. The path is made absolute before it
is compared, so that a path with `..` in it cannot slip past.

**The question.** It makes a future, files it under a new id, and puts
an `approval` event on the turn's queue, with the id, the file and
what the agent wants to write in it. The route sends that to the page
like any other event.

**The wait.** `asyncio.wait_for()` awaits the future for at most
`APPROVAL_SECONDS`. If nobody answers in time it gives up, and the
call is refused. Either way a second event, `answered`, tells the page
how it came out.

```{editor-insert}
:id: add-callback
:title: Add the method that puts the question to the page
:path: app.py
:match: answers=self.answers))
:position: after
:save: false


    async def approve(self, tool_name, tool_input, context):
        """Called by the SDK when a call needs approval: put the question to the page and wait."""
        if tool_name != "Write":
            return PermissionResultDeny(message="That tool has not been approved for the assistant.")
        target = Path(tool_input["file_path"]).resolve()
        if not target.is_relative_to(WORKSPACE / "notices"):
            return PermissionResultDeny(message="A notice may only be written in the notices directory.")
        number = uuid4().hex[:8]
        questions[number] = asyncio.get_running_loop().create_future()
        self.listener.put_nowait(
            {
                "type": "approval",
                "id": number,
                "file": str(target.relative_to(WORKSPACE)),
                "content": tool_input.get("content", ""),
            }
        )
        try:
            allowed = await asyncio.wait_for(questions[number], APPROVAL_SECONDS)
        except TimeoutError:
            allowed = None
        finally:
            del questions[number]
        answer = {True: "allowed", False: "refused", None: "timed out"}[allowed]
        self.answers.append(answer)
        self.listener.put_nowait({"type": "answered", "id": number, "answer": answer})
        if allowed:
            return PermissionResultAllow()
        return PermissionResultDeny(message="The member of staff did not approve this. Do not try again.")
```

Last, the client has to be told the method exists. Each conversation
makes its options from a copy of `OPTIONS`, and the copy now names its
own method as the callback.

```{editor-replace}
:id: use-callback
:title: Name the method as the conversation's callback
:path: app.py
:regex: true
:match: ^        options = replace\(OPTIONS, resume=key\).*$
        options = replace(OPTIONS, can_use_tool=self.approve)
        options = replace(options, resume=key) if self.resumed else replace(options, session_id=key)
```

```{verify}
:id: callback-in-place
:label: The server restarted with a callback that asks the page
:substrate: script
:script: checks/callback_in_place.py
:trigger: after:use-callback
```

```{hint}
:title: Why a time limit
The SDK will wait for the callback for as long as the callback takes,
so a question nobody answers would hold its turn open for good, and
with it the lock that keeps the conversation's turns in order. A limit
turns silence into an answer. Forty five seconds suits a workshop. An
application of your own would choose a limit to suit the people using
it, or let the session rest and pick the question up later, which the
SDK's documentation on approvals describes.
```
