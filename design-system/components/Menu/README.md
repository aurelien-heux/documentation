# Menu
Temporary surface of 48 px items on `surface-container`, radius-xs, elevation-2, 8 px vertical padding; 112–280 px wide.
- Items: 20 px leading icon, body-medium label, optional trailing shortcut in label-medium `on-surface-variant`. Hover: `primary` state layer at 6 % (#ECE5F7 on the light menu); keyboard focus: the focus ring, no layer, so a clicked item keeps no tint.
- Destructive items in `error`, last, after a divider when the menu is long. Opens from a trailing "more" icon button or a right-click.
- **Keyboard and screen reader:** the trigger has `aria-haspopup="menu"` and `aria-expanded`; opening moves focus to the first item; ↑ ↓ Home End move; Esc and Tab close and return focus to the trigger (`mat-menu` does this).
- **Angular Material:** `mat-menu` + `matMenuTriggerFor`, items `mat-menu-item`. M2: `--mat-menu-container-shape: 4px`, `background.card`; M3: `mat.menu-overrides((container-shape: 4px))`. List-level states are non-selectable items (see angular-material.md). Full map and theme files: `angular-material.md`.
