# What is kept where

Two visitors, each with a conversation, and the four places that hold
a part of it.

```mermaid
flowchart LR
    subgraph browser["Each browser"]
        id1["the id of its conversation,<br/>in localStorage"]
    end

    subgraph server["The server's memory"]
        dict["conversations:<br/>id to Conversation"]
        c1["Conversation<br/>a connected client"]
        c2["Conversation<br/>a connected client"]
        dict --> c1
        dict --> c2
    end

    subgraph processes["Processes on the server's machine"]
        p1["Claude Code,<br/>one session open"]
        p2["Claude Code,<br/>one session open"]
    end

    subgraph disk["The disk"]
        t1["transcript<br/>of session 1"]
        t2["transcript<br/>of session 2"]
    end

    id1 -- "sent with every message" --> dict
    c1 --> p1
    c2 --> p2
    p1 -- "writes as it goes" --> t1
    p2 -- "writes as it goes" --> t2
```

- The browser keeps one small thing: the id. It never holds the
  conversation, only what it has drawn of it.

- The server's memory holds what is live. A `Conversation` is a
  client and a lock, and the client is a line to a process.

- Each process is a copy of Claude Code with one session open. It is
  what a quick second message costs: a process waiting.

- The transcript on disk is the conversation itself. The route for
  what was said reads it, and a client connected with `resume` starts
  from it. Lose everything to its left and the conversation is still
  there.
