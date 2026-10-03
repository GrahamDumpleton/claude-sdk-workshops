---
title: Draw the work
requires: [verify:page-draws-tools, verify:work-shown]
---

# Draw the work

The page has two things to do with the new events: draw a line when a
tool is asked for, and mark that line when its result arrives.

There is one thing to get right about where the line goes. While a
run is going on, the last thing in the chat is the bubble that is
waiting for the model's words, showing three dots. A tool line belongs
above it, so that the answer, when it comes, is written below the work.

`aside()`, inside `send()`, puts a line there. The `tool` branch
clears the bubble as before, then calls it and gives the new line the
request's id. The `tool_result` branch finds the line by that id,
makes its border solid or red, and adds what came back. When the run
is done, a waiting bubble that never got any words is taken away.

```{editor-replace}
:id: replace-send
:title: Draw tool requests and results in the page
:path: page.html
:regex: true
:match: ^async function send\(text\) \{[\s\S]*?^\}$
async function send(text) {
  add("user", text);
  const reply = add("assistant", "…");
  let written = "";

  // Put a line that is not the model's words above the bubble being waited for.
  function aside(kind, text) {
    const line = add(kind, text);
    reply.before(line);
    return line;
  }

  const response = await post("/chat", {conversation, message: text});
  for await (const event of events(response)) {
    if (event.type === "text") {
      written += event.text;
      reply.textContent = written;
    } else if (event.type === "tool") {
      // What the model wrote before asking for a tool was not the answer.
      written = "";
      reply.textContent = "…";
      aside("tool", event.name + " " + JSON.stringify(event.input).slice(0, 160)).id = event.id;
    } else if (event.type === "tool_result") {
      const line = document.getElementById(event.id);
      line.classList.add(event.error ? "failed" : "worked");
      line.textContent += event.error ? "\nfailed" : `\nreturned ${event.size} characters`;
    } else if (event.type === "done") {
      if (!written) reply.remove();
    }
  }
}
```

```{verify}
:id: page-draws-tools
:label: The page draws tool requests and results
:substrate: contents
:trigger: after:replace-send
contains page.html event.type === "tool_result"
```

## Ask again

A new conversation, and a question of the same kind as before: whether
the shop is open when the book club meets, and when the author evening
starts.

```{url-open}
:id: ask-club
:title: Ask whether the shop is open for the book club and the author evening
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Is+the+shop+open+when+the+Harbour+book+club+meets%2C+and+when+the+author+evening+starts%3F
:pane: chat
:label: Chat
:area: chat
```

This time the wait has something in it. Each line with a dashed border
is a tool the model has asked for, with what it passed. The border
turns solid when the result is back, and the line says how much came
back. Then the answer is written below.

```{verify}
:id: work-shown
:label: The run called tools, and the page was told of each
:substrate: script
:script: checks/work_shown.py
:timeout: 150s
:trigger: after:ask-club
```
