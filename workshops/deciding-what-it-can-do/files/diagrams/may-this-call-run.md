# May this call run?

The questions the SDK asks about a tool, in order, with the option
that answers each. The first is asked once, when the session starts.
The rest are asked every time the model wants a tool used.

```mermaid
flowchart LR
    given{"In <b>tools</b>, and not in<br/><b>disallowed_tools</b>?"}
    given -- "no" --> unseen(["The model is not told of the tool.<br/>If it asks anyway, it is told<br/>there is no such tool"])
    given -- "yes" --> asks["The model asks<br/>for the tool"]
    asks --> needs{"Does the call<br/>need approval?"}
    needs -- "no: reading in the<br/>working directory" --> run(["The SDK<br/>runs it"])
    needs -- "yes: writing<br/>a file" --> mode{"Approved by<br/><b>permission_mode</b>?"}
    mode -- "yes" --> run
    mode -- "no" --> allow{"Tool in<br/><b>allowed_tools</b>?"}
    allow -- "yes" --> run
    allow -- "no" --> refused(["Refused, when nobody<br/>is there to ask.<br/>The model is told"])
```

- The first attempt went as far as the last question and was refused:
  the call needed approval, the mode did not give it, and no rule
  allowed it.

- The second attempt took the same path and was approved at the last
  question, by `allowed_tools`.

- A mode that approves edits answers one question sooner, and a tool
  on the deny list never gets past the first.

- The picture leaves out two things that later workshops add: a
  function of your own that is asked in place of the refusal, and
  hooks, which are code of yours that runs before any of this.
