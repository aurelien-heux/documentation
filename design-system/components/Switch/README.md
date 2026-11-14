# Switch
52×32 px track. On: `primary` track, 24 px `on-primary` handle with an optional check icon. Off: `surface-container-highest` track with a 2 px `outline` border and a 16 px `outline` handle.
- The label sits to the left in settings lists (switch trailing) or to the right in forms.
- A switch applies immediately; if the change needs confirmation use a checkbox and a Save button instead.
- **Keyboard and screen reader:** `role="switch"` with `aria-checked` and a label; Space toggles; the off-state outline is ≥ 3:1.
- **Angular Material:** `mat-slide-toggle` (`color="primary"` in M2; M3 default). The check icon in the handle is `hideIcon="false"` (default since v15). Full map and theme files: `angular-material.md`.
