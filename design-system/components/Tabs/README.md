# Tabs
- **Primary tabs** — fixed, equal width, 48 px, a 3 px rounded `primary` indicator under the label; for the top-level sections of a screen.
- **Secondary tabs** — scrollable, content-width, 2 px full-width indicator; for sub-sections inside a tab.
- Active label `primary`, inactive `on-surface-variant`; label-large. Use `role="tab"` and `aria-selected`.
- **Responsive:** Scrollable under 600 px of page area, counts kept; never wrapped onto two lines.
- **Keyboard and screen reader:** `role="tablist"` with one Tab stop (roving tabindex), ← → Home End move and select, each tab `aria-controls` its `tabpanel`; focus ring inside the tab so a scrolling bar does not clip it.
- **Angular Material:** `mat-tab-group` (primary) / `mat-tab-nav-bar` for routed tabs; `mat-tab-group` with `mat-stretch-tabs="false"` for secondary tabs. Indicator `primary` in both; M3 `mat.tabs-overrides` to pin 3 px. Full map and theme files: `angular-material.md`.
