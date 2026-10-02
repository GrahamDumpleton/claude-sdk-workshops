# A subagent at work

One question, answered by a main agent that hands the reading to a
subagent. Time runs down the page.

```mermaid
sequenceDiagram
    participant You as Your code
    participant Main as The main agent
    participant Sub as The subagent
    participant Files as The suppliers' files

    You->>Main: the question
    Main->>Sub: the Agent tool: a task, written out in words
    Note over Sub: starts with an empty conversation
    loop the subagent's own loop
        Sub->>Files: Glob, Read
        Files-->>Sub: the files, one after another
    end
    Sub-->>Main: a short report
    Note over Sub: its conversation is dropped,<br/>the files with it
    Main-->>You: the answer
```

- The main agent starts the subagent by asking for a tool, `Agent`,
  like any other. What it passes is a task in plain words. That text
  is all the subagent is told: it does not see the main conversation.

- The subagent runs an agent loop of its own, with its own
  instructions and its own tools. The files it reads join its
  conversation, not the main one.

- What comes back to the main agent is the result of the tool call:
  the subagent's last message, its report.

- The main conversation ends up holding the question, the task, the
  report and the answer.
