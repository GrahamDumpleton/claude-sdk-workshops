"""The server is running and has a route for the chat."""

from _server import PORT, fail, routes, status

status()

if "/chat" not in routes():
    fail("Something is answering on the port, and it is not this workshop's server.")

print(f"The server is answering on port {PORT}.")
