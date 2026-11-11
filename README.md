# claudettsedge

Claude Code reads its replies to you out loud, using Microsoft Edge's free neural voices ([edge-tts](https://github.com/rany2/edge-tts)).

**Windows only.**

## Install

You need **Python 3.9+** ([python.org](https://www.python.org/downloads/), tick *Add to PATH*). Then, in Claude Code:

```
/plugin marketplace add <github-user>/claudettsedge
/plugin install claudettsedge@claudettsedge
```

Start a new session. The first reply takes ~10 seconds while edge-tts installs into a private folder (`%USERPROFILE%\.claude\claudettsedge\lib`); it never touches your global Python.

## What it says

It reads the plain sentences of each reply. Any sentence with a number, file path, URL or code is skipped, and if anything was skipped it says once:

> "Below I've listed the numbers and directories."

Those details stay in the written reply on screen.

## Commands

| Command | Does |
| --- | --- |
| `/tts on` / `/tts off` | Turn speech on or off |
| `/tts-voice ava` / `/tts-voice aria` | Pick the voice (Ava is default) |
| `/tts-speed +20%` / `-10%` / `normal` | Change speed |

**To stop it mid-sentence:** send any message. A single character (like `k`) just stops the audio — Claude answers "Stopped." and nothing is spoken.

## Privacy

Spoken text is sent to Microsoft's online Edge text-to-speech service to make the audio. Only the filtered sentences are sent, never code, paths or numbers. Use `/tts off` if that's a concern.

## Uninstall

```
/plugin uninstall claudettsedge@claudettsedge
```

Then delete `%USERPROFILE%\.claude\claudettsedge` to remove settings and the private edge-tts install.

## Troubleshooting

- **No sound:** check Windows volume / output device; run `/tts on`.
- **"could not install edge-tts":** run `python -m pip install edge-tts` once yourself.

## License

MIT
