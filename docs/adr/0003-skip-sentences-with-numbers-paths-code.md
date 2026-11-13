# ADR 0003: Skip whole sentences with numbers, paths or code

Status: Accepted (2026-11-11)

Any sentence containing a digit, a file path/URL, inline code, or a code block/table is skipped entirely — never read with gaps. If a code block or table row with a number or path was skipped, the voice says once: "Below I've listed the numbers and directories." Those details stay in the written reply. Ordinary sentences and list items with a digit or path are skipped silently (2026-11-13: list items no longer trigger the cue, since prose bullets made it fire on most replies), and a lone slash as in "on/off" is not a path.
