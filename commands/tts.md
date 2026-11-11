---
description: Turn spoken replies on or off, or stop current audio (/tts on | /tts off | /tts stop)
argument-hint: on | off | stop
allowed-tools: Bash(python:*), Bash(py:*)
---
!`python "${CLAUDE_PLUGIN_ROOT}/scripts/ttsctl.py" $ARGUMENTS || py -3 "${CLAUDE_PLUGIN_ROOT}/scripts/ttsctl.py" $ARGUMENTS`

Reply with only the line above, nothing else.
