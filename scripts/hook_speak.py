"""Stop hook: speak the spoken summary of Claude's final message."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from tts_common import SKIP_FILE, load_config  # noqa: E402


def last_assistant_text(transcript: Path) -> str:
    last = ""
    with transcript.open(encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") != "assistant" or e.get("isSidechain"):
                continue
            content = (e.get("message") or {}).get("content") or []
            texts = [b.get("text", "") for b in content
                     if isinstance(b, dict) and b.get("type") == "text"]
            if any(t.strip() for t in texts):
                last = "\n".join(texts)
    return last


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    if SKIP_FILE.exists():                      # turn was a 1-character stop signal
        SKIP_FILE.unlink(missing_ok=True)
        return 0
    if data.get("stop_hook_active") or not load_config()["enabled"]:
        return 0
    path = data.get("transcript_path")
    if not path or not Path(path).exists():
        return 0
    text = last_assistant_text(Path(path))
    if text.strip():
        subprocess.run([sys.executable, str(HERE / "speak.py")],
                       input=text, text=True, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
