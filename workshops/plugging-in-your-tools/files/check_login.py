"""Ask the model for one word, to find out whether the SDK can reach it with your login."""

import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query


async def main():
    ready = False

    try:
        async for message in query(
            prompt="Reply with the single word: ready",
            options=ClaudeAgentOptions(
                model="haiku",
                system_prompt="Reply with one word.",
                tools=[],
                setting_sources=[],
                strict_mcp_config=True,
                thinking={"type": "disabled"},
                max_turns=1,
                env={"CLAUDE_CODE_SKIP_PROMPT_HISTORY": "1"},
            ),
        ):
            if isinstance(message, ResultMessage):
                ready = not message.is_error
                print("the model replied:", message.result)
    except Exception as error:
        print("the run failed:", error)

    print("ready:", ready)
    Path("login.txt").write_text(f"ready: {ready}\n")
    return ready


sys.exit(0 if asyncio.run(main()) else 1)
