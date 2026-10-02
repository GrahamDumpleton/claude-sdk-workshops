---
title: A server with no agent
requires: [verify:server-up]
---

# A server with no agent

Start with the web part alone, which has nothing to do with agents
yet. {open}`app.py` is the whole server, and it is short. Read it from
the top.

- `app = FastAPI(...)` makes the application. The functions below it
  are attached to it with a line beginning `@app`, which says which
  requests the function answers. A function attached that way is
  called a route.

- `@app.get("/")` answers a browser that asks for the page, by sending
  it the file {open}`page.html`.

- `@app.post("/chat")` answers a message from the page. For now it
  sends back what it was sent, with "You said:" in front.

- `@app.get("/status")` reports when the server started and the list
  `runs`, which is empty. It is there for you, and for the checks on
  these pages, to see what the server has done.

One thing in the file does its work without showing it. The class
`Ask` says what a message from the page must look like: a piece of
text called `message`. Because `chat` takes an `Ask`, FastAPI reads
the request, checks that it has that shape and turns it into an object
before your function runs. A request of the wrong shape is refused and
your function is never called.

## Start it

The command runs the server with `uvicorn`, the program that listens
on a port and passes each request to the application. `app:app` means
the object `app` in the file `app.py`. With `--reload`, uvicorn
restarts the server whenever that file changes, which later steps rely
on.

```{execute}
:id: start-server
:title: Start the server
:session: server
:wait: 4s
{{ app_python | shell }} -m uvicorn app:app --port {{ server_port }} --reload
```

The terminal shows the address the server is listening on, and from
now on a line for each request it answers.

```{verify}
:id: server-up
:label: The server is answering
:substrate: script
:script: checks/server_up.py
:trigger: after:start-server
```

```{hint}
:title: If the port is already in use
The server prints "address already in use" when another program has
port {{ server_port }}. The gear button at the top of this panel opens
the Variables dialog, where `server_port` can be changed. The commands
and links on these pages then use the new number. Run the step again
afterwards.
```

## Open the page

The step below opens the application beside its source, as a browser
would show it.

```{url-open}
:id: open-chat
:title: Open the chat
:url: http://127.0.0.1:{{ server_port }}/
:pane: chat
:label: Chat
:area: chat
```

Type something in the box and press Send, and the server's canned
reply comes back. The terminal shows a `GET /` for the page and a
`POST /chat` for your message. The requests for `/status` and
`/openapi.json` there are the checks on these pages, looking at what
the server has done.

## What the page does

{open}`page.html` is as small as the server. Its script does three
things.

- `send()` shows what was typed, sends it to `/chat` as JSON with
  `fetch`, the browser's way of making a request from a script, and
  shows the reply when it arrives. Until then it shows three dots.

- The form calls `send()` when Send is pressed.

- The last lines look in the page's own address for a question. An
  address ending in `/?ask=Hello` asks "Hello" as the page loads. Many
  chat applications take a question that way, so that a link can ask
  it. The steps of these workshops use it, so that a button here can
  put a question to the chat.

```{url-open}
:id: ask-hello
:title: Ask "Is anyone there?" through the address
:url: http://127.0.0.1:{{ server_port }}/?ask=Is+anyone+there%3F
:pane: chat
:label: Chat
:area: chat
```

The page loaded again and asked at once. Nothing has thought about the
question: the reply is the route's one line of Python.
