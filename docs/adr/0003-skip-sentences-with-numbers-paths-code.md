# ADR 0003: Skip whole sentences with numbers, paths or code

Status: Accepted (2026-11-11)

Any sentence containing a digit, a file path/URL, inline code, or a code block/table is skipped entirely — never read with gaps. If something listed was skipped (a code block, table row, or list item with a number or path), the voice says once: "Below I've listed the numbers and directories." Those details stay in the written reply. An ordinary sentence with a digit is skipped silently, and a lone slash as in "on/off" is not a path.
