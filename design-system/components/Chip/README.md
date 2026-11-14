# Chip

32 px, radius-sm (8 px), label-large at weight 500.

- **Assist / filter (unselected)** — outlined with `outline`, text on-surface.
- **Filter (selected)** — `secondary-container` fill with a leading check.
- **Input** — outlined with a trailing close icon; used for applied filters and tags like `env:prod`.
- **AI chip** — `ai-container` fill with the sparkle icon; marks content a model produced. Only AI features may use it.

Chips sit in a wrapping flex row with space-2 (8 px) gaps. Health status is not a chip: see StatusChip.
- **Keyboard and screen reader:** filter chips are toggle buttons (`aria-pressed`); a chip set has one Tab stop with arrow keys; the remove icon is a 24 × 24 px target named "Remove <label>".
- **Angular Material:** `mat-chip-set` + `mat-chip-option` (filter), `mat-chip-row` (input), `mat-chip` (assist). Selected = `accent` lighter (M2) / `secondary-container` (M3). AI chips: `class="dt-ai"`; health chips are StatusChip. Full map and theme files: `angular-material.md`.
