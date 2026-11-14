# Card

Three Material 3 card styles, radius-md (12 px), space-4 (16 px) padding, title-medium heading.

- **Elevated** — `surface-container-lowest` with elevation-1; the default for a service or tool card with actions.
- **Filled** — `surface-container-high`, no shadow; for dense lists and grids.
- **Outlined** — `surface` with an `outline-variant` border; for secondary or grouped content.

A card's actions sit in a flex row at the bottom: Text buttons on the left, one Filled on the right. Status in a card header is a small small badge on a `*-container` fill (see StatusChip), never a coloured title.
- **Responsive:** KPI cards: 4 per row from 720 px of page area, 2 from 300 px (a 360 px phone), 1 below.
- **Angular Material:** `mat-card` (elevated by default, `appearance="outlined"`). Filled: M2 → a class on `surface-container-high`; M3 → `mat.card-overrides`. Radius 12 px set in both theme files. Full map and theme files: `angular-material.md`.
