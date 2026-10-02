---
title: Clean up
requires: [verify:sessions-deleted]
---

# Clean up

A transcript holds everything that was said in a session, and it stays
on disk until something removes it. A program that keeps conversations
has to decide how long to keep them, the same as any other record
about a person.

`delete_session()` removes one transcript. The cell deletes the two
sessions this workshop made on purpose, the original and the fork,
then lists the directory's sessions again to see that they are gone.
It is written to be safe to run twice.

```{cell-insert}
:id: insert-deleted
:path: {{ notebook }}
:tags: [deleted]
:run: true
made = [first.session_id, forked.session_id]

for session_id in made:
    try:
        delete_session(session_id, directory=here)
        print("deleted       :", session_id)
    except FileNotFoundError:
        print("already gone  :", session_id)

remaining = {session.session_id for session in list_sessions(directory=here)}

still_kept = [session_id for session_id in made if session_id in remaining]

print("still kept    :", still_kept)
```

Both are gone, and neither can be resumed now: there is nothing left
to send the model.

The login check at the start of the workshop was a run too, and it
left a small transcript of its own, as every run of every workshop
has. They are a few lines each. `list_sessions(directory=here)` shows
what is there for this directory if you want to look.

```{verify}
:id: sessions-deleted
:label: The two sessions the workshop made are gone
:substrate: learner-kernel
:path: {{ notebook }}
:trigger: cell-executed deleted
if still_kept:
    print("These sessions are still on disk:", still_kept, "- run the cell again.")
still_kept == []
```
