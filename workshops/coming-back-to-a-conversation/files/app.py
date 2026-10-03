"""The Tidewater Books chat: the server behind the web page."""

import asyncio
import time
from contextlib import asynccontextmanager
from dataclasses import replace
from pathlib import Path
from uuid import UUID, uuid4

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    PermissionResultAllow,
    PermissionResultDeny,
    ResultMessage,
    StreamEvent,
    SystemMessage,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    get_session_info,
    get_session_messages,
)
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.sse import EventSourceResponse
from pydantic import BaseModel

from shop_tools import shop_server

OPTIONS = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "The shop's documents are in the shop directory. Answer from them, briefly, "
        "in plain text with no Markdown. Give the answer only: do not say what you "
        "are about to do. When you are asked for a notice, write it as a file in "
        "the notices directory."
    ),
    tools=["Read", "Glob", "Grep", "Write", "Skill"],
    permission_mode="default",
    mcp_servers={"shop": shop_server},
    allowed_tools=["mcp__shop__check_stock", "mcp__shop__query_orders"],
    setting_sources=["project"],
    skills=["refund-reply"],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    include_partial_messages=True,
    max_turns=10,
)

APPROVAL_SECONDS = 45  # how long the page has to answer a question from the agent
WORKSPACE = Path.cwd().resolve()  # the directory the server runs in, where the agent works
started = time.time()  # when this server process began
runs = []  # what the server has kept about each run since it started
conversations = {}  # conversation id -> the Conversation the server is holding
questions = {}  # question id -> the future its answer will arrive in


@asynccontextmanager
async def lifespan(app):
    """Run the server, and when it stops, close every conversation it holds."""
    yield
    for conversation in conversations.values():
        await conversation.client.disconnect()
    print(f"closed {len(conversations)} conversations")


app = FastAPI(title="Tidewater Books chat", lifespan=lifespan)


class Ask(BaseModel):
    conversation: UUID
    message: str


class Which(BaseModel):
    conversation: UUID


class Answer(BaseModel):
    id: str
    allow: bool


def summary(result, **more):
    """What the server keeps about one run, with anything more it is handed."""
    return {
        "session": result.session_id,
        "ended": result.subtype,
        "turns": result.num_turns,
        "seconds": round(result.duration_ms / 1000, 1),
        "reply": result.result,
        **more,
    }


def events_for(message):
    """Turn one message of a run into the events the page is sent."""
    if isinstance(message, StreamEvent):
        delta = message.event.get("delta", {})
        if delta.get("type") == "text_delta":
            yield {"type": "text", "text": delta["text"]}
    elif isinstance(message, SystemMessage) and message.subtype == "init":
        yield {"type": "tools", "names": message.data["tools"], "model": message.data["model"]}
    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                yield {"type": "tool", "id": block.id, "name": block.name, "input": block.input}
    elif isinstance(message, UserMessage) and isinstance(message.content, list):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                yield {
                    "type": "tool_result",
                    "id": block.tool_use_id,
                    "error": bool(block.is_error),
                    "size": len(str(block.content)),
                }
    elif isinstance(message, ResultMessage):
        yield {"type": "done", "ended": message.subtype, "seconds": round(message.duration_ms / 1000, 1)}


class Conversation:
    """A conversation the server is holding: a connected client, and its turns kept in order."""

    def __init__(self, key):
        self.resumed = get_session_info(key, directory=str(WORKSPACE)) is not None
        options = replace(OPTIONS, can_use_tool=self.approve)
        options = replace(options, resume=key) if self.resumed else replace(options, session_id=key)
        self.client = ClaudeSDKClient(options=options)
        self.turns = asyncio.Lock()

    async def turn(self, text, listener):
        """Run one turn, putting each event of it on the listener's queue, and None when it is over."""
        async with self.turns:
            self.calls, self.answers, self.listener = [], [], listener
            try:
                await self.client.query(text)
                async for message in self.client.receive_response():
                    for event in events_for(message):
                        self.note(event, message)
                        listener.put_nowait(event)
            finally:
                listener.put_nowait(None)

    def note(self, event, message):
        """Keep what the server wants to remember of one event of a turn."""
        if event["type"] == "tool":
            self.calls.append(event["name"])
        elif event["type"] == "done":
            runs.append(summary(message, resumed=self.resumed, calls=self.calls, answers=self.answers))

    async def approve(self, tool_name, tool_input, context):
        """Called by the SDK when a call needs approval: put the question to the page and wait."""
        if tool_name != "Write":
            return PermissionResultDeny(message="That tool has not been approved for the assistant.")
        target = Path(tool_input["file_path"]).resolve()
        if not target.is_relative_to(WORKSPACE / "notices"):
            return PermissionResultDeny(message="A notice may only be written in the notices directory.")
        number = uuid4().hex[:8]
        questions[number] = asyncio.get_running_loop().create_future()
        self.listener.put_nowait(
            {
                "type": "approval",
                "id": number,
                "file": str(target.relative_to(WORKSPACE)),
                "content": tool_input.get("content", ""),
            }
        )
        try:
            allowed = await asyncio.wait_for(questions[number], APPROVAL_SECONDS)
        except TimeoutError:
            allowed = None
        finally:
            del questions[number]
        answer = {True: "allowed", False: "refused", None: "timed out"}[allowed]
        self.answers.append(answer)
        self.listener.put_nowait({"type": "answered", "id": number, "answer": answer})
        if allowed:
            return PermissionResultAllow()
        return PermissionResultDeny(message="The member of staff did not approve this. Do not try again.")


async def conversation_for(key):
    """Return the conversation with this id, connecting a client for it if the server holds none."""
    if key not in conversations:
        conversations[key] = Conversation(key)
        await conversations[key].client.connect()
    return conversations[key]


@app.get("/", response_class=HTMLResponse)
def page():
    return Path("page.html").read_text()


@app.post("/chat", response_class=EventSourceResponse)
async def chat(ask: Ask):
    conversation = await conversation_for(str(ask.conversation))
    listener = asyncio.Queue()
    conversation.running = asyncio.create_task(conversation.turn(ask.message, listener))
    while (event := await listener.get()) is not None:
        yield event


@app.post("/approve")
async def approve(answer: Answer):
    waiting = answer.id in questions
    if waiting:
        questions[answer.id].set_result(answer.allow)
    return {"answered": waiting}


@app.post("/stop")
async def stop(which: Which):
    conversation = conversations.get(str(which.conversation))
    if conversation:
        await conversation.client.interrupt()
    return {"stopped": conversation is not None}


@app.get("/history/{conversation}")
def history(conversation: UUID):
    said = []
    for message in get_session_messages(str(conversation), directory=str(WORKSPACE)):
        content = message.message["content"]
        blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content
        for block in blocks:
            if block["type"] == "text":
                said.append({"role": message.type, "text": block["text"]})
            elif block["type"] == "tool_use" and said and said[-1]["role"] == "assistant":
                said.pop()  # what the model wrote before asking for a tool was not the answer
    return said


@app.get("/status")
def status():
    return {"started": started, "conversations": len(conversations), "runs": runs}
