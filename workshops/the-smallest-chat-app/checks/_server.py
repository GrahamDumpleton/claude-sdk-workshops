"""What the checks share: reading what the running server reports about itself.

Nothing here calls the model. A check asks the server's /status route
what it has done, and waits a while for it where a step takes time.
"""

import json
import os
import sys
import time
import urllib.request

PORT = os.environ.get("SERVER_PORT", "")
BASE = f"http://127.0.0.1:{PORT}"


def fail(message):
    print(message)
    sys.exit(1)


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=10) as response:
        return json.load(response)


def status(wait=20):
    """The server's status, giving it a while to come up."""
    deadline = time.time() + wait

    while True:
        try:
            return get("/status")
        except OSError:
            if time.time() > deadline:
                fail(f"Nothing is answering on port {PORT}. Start the server with the action on the welcome page.")
            time.sleep(0.5)


def current(wait=40):
    """The status of a server that has started since app.py was last saved."""
    deadline = time.time() + wait

    while True:
        found = status()
        if found["started"] >= os.path.getmtime("app.py"):
            return found
        if time.time() > deadline:
            fail("The server has not restarted since app.py changed. Look in the server terminal for an error.")
        time.sleep(0.5)


def runs(count=1, wait=120):
    """The runs the server has made, waiting until there are at least `count` of them."""
    deadline = time.time() + wait

    while True:
        found = status()["runs"]
        if len(found) >= count:
            return found
        if time.time() > deadline:
            fail("The run has not finished. Click the action above, wait for the reply in the chat, then check again.")
        time.sleep(1)


def routes():
    """The paths the server answers, from the description FastAPI publishes of itself."""
    return get("/openapi.json")["paths"]
