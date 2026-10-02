"""The refund skill has been copied to where the SDK looks for a project's skills."""

from pathlib import Path

from _server import fail

if not Path(".claude/skills/refund-reply/SKILL.md").exists():
    fail("There is no .claude/skills/refund-reply/SKILL.md yet. Run the command above.")

print("The skill is at .claude/skills/refund-reply/SKILL.md.")
