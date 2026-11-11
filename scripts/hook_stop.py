"""UserPromptSubmit hook: stop audio if it is still talking. Never disables speech.

The message "ss" is a pure stop signal: Claude is told
not to reply, and the speak hook is told to skip that turn (so the old reply is
not re-spoken).

A /tts command also skips that turn, so its confirmation is never spoken. If
this hook stopped audio for it, a marker tells ttsctl so "/tts stop" can report
that speech was stopped.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tts_common import SKIP_FILE, STOPPED_FILE, stop_playback  # noqa: E402

try:
    data = json.load(sys.stdin)
except ValueError:
    data = {}

stopped = stop_playback()
prompt = (data.get("prompt") or "").strip()
STOPPED_FILE.unlink(missing_ok=True)

if prompt.lower() == "ss":
    SKIP_FILE.write_text("1")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "The user's message is only a signal to stop "
                             "audio. Reply with exactly the word 'Stopped.' and nothing "
                             "else, with no tool calls.",
    }}))
elif re.match(r"/(claudettsedge:)?tts\b", prompt, flags=re.I):
    SKIP_FILE.write_text("1")
    if stopped:
        STOPPED_FILE.write_text("1")
else:
    SKIP_FILE.unlink(missing_ok=True)
