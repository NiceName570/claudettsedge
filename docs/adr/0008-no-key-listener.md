# ADR 0008: No global key listener, no /tts stop

Status: Accepted (2026-11-11)

Hooks cannot see an empty Enter or Space. A global listener would fire in every app. Rejected; sending a message is the stop gesture.
