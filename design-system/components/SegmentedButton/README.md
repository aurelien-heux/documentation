# SegmentedButton
A single-select (or multi-select) group of 2–5 options, 40 px, radius-lg (16 px) outer corners, `outline` dividers.
- Selected segment: `secondary-container` fill with a leading check; others transparent with `on-surface` text.
- Use for views of the same data (Day / Week / Month, List / Grid). For navigation use Tabs; for filters use chips.
- **Keyboard and screen reader:** one Tab stop, arrow keys between segments, `aria-pressed` (multi) or radio semantics (single); focus ring inside the group.
- **Angular Material:** `mat-button-toggle-group` (`appearance="standard"`, `multiple` for multi-select). Selected: `accent` lighter (M2) / `secondary-container` (M3) with a leading check icon; `mat.button-toggle-overrides((shape: 16px))` is set in both theme files. Full map and theme files: `angular-material.md`.
