"""Shared config and playback state for claudettsedge."""
import json
import os
import subprocess
from pathlib import Path

CONFIG_DIR = Path.home() / ".claude" / "claudettsedge"
CONFIG_FILE = CONFIG_DIR / "config.json"
PID_FILE = CONFIG_DIR / "player.pid"
SKIP_FILE = CONFIG_DIR / "skip_next"

VOICES = {
    "ava": "en-US-AvaMultilingualNeural",
    "aria": "en-US-AriaNeural",
}
DEFAULTS = {"enabled": True, "voice": VOICES["ava"], "rate": "+0%"}

CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    try:
        return {**DEFAULTS, **json.loads(CONFIG_FILE.read_text())}
    except (OSError, ValueError):
        return dict(DEFAULTS)


def save_config(cfg: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def stop_playback() -> bool:
    """Kill the current player if it is still talking. Returns True if one was stopped."""
    try:
        pid = int(PID_FILE.read_text().strip())
    except (OSError, ValueError):
        return False
    PID_FILE.unlink(missing_ok=True)
    r = subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                       capture_output=True, text=True)
    return r.returncode == 0
