# IconButton
40 px circular buttons holding a 24 px icon. Four styles: standard (no fill, `on-surface-variant`), filled (`primary`), tonal (`secondary-container`), outlined (`outline` border).
- Toggle icon buttons use `aria-pressed`; the selected standard state takes `primary`.
- Always an `aria-label`. 48 px touch target: add 4 px of margin when they sit in a dense row.
- **Keyboard and screen reader:** `aria-label` starting with its tooltip text; 40 px button, never a hit area under 24 × 24 px; toggles use `aria-pressed`.
- **Angular Material:** `mat-icon-button` (standard). Filled / tonal / outlined have no Angular variant: classes over the same element with `--mdc-icon-button-*` (M2) or `mat.icon-button-overrides` (M3). Always `aria-label`. Full map and theme files: `angular-material.md`.
