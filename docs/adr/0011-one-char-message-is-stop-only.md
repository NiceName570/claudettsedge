# ADR 0011: A 1-character message is only a stop signal

Status: Accepted (2026-11-11, revised)

A 1-character message stops audio. Claude is told via hidden context to reply with exactly "Stopped." The speak hook skips that turn, so nothing is spoken. Blocking was rejected (visible blocked notice); an empty reply was rejected (the desktop app forces a visible reply).
