"""UserPromptSubmit hook: stop audio if it is still talking. Never disables speech.

A 1-character message is a pure stop signal: Claude is told not to reply, and
the speak hook is told to skip that turn (so the old reply is not re-spoken).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tts_common import SKIP_FILE, stop_playback  # noqa: E402

try:
    data = json.load(sys.stdin)
except ValueError:
    data = {}

stop_playback()

if len((data.get("prompt") or "").strip()) <= 1:
    SKIP_FILE.write_text("1")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "The user's 1-character message is only a signal to stop "
                             "audio. Reply with exactly the word 'Stopped.' and nothing "
                             "else, with no tool calls.",
    }}))
else:
    SKIP_FILE.unlink(missing_ok=True)
