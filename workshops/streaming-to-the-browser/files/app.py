"""The Tidewater Books chat: the server behind the web page."""

import time
from pathlib import Path

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ResultMessage,
    query,
)
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

OPTIONS = ClaudeAgentOptions(
    model="haiku",
    system_prompt=(
        "You are the assistant for the staff of Tidewater Books, a small bookshop. "
        "The shop's documents are in the shop directory. Answer from them, briefly, "
        "in plain text with no Markdown. Give the answer only: do not say what you "
        "are about to do."
    ),
    tools=["Read", "Glob", "Grep"],
    setting_sources=[],
    strict_mcp_config=True,
    thinking={"type": "disabled"},
    max_turns=10,
)

started = time.time()  # when this server process began
runs = []  # what the server has kept about each run since it started

app = FastAPI(title="Tidewater Books chat")


class Ask(BaseModel):
    message: str


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


@app.get("/", response_class=HTMLResponse)
def page():
    return Path("page.html").read_text()


@app.post("/chat")
async def chat(ask: Ask):
    async for message in query(prompt=ask.message, options=OPTIONS):
        if isinstance(message, ResultMessage):
            result = message
    runs.append(summary(result))
    return {"reply": result.result}


@app.get("/status")
def status():
    return {"started": started, "runs": runs}
