"""The server tells the page what the agent has, and has restarted since app.py was saved."""

from pathlib import Path

from _server import current, fail

source = Path("app.py").read_text()
page = Path("page.html").read_text()

for text, needed, step in [
    (source, "    SystemMessage,", "Import SystemMessage"),
    (source, 'yield {"type": "tools"', "Tell the page what the session was given"),
    (page, '<p id="tools"></p>', "Add a line for the tools under the heading"),
    (page, 'event.type === "tools"', "Fill the line in when the event arrives"),
]:
    if needed not in text:
        fail(f'The step "{step}" has not been applied, or its file was not saved. Run the four steps in order.')

current()

print("The server restarted, and sends the page the tools and model of each run.")
