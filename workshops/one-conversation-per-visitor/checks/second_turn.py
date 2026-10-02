"""The last two runs were turns of one session."""

from _server import fail, runs

found = runs(2)
first, second = found[-2], found[-1]

if second["ended"] != "success":
    fail(f"The run ended with {second['ended']}. Ask again with the action above.")

if first["session"] != second["session"]:
    fail(
        "The last two runs were in different sessions. Start again from the first action on this page, "
        "then the second."
    )

print(f"Both runs were in session {second['session'][:8]}.")
