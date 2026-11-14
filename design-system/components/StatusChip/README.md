# StatusChip

Health and log-level colour, kept apart from the brand colours so a green dot means the same thing on every screen.

- **Chip** — label-medium, radius-xs, `*-container` fill with `on-*-container` text, led by the 18 px tinted tile glyph (StateMark C) — a 6 px solid dot only for unknown: `success` healthy / passing, `warning` degraded, `error` down / failed, `surface-container-highest` + `outline` dot for unknown.
- **Log level** — only the level word is coloured, in Open Sans at 600: INFO `success`, WARN `warning`, ERR `error`. The message stays on-surface.
- Never use `primary`, `secondary` or `tertiary` for a status, and never a status colour for a button.
- **Keyboard and screen reader:** the glyph tile is `aria-hidden`, the word is the name ("Failed", not "multiplication x Failed"); never colour alone.
- **Angular Material:** `mat-chip` with `class="dt-chip-success | dt-chip-warning | dt-chip-error | dt-chip-info"` — the classes exist in both theme files; the 18 px tinted tile glyph (StateMark C) goes in `matChipAvatar`. Log levels are plain `span`s, not chips. Full map and theme files: `angular-material.md`.
