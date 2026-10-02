---
title: What you know now
requires: [quiz:what-to-store]
---

# What you know now

A session is a conversation kept on disk, under an id.

- The SDK writes every session to a transcript as it runs.
  `list_sessions()` finds the sessions for a directory, and
  `get_session_messages()` reads one back.

- `resume=<id>` starts a run that carries the session on. The result
  has the same session id.

- `fork_session=True`, beside `resume`, starts a new session from a
  copy and leaves the original alone.

- `delete_session()` removes a transcript.

What this is for:

- **A chat that survives a restart.** The server keeps a session id
  for each visitor, and any later request resumes it.

- **A job that failed part way.** Resume the session, and the agent
  has everything it had read and done before it stopped.

- **Two ways forward.** Fork at the point of decision and try both.

```{quiz}
:id: what-to-store
:title: What to store
question: "Your application lets a customer come back tomorrow and carry on a conversation with the agent. What does the application have to keep overnight?"
options:
  - text: "The session id, stored against the customer."
    correct: true
  - text: "The connected client, kept running until the customer returns."
    explanation: "That would mean a running process for every customer who might come back, and all of them lost when the server restarts."
  - text: "Nothing. The model remembers the customer."
    explanation: "The model keeps nothing between requests. Whatever it knows of a conversation, it was sent."
  - text: "A summary of the conversation, to paste into the next prompt."
    explanation: "That could be made to work, and it throws away what the SDK already keeps. The transcript has the whole conversation, and the id is all that is needed to load it."
explanation: "The SDK keeps the conversation. The application keeps the id, and passes it as `resume`."
```

## Where this goes next

In every run so far, the reply has arrived whole: nothing, then all of
it. For a one line answer that is fine. For a long one it is a long
wait in front of an empty screen. The next workshop shows the reply
arriving as the model writes it.

**Stream the reply as it is written** is next.

Press Finish below to move on.
