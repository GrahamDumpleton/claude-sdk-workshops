---
title: A call that is refused
requires: [quiz:what-the-model-is-told, verify:change-refused]
---

# A call that is refused

The second job asks the agent to change one of the shop's own
documents, which the rules do not permit.

```{quiz}
:id: what-the-model-is-told
:title: What the model is told
question: "The callback returns `PermissionResultDeny(message=...)`. What happens next?"
options:
  - text: "The run ends at once with an error."
    explanation: "A refusal does not end the run. The model is told, and decides what to do about it."
  - text: "The call is dropped and the model is not told, so it thinks the file was changed."
    explanation: "The model always gets a result for a request it made. Here the result is the refusal."
  - text: "The message is sent to the model as the result of its request, and the run carries on."
    correct: true
  - text: "The SDK asks the callback again until it says yes."
    explanation: "The callback is asked once for each call. A new call by the model would be a new question."
explanation: "A refusal is a tool result. The model reads the message you wrote and goes on from there, which is why the message is worth writing well."
```

```{cell-insert}
:id: insert-second
:path: {{ notebook }}
:tags: [second]
:run: true
hours = Path("shop/opening-hours.md")
hours_before = hours.read_text()

second = await attempt("Change shop/opening-hours.md so that Saturday closes at 6:00pm.")

print()
print("calls denied     :", second["denied"])
print("the file changed :", hours.read_text() != hours_before)
```

The model asked to change the file, the callback refused, and the file
is as it was. Now read what the agent said at the end. It did not
report a failure it could not explain. It was sent your message as the
result of its request, and it passed the substance of it on: who
changes these files, and whom to ask.

A refusal with a reason turns a dead end into an answer. A person
clicking No in an application can be asked why, and what they type
goes in that message.

The refused call is also listed under `permission_denials` on the
result, as it was when nobody was there to ask at all.

```{verify}
:id: change-refused
:label: The callback refused the change and the file is as it was
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed second
if "refused" not in verdicts(second):
    print("The callback was not asked to change the file. Run the cell again.")
"refused" in verdicts(second) and hours.read_text() == hours_before and len(second["denied"]) >= 1
```
