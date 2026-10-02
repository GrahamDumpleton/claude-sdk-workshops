# The pieces of an agent

Three of the pieces are on your machine. The model is not: it is a
service, reached over the network with your Claude login. A solid
arrow is a request, and a dashed arrow is what comes back.

```mermaid
flowchart LR
    subgraph machine["Your machine"]
        code["<b>Your code</b><br/>calls query()"]
        sdk["<b>Claude Agent SDK</b><br/>runs the loop<br/>and the tools"]
        files[("<b>Files</b><br/>in the working<br/>directory")]
    end
    subgraph service["Anthropic's service"]
        model["<b>The model</b><br/>text in, text out"]
    end

    code -- "prompt and options" --> sdk
    sdk -. "messages, as the run goes on" .-> code
    sdk -- "the conversation so far,<br/>and the tools that exist" --> model
    model -. "an answer, or a request<br/>to use a tool" .-> sdk
    sdk -- "carries out a request" --> files
```

- **Your code** starts a run with a prompt and options, and reads the
  messages that come back.

- **The Claude Agent SDK** is the program around the model. It sends
  the model the conversation, carries out any tool the model asks for,
  sends back what the tool found, and repeats until the model answers.
  Underneath, it runs Claude Code as a separate process to do this.

- **The model** only ever sees text and only ever produces text. It
  never touches your files. It can ask, and the SDK decides whether to
  do what it asks.

- **Files** are reached by tools, and only by the tools the options
  give the agent.
