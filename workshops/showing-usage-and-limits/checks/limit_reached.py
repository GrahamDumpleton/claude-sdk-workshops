"""A run has been made, since the server restarted, that the turn limit ended."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "error_max_turns":
    fail(
        f"The run ended with {last['ended']}, so it finished within the limit. "
        "Ask again with the action above."
    )

print(f"The run was ended by the limit after calling {', '.join(last['calls']) or 'nothing'}.")
