---
title: Read the stream in the page
requires: [verify:page-reads-stream, verify:streamed-to-page]
---

# Read the stream in the page

Now the other half. In {open}`page.html`, `send()` waits for the whole
response and reads it as JSON. It has to read the response as it
arrives.

## A reader for the events

The browser hands a script the body of a response in chunks, as the
bytes come in. A chunk can hold several events or stop in the middle
of one, so the function below keeps what it has not used yet in
`buffer`, takes whole lines out of it, and for each line that begins
`data:` hands back the JSON after it.

The star in `async function*` makes it a generator, like a Python
function that yields: the page can loop over the events as they come.

```{editor-insert}
:id: add-reader
:title: Add a reader for the stream
:path: page.html
:match: async function send(text) {
:save: false
// Read a streamed response as the events the server sent: one JSON object on each "data:" line.
async function* events(response) {
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";
  while (true) {
    const {value, done} = await reader.read();
    if (done) break;
    buffer += value;
    const lines = buffer.split("\n");
    buffer = lines.pop();
    for (const line of lines) {
      if (line.startsWith("data: ")) yield JSON.parse(line.slice(6));
    }
  }
}


```

## Show each piece

`send()` now loops over the events. For each `text` event it adds the
words to what has been written so far and puts that in the bubble, in
place of the three dots.

```{editor-replace}
:id: replace-send
:title: Add each piece to the reply as it arrives
:path: page.html
:regex: true
:match: ^async function send\(text\) \{[\s\S]*?^\}$
async function send(text) {
  add("user", text);
  const reply = add("assistant", "…");
  let written = "";
  const response = await post("/chat", {message: text});
  for await (const event of events(response)) {
    if (event.type === "text") {
      written += event.text;
      reply.textContent = written;
    }
  }
}
```

The server did not restart this time, and did not need to. It reads
`page.html` each time a browser asks for the page, so the next load
gets the new script.

```{verify}
:id: page-reads-stream
:label: The page reads the response as a stream
:substrate: contents
:trigger: after:replace-send
contains page.html for await (const event of events(response))
```

## Ask again

A different question this time, about the returns policy, and with a
paragraph for an answer. Watch the bubble.

```{url-open}
:id: ask-returns
:title: Ask for the returns policy to be explained
:url: http://127.0.0.1:{{ server_port }}/?ask=Read+shop%2Freturns-policy.md+and+explain+it+in+a+short+paragraph%2C+for+a+new+member+of+staff.
:pane: chat
:label: Chat
:area: chat
```

There is still a pause at the start, while the agent reads the file.
Then the reply grows as the model writes it.

```{verify}
:id: streamed-to-page
:label: The run was streamed, in more than one piece
:substrate: script
:script: checks/streamed_to_page.py
:timeout: 150s
:trigger: after:ask-returns
```

```{hint}
:title: If the reply ran two sentences together
A run is not always one reply. Where the model says something, asks
for a tool, and then answers, there are two pieces of writing, and
this page puts both in one bubble with nothing between them. The page
does not know yet that a tool was used in between. A later workshop,
**Show the agent at work**, tells it.
```
