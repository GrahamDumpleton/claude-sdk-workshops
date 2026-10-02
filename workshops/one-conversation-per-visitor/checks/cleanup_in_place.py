"""app.py closes its conversations when the server stops, and the server has restarted since it was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()

for needed, step in [
    ("from contextlib import asynccontextmanager", "Import what a lifespan function needs"),
    ("lifespan=lifespan", "Close every conversation when the server stops"),
]:
    if needed not in source:
        fail(f'app.py has not had the step "{step}" applied, or was not saved. Run the two steps in order.')

current()

print("The server restarted. It will close its conversations when it next stops.")
