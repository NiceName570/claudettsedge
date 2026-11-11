---
description: Set speaking speed (e.g. +20%, -10%, normal)
argument-hint: +20% | -10% | normal
allowed-tools: Bash(python:*), Bash(py:*)
---
!`python "${CLAUDE_PLUGIN_ROOT}/scripts/ttsctl.py" speed $ARGUMENTS || py -3 "${CLAUDE_PLUGIN_ROOT}/scripts/ttsctl.py" speed $ARGUMENTS`

Reply with only the line above, nothing else.
