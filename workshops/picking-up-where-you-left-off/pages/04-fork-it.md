---
title: Fork it
requires: [quiz:what-a-fork-leaves, verify:session-forked]
---

# Fork it

Resuming adds to a session. Sometimes you want to start from where a
conversation has got to without adding to it: to try a different
instruction, or to let two people carry on from the same point.
`fork_session=True`, set beside `resume`, does that.

```{quiz}
:id: what-a-fork-leaves
:title: What a fork leaves behind
question: "A run resumes the session with `fork_session=True` and tells the agent something new. What happens to the original session?"
options:
  - text: "It gains the new messages, like any resumed session."
    explanation: "That is what resuming without the option does. Forking exists so that it does not happen."
  - text: "It is left as it was. The new messages go into a new session that starts as a copy."
    correct: true
  - text: "It is deleted, and the fork replaces it."
    explanation: "Nothing is removed. Both sessions exist afterwards, each with its own id."
  - text: "It is locked, and cannot be resumed again."
    explanation: "The original is untouched and can be resumed or forked again as often as you like."
explanation: "A fork is a new session that begins with everything the original held. From there the two go their own ways."
```

The cell counts the messages in the original, then forks it and tells
the agent the stock code has changed, then counts again.

```{cell-insert}
:id: insert-forked
:path: {{ notebook }}
:tags: [forked]
:run: true
before_fork = len(get_session_messages(first.session_id, directory=here))

fork_options = replace(options, resume=first.session_id, fork_session=True)

change = "The harbour atlas has been given a new stock code, TW-9000-Z. What is its code now?"

async for message in query(prompt=change, options=fork_options):
    if isinstance(message, ResultMessage):
        forked = message

after_fork = len(get_session_messages(first.session_id, directory=here))

print(forked.result)
print("forked session   :", forked.session_id)
print("original session :", first.session_id)
print("messages in the original, before and after:", before_fork, after_fork)
```

The forked run has a session id of its own. It knew the conversation
so far, since it began as a copy of it, and it now holds the new code.
The original has the same number of messages as before: nothing the
fork said was added to it, and resuming the original would find the
old code still standing.

```{verify}
:id: session-forked
:label: The fork is a new session and the original is unchanged
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed forked
if forked.session_id == first.session_id:
    print("The run carried on the original session. Check that the cell passes fork_session=True, and run it again.")
elif before_fork != after_fork:
    print("The original session changed. Run the cell again.")
forked.session_id != first.session_id and before_fork == after_fork and "TW-9000-Z" in (forked.result or "")
```

## The two as a picture

The step below opens a picture of the three runs you have made and
the two sessions they left.

```{file-open}
:id: open-sessions
:title: Open the picture of the sessions
:path: diagrams/resume-and-fork.md
:factory: Markdown Preview
```
