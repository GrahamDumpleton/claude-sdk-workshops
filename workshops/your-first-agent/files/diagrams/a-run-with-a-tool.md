# A run with one tool

The run you just made, step by step. Time runs down the page. A solid
arrow is a request, and a dashed arrow is what comes back.

```mermaid
sequenceDiagram
    participant C as Your code
    participant S as Claude Agent SDK
    participant M as The model
    participant F as shop/opening-hours.md

    C->>S: query(prompt, options)
    S-->>C: SystemMessage (init)

    Note over S,M: Turn 1
    S->>M: the question, and that a Read tool exists
    M-->>S: a request to use Read on the file
    S-->>C: AssistantMessage holding a ToolUseBlock
    S->>F: read the file
    F-->>S: its contents
    S-->>C: UserMessage holding a ToolResultBlock

    Note over S,M: Turn 2
    S->>M: everything so far, with the contents of the file
    M-->>S: the answer
    S-->>C: AssistantMessage holding a TextBlock
    S-->>C: ResultMessage
```

- The model is asked twice. The first time it replies with a request,
  not an answer. The second time it has the file's contents in front of
  it and can answer.

- The model never reads the file. The SDK does, on your machine, and
  passes the contents on as text.

- The second request carries everything so far: the question, the
  model's own request, and the tool's result. The model keeps nothing
  between the two, so the SDK sends it all again.

- Your code sees each step as a message, in the order shown down the
  left.
