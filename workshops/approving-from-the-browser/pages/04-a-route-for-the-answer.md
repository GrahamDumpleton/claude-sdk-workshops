---
title: A route for the answer
requires: [verify:approve-in-place]
---

# A route for the answer

The callback is waiting on a future. Something has to complete it, and
that is an ordinary route: the page will send the id of the question
and a yes or a no, and the route will find the future and set its
result.

```{file-open}
:id: open-diagram
:title: Open a diagram of one approval
:path: diagrams/one-approval.md
:factory: Markdown Preview
:area: code
```

First what such a request must look like.

```{editor-insert}
:id: add-answer
:title: Say what an answer from the page looks like
:path: app.py
:match: def summary(result, **more):
:save: false
class Answer(BaseModel):
    id: str
    allow: bool



```

Then the route. It is declared with `async def`, and here that is not
a matter of taste. A future belongs to the server's event loop and
must be completed from it. A route declared with a plain `def` runs on
another thread, from which setting the result would not be safe.

An id that is not waiting, because the time ran out or the question
was already answered, is passed over.

```{editor-insert}
:id: add-approve
:title: Add the route that completes the future
:path: app.py
:match: @app.get("/history/{conversation}")
@app.post("/approve")
async def approve(answer: Answer):
    waiting = answer.id in questions
    if waiting:
        questions[answer.id].set_result(answer.allow)
    return {"answered": waiting}



```

That saved the file, and the server restarted.

```{verify}
:id: approve-in-place
:label: The server restarted with a route for the answer
:substrate: script
:script: checks/approve_in_place.py
:trigger: after:add-approve
```

Notice what the route does not check: who is answering. Anyone who can
reach the server and knows the id of a question can approve it. The id
is random and short lived, which is enough on your own machine. An
application for other people would check that the answer comes from
the person whose conversation it is.
