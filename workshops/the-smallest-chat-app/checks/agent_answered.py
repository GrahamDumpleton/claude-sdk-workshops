"""The last run succeeded, used a tool, and gave the closing time that is only in the shop's file."""

from _server import fail, runs

last = runs(1)[-1]

if last["ended"] != "success":
    fail(f"The run ended with {last['ended']}. Ask again with the action above.")

if last["turns"] < 2:
    fail("The agent answered without reading anything. Ask again with the action above.")

if "4:40" not in (last["reply"] or ""):
    fail("The reply does not give the closing time from shop/opening-hours.md. Ask again with the action above.")

print(f"The run took {last['turns']} turns and {last['seconds']} seconds.")
