# A streamed reply

One message and its reply, now that the reply is streamed. Time runs
down the page.

```mermaid
sequenceDiagram
    participant Page as The page, in the browser
    participant Server as The server, app.py
    participant Agent as The agent, run by the SDK
    participant Model as The model

    Page->>Server: POST /chat with the message
    Server->>Agent: query(prompt=the message)
    Note over Page,Server: the response opens, and stays open
    loop while the model writes
        Model-->>Agent: the next few words
        Agent-->>Server: a StreamEvent
        Server-->>Page: data: {"type": "text", ...}
    end
    Agent-->>Server: the ResultMessage
    Server-->>Page: data: {"type": "done", ...}
    Note over Page,Server: the response ends
```

- There is still one request and one response. What changed is that
  the response is sent a piece at a time, and takes as long as the
  run.

- Each `StreamEvent` that carries text becomes one `data:` line. The
  page adds its words to the bubble and waits for the next.

- When the agent uses a tool there is a gap in the middle of the
  loop: nothing is being written, so nothing is sent.

- The `ResultMessage` still ends the run. The route turns it into a
  `done` event, its function finishes, and FastAPI closes the
  response.
