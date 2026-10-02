# One approval

A turn in which the agent asks to write a file, and the person in the
chat says yes. Time runs down the page.

```mermaid
sequenceDiagram
    participant Page as The page
    participant Chat as The chat route
    participant Turn as The turn, and the SDK
    participant Answer as The approve route

    Page->>Chat: POST /chat with the message
    Chat->>Turn: start the turn
    Turn-->>Page: events: text, a Read, its result
    Note over Turn: the model asks for Write
    Turn->>Turn: the SDK calls the callback
    Note over Turn: the callback makes a future,<br/>files it under an id
    Turn-->>Page: event: approval, with the id
    Note over Turn: the callback waits on the future
    Note over Page: a card, with Allow and Refuse
    Page->>Answer: POST /approve with the id and yes
    Answer->>Turn: set the future's result
    Note over Turn: the callback returns Allow,<br/>and the SDK runs the tool
    Turn-->>Page: events: answered, the result, more text, done
```

- Two requests from the page are open at once. The first, to `/chat`,
  is the stream the reply is arriving on. The second, to `/approve`,
  is short: it carries the answer and ends.

- The future is what joins them. The callback awaits it inside the
  turn, and the approve route completes it from outside.

- While the callback waits, the turn waits. Nothing is sent to the
  model, and nothing is charged, until the answer comes or the time
  runs out.
