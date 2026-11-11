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

LIB_DIR = CONFIG_DIR / "lib"   # private install of edge-tts; never touches global Python

CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def ensure_edge_tts():
    """Import edge_tts, installing it into LIB_DIR on first use."""
    import sys
    if str(LIB_DIR) not in sys.path:
        sys.path.insert(0, str(LIB_DIR))
    try:
        import edge_tts
        return edge_tts
    except ImportError:
        pass
    print("claudettsedge: installing edge-tts (first run only)...", file=sys.stderr)
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check",
         "--target", str(LIB_DIR), "edge-tts"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("claudettsedge: could not install edge-tts. Run:  python -m pip install edge-tts\n"
              + r.stderr[-800:], file=sys.stderr)
        raise SystemExit(0)
    import importlib
    importlib.invalidate_caches()
    import edge_tts
    return edge_tts


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
