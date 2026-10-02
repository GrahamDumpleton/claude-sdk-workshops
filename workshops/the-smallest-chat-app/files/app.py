"""The Tidewater Books chat: the server behind the web page."""

import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

started = time.time()  # when this server process began
runs = []  # what the server has kept about each run since it started

app = FastAPI(title="Tidewater Books chat")


class Ask(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def page():
    return Path("page.html").read_text()


@app.post("/chat")
async def chat(ask: Ask):
    return {"reply": f"You said: {ask.message}"}


@app.get("/status")
def status():
    return {"started": started, "runs": runs}
