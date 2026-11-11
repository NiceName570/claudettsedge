# Glossary

- **Spoken summary**: The text actually read aloud for a reply — its clean sentences plus, if needed, the cue.
- **Clean sentence**: A sentence with no digits, file paths, URLs, inline code or code blocks.
- **Cue**: The fixed line "Below I've listed the numbers and directories.", spoken once when any sentence was skipped.
- **Player**: The background process playing the current audio; its PID is kept in `~/.claude/claudettsedge/player.pid`.
- **Stop gesture**: Sending any message while the player is talking; stops audio, does not disable speech.
