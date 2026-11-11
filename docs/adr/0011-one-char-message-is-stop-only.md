# ADR 0011: The message `ss` is only a stop signal

Status: Accepted (2026-11-11, revised)

The message `ss` stops audio (originally any 1-character message; narrowed to `ss` so single characters stay normal messages). Claude is told via hidden context to reply with exactly "Stopped." The speak hook skips that turn, so nothing is spoken. Blocking was rejected (visible blocked notice); an empty reply was rejected (the desktop app forces a visible reply).
