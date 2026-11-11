---
description: Turn spoken replies on or off (/tts on | /tts off)
argument-hint: on | off
allowed-tools: Bash(python:*)
---
!`python "${CLAUDE_PLUGIN_ROOT}/scripts/ttsctl.py" $ARGUMENTS`

Reply with only the line above, nothing else.
