# ADR 0012: Windows only, no exe, private dependency install

Status: Accepted (2026-11-11)

- Windows only (PowerShell playback, taskkill).
- No bundled exe: unsigned exes trip antivirus, are opaque, large and hard to update.
- edge-tts is pip-installed on first use into ~/.claude/claudettsedge/lib, never global Python.
- Hooks/commands try `python`, then fall back to `py -3`.
