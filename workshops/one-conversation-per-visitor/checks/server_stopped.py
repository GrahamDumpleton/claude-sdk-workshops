"""Nothing is answering on the server's port any more."""

import time

from _server import PORT, fail, get

deadline = time.time() + 15

while True:
    try:
        get("/status")
    except OSError:
        break
    if time.time() > deadline:
        fail(f"The server is still answering on port {PORT}. Click the action above, or press Control and C in the terminal.")
    time.sleep(0.5)

print("The server has stopped.")
