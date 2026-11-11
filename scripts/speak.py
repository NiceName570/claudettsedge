"""Speak a Claude reply aloud with edge-tts.

Usage:
  python speak.py --text "reply text"     speak given text
  python speak.py < reply.txt             speak text from stdin
  python speak.py --dry-run --text "..."  print what would be spoken, no audio
"""
import argparse
import asyncio
import re
import subprocess
import sys

from tts_common import CONFIG_DIR, load_config, stop_playback, PID_FILE

CUE = "Below I've listed the numbers and directories."
AUDIO_FILE = CONFIG_DIR / "last.mp3"

PATH_RE = re.compile(
    r"[A-Za-z]:\\"                      # C:\
    r"|(?:^|\s)[~.]?[\\/]\w+[\\/]"      # /foo/, ./foo/, ~/foo/ (not /tts commands)
    r"|\w[\\/]\w"                       # foo/bar, foo\bar
    r"|\b\w+\.(?:py|md|json|js|ts|tsx|txt|html|css|ps1|sh|exe|toml|yaml|yml|mp3)\b"
    r"|https?://"
)


def strip_markdown(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)   # [text](link) -> text
    s = re.sub(r"^\s*#+\s*", "", s)                  # headers
    s = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", s)     # bullets / numbered items
    s = re.sub(r"[*_]{1,3}", "", s)                  # bold / italics
    return s.strip()


def build_summary(text: str) -> str:
    """Keep clean sentences; drop any with numbers or paths. Add the cue only if
    something with a number or path was actually dropped."""
    skipped = False

    def has_detail(s: str) -> bool:
        return bool(re.search(r"\d", s) or PATH_RE.search(s))

    for block in re.findall(r"```.*?(?:```|$)", text, flags=re.S):
        skipped = skipped or has_detail(block)
    text = re.sub(r"```.*?(```|$)", " ", text, flags=re.S)

    kept = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("|"):                     # table row: never spoken
            skipped = skipped or has_detail(line)
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            sentence = sentence.replace("`", "")
            if not sentence:
                continue
            if has_detail(sentence):
                skipped = True
                continue
            clean = strip_markdown(sentence)
            if clean:
                kept.append(clean)

    if skipped:
        kept.append(CUE)
    return " ".join(kept)


async def synth(text: str, voice: str, rate: str) -> None:
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(str(AUDIO_FILE))


def play(path) -> None:
    ps = (
        "Add-Type -AssemblyName PresentationCore;"
        "$p=New-Object System.Windows.Media.MediaPlayer;"
        f"$p.Open([uri]'{path}');"
        "$i=0; while(-not $p.NaturalDuration.HasTimeSpan -and $i -lt 50){Start-Sleep -m 100;$i++};"
        "$p.Play();"
        "Start-Sleep -m ([int]$p.NaturalDuration.TimeSpan.TotalMilliseconds + 300);"
        "$p.Close()"
    )
    flags = 0x00000200 | 0x08000000  # CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
    proc = subprocess.Popen(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps],
        creationflags=flags, close_fds=True,
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    PID_FILE.write_text(str(proc.pid))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    summary = build_summary(text)

    if args.dry_run:
        print(summary)
        return 0

    cfg = load_config()
    if not cfg["enabled"] or not summary:
        return 0

    stop_playback()
    asyncio.run(synth(summary, cfg["voice"], cfg["rate"]))
    play(AUDIO_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
