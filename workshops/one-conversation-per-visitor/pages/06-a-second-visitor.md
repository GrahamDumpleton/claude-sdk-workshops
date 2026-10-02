---
title: A second visitor
requires: [quiz:whose-conversation, verify:second-visitor]
---

# A second visitor

One server, and so far one visitor. A second needs a second browser,
or something that looks like one to the page.

The page keeps its id in the browser's storage, and a browser keeps
storage separately for each address a page comes from. To a browser,
`127.0.0.1` and `localhost` are two different addresses, although both
are names for this machine and both reach your server. So the chat
opened as `localhost` finds no id in its storage, and makes up a new
one: a second visitor, in a second tab beside the first.

```{quiz}
:id: whose-conversation
question: The second visitor's first message asks "What have I asked you so far?". What does the agent have to go on?
options:
  - { text: "The first visitor's two questions, because there is one server and one agent", explanation: "There is one server, and it holds a separate client, with a separate session, for each id." }
  - { text: "Nothing but that message, because a new id gets a new session", correct: true }
  - { text: "The first visitor's two questions, because both tabs are in one browser", explanation: "The server knows nothing about browsers. It goes by the id, and the two tabs send different ones." }
explanation: "A conversation is found by its id. An id the server has not seen gets a client of its own, connected to a session of its own."
```

```{url-open}
:id: open-second-visitor
:title: Open a second visitor and ask what they have asked
:url: http://localhost:{{ server_port }}/?new&ask=What+have+I+asked+you+so+far%3F
:pane: visitor
:label: Second visitor
:area: chat
```

Go between the two tabs, Chat and Second visitor. Each shows its own
conversation, and anything you type in one stays out of the other.

```{verify}
:id: second-visitor
:label: The second visitor has a conversation of their own
:substrate: script
:script: checks/second_visitor.py
:timeout: 150s
:trigger: after:open-second-visitor
```

## What each one costs

```{file-open}
:id: open-diagram
:title: Open a diagram of what is kept where
:path: diagrams/what-is-kept-where.md
:factory: Markdown Preview
:area: code
```

Each conversation the server holds is a `ClaudeSDKClient`, and behind
each client is a copy of Claude Code, running as a process of its own
and waiting for the next message. That is what makes a second message
quick: nothing has to be started. It is also the cost. A process that
waits still takes memory, and a server with a thousand visitors would
be holding a thousand of them, most belonging to people who have gone
home.

A real application closes a conversation that has been quiet for a
while, and connects a client again if its visitor comes back. This
one does not, to keep it short. The next page shows why closing one
loses nothing.
