---
title: Ask in the chat
requires: [verify:page-asks, verify:question-answered]
---

# Ask in the chat

The server now sends two events the page does not know. `send()` in
{open}`page.html` gains a branch for each.

- For `approval` it draws a card saying what the agent wants to write,
  with two buttons. Each button posts the question's id and its answer
  to `/approve`. The card goes above the waiting bubble, as tool lines
  do.

- For `answered` it takes the buttons off the card and says how it
  came out, which also covers the case where the time ran out with the
  buttons still showing.

```{editor-insert}
:id: add-approval-branches
:title: Draw the question, and its answer
:path: page.html
:match: } else if (event.type === "done") {
    } else if (event.type === "approval") {
      const card = aside("approval", `The assistant wants to write ${event.file}:\n\n${event.content}\n`);
      card.id = event.id;
      for (const [label, allow] of [["Allow", true], ["Refuse", false]]) {
        const button = document.createElement("button");
        button.textContent = label;
        button.onclick = () => post("/approve", {id: event.id, allow});
        card.append(button);
      }
    } else if (event.type === "answered") {
      const card = document.getElementById(event.id);
      card.querySelectorAll("button").forEach((button) => button.remove());
      card.append("\n" + event.answer);
```

```{verify}
:id: page-asks
:label: The page draws the question and sends the answer
:substrate: contents
:trigger: after:add-approval-branches
contains page.html post("/approve", {id: event.id, allow})
```

## Decide

Ask for another notice, about the author evening. When the card
appears in the chat, read what the agent wants to write, and press
**Allow** or **Refuse**. You have forty five seconds from the moment
it appears, after which the server answers no for you.

```{url-open}
:id: ask-evening
:title: Ask for a notice about the author evening
:url: http://127.0.0.1:{{ server_port }}/?new&ask=Read+shop%2Fevents.md+and+write+a+short+notice+about+the+author+evening%2C+to+the+file+notices%2Fauthor-evening.md.
:pane: chat
:label: Chat
:area: chat
```

If you allowed it, the `Write` line turned solid and the notice is in
`notices/author-evening.md`. If you refused, or waited, the line
turned red and the agent said the notice was not written. The check
waits for the run to end, so it may take up to a minute, and its
message says which answer the run was given.

```{verify}
:id: question-answered
:label: The question was put to the page and answered
:substrate: script
:script: checks/question_answered.py
:timeout: 240s
:trigger: after:ask-evening
```

Follow what happened in the middle of that turn. The model asked for
`Write`. The SDK called your method, which sent an event down the
stream that was already open for the reply, and then waited. Your
click made a second request, to a different route, which completed the
future. The method returned, the SDK ran the tool or refused it, and
the turn carried on from where it had stopped.

Try it again from the box if you like, and give the other answer. Ask
for a notice somewhere it may not go, such as a file in the `shop`
directory, and no card appears: the rule at the top of the method
refuses it without asking.
