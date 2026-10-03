---
title: Choose the model
requires: [verify:model-in-place, verify:page-chooses, verify:model-used]
---

# Choose the model

Every turn so far has run on Haiku, the smallest model, which is
quick and cheap and good enough for looking things up. Some questions
deserve a larger one. Which is right is a judgement about the
question, and the person asking is well placed to make it.

A connected client can change model in the middle of a conversation.
`await client.set_model(name)` takes effect from the next turn, and
the conversation carries on: the new model is sent everything said
so far.

## A route that changes it

The server names the models it will accept. A page should not be able
to choose any model at all, since the choice is a choice about cost.

```{editor-insert}
:id: add-models
:title: Name the models the page may choose
:path: app.py
:match: APPROVAL_SECONDS = 45
:save: false
MODELS = ["haiku", "sonnet"]  # the models the page may choose between
```

```{editor-insert}
:id: add-choice
:title: Say what a choice of model looks like
:path: app.py
:match: def summary(result, **more):
:save: false
class Choice(BaseModel):
    conversation: UUID
    model: str



```

The route finds the conversation and tells its client. A model that
is not on the list is passed over.

```{editor-insert}
:id: add-model-route
:title: Add the route that changes the model
:path: app.py
:match: @app.get("/history/{conversation}")
:save: false
@app.post("/model")
async def model(choice: Choice):
    conversation = await conversation_for(str(choice.conversation))
    if choice.model in MODELS:
        await conversation.client.set_model(choice.model)
    return {"model": choice.model if choice.model in MODELS else None}



```

## Which model answered

The `init` message that opens every turn names the model, and the
server already sends it to the page with the list of tools. Two small
changes keep it with the record of each run.

```{editor-insert}
:id: note-model
:title: Remember the model each turn ran on
:path: app.py
:match: elif event["type"] == "done":
:save: false
        elif event["type"] == "tools":
            self.model = event["model"]
```

```{editor-insert}
:id: keep-model
:title: Keep the model with the run
:path: app.py
:match: sent=event["sent"],
:save: false
                    model=self.model,
```

One more thing follows from changing model. The SDK records the
change in the conversation's transcript, as a command wrapped in
angle brackets, and the route that returns what was said would show
it as though somebody had typed it. It leaves out text that begins
that way.

```{editor-replace}
:id: skip-commands
:title: Leave the SDK's own notes out of what was said
:path: app.py
:match: if block["type"] == "text":
if block["type"] == "text" and not block["text"].startswith("<"):
```

```{verify}
:id: model-in-place
:label: The server restarted with a route that changes the model
:substrate: script
:script: checks/model_in_place.py
:trigger: after:skip-commands
```

## A menu in the page

The page gets a menu in its heading, and tells the server when the
choice changes.

```{editor-insert}
:id: add-menu
:title: Add a menu of models to the heading
:path: page.html
:match: </header>
  <select id="model"><option>haiku</option><option>sonnet</option></select>
```

```{editor-insert}
:id: name-menu
:title: Give the script a name for the menu
:path: page.html
:match: const params = new URLSearchParams(location.search);
const model = document.getElementById("model");
```

```{editor-insert}
:id: wire-menu
:title: Tell the server when the choice changes
:path: page.html
:regex: true
:match: ^\};$
:position: after
model.onchange = () => post("/model", {conversation, model: model.value});
```

And, as with a question, the address can make the choice, so that a
step on this page can.

```{editor-insert}
:id: model-from-address
:title: Take a choice of model from the address
:path: page.html
:match: // A question in the address, as in /?ask=When+do+we+open, is asked as the
  // /?model=<name> picks the model before anything is asked.
  if (params.has("model")) {
    model.value = params.get("model");
    await post("/model", {conversation, model: model.value});
  }


```

```{verify}
:id: page-chooses
:label: The page has a menu that chooses the model
:substrate: contents
:trigger: after:model-from-address
contains page.html post("/model", {conversation, model: model.value})
```

## Ask the larger model

The step below chooses Sonnet and asks a question with some working
out in it, in the same conversation as before. This is the one run of
these workshops that is not on the smallest model.

```{url-open}
:id: ask-sonnet
:title: Choose Sonnet and ask who has spent the most
:url: http://127.0.0.1:{{ server_port }}/?model=sonnet&ask=Which+customer+spent+the+most+with+us+in+September%2C+and+how+much%3F
:pane: chat
:label: Chat
:area: chat
```

The line under the heading names the model that answered, and it has
changed. The conversation did not start again: the earlier questions
are still above, and the new model was sent them.

```{verify}
:id: model-used
:label: A turn ran on the model the page chose
:substrate: script
:script: checks/model_used.py
:timeout: 150s
:trigger: after:ask-sonnet
```

The choice lasts as long as the server holds the conversation. A
conversation picked up after a restart begins on the model in the
options again, since nothing here records the choice. Keeping it is
one more thing an application of your own would store beside each
conversation.
