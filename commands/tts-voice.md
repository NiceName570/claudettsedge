---
description: Choose the speaking voice (ava or aria)
argument-hint: ava | aria
allowed-tools: Bash(python:*)
---
!`python "${CLAUDE_PLUGIN_ROOT}/scripts/ttsctl.py" voice $ARGUMENTS`

Reply with only the line above, nothing else.
