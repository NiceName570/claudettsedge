"""Settings control: on | off | stop | voice <ava|aria> | speed <+N%|-N%|normal> | status"""
import re
import sys

import time

from tts_common import (SKIP_FILE, STOPPED_FILE, VOICES, load_config, save_config,
                        stop_playback)


def hook_just_stopped() -> bool:
    """True if the prompt hook stopped audio for this command a moment ago."""
    try:
        fresh = time.time() - STOPPED_FILE.stat().st_mtime < 30
    except OSError:
        return False
    STOPPED_FILE.unlink(missing_ok=True)
    return fresh


def main(argv) -> int:
    if not argv:
        print(__doc__)
        return 1
    cmd, rest = argv[0].lower(), argv[1:]
    cfg = load_config()

    if cmd == "on":
        cfg["enabled"] = True
        msg = "Speech is on."
    elif cmd == "off":
        cfg["enabled"] = False
        stop_playback()
        msg = "Speech is off."
    elif cmd == "stop":
        stopped = stop_playback() or hook_just_stopped()
        msg = "Stopped speech." if stopped else "Nothing was playing."
    elif cmd == "voice":
        name = (rest[0].lower() if rest else "")
        if name not in VOICES:
            print(f"Unknown voice. Choose: {', '.join(VOICES)}")
            return 1
        cfg["voice"] = VOICES[name]
        msg = f"Voice set to {name}."
    elif cmd == "speed":
        raw = (rest[0] if rest else "").strip().lower()
        if raw in ("normal", "0", "+0%", "0%"):
            rate = "+0%"
        else:
            m = re.fullmatch(r"([+-]?)(\d{1,3})%?", raw)
            if not m:
                print("Use a percent like +20%, -10%, or 'normal'.")
                return 1
            rate = f"{m.group(1) or '+'}{m.group(2)}%"
        cfg["rate"] = rate
        msg = f"Speed set to {rate}."
    elif cmd == "status":
        print(f"enabled={cfg['enabled']} voice={cfg['voice']} rate={cfg['rate']}")
        return 0
    else:
        print(__doc__)
        return 1

    save_config(cfg)
    SKIP_FILE.write_text("1")   # a settings confirmation is never spoken
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
