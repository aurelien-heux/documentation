# Snackbar
Brief confirmation at the bottom of the screen: `inverse-surface` ground, `inverse-on-surface` text, one optional action in `inverse-primary`, optional close icon.
- 48 px single line, 68 px two lines; radius-xs; elevation-3; 4–10 s then auto-dismiss.
- Never use it for errors that need a decision (use a dialog) and never stack more than one.
- **Responsive:** Under 600 px full width minus 2 × 16 px, 16 px above the NavigationBar; from 600 px 344–600 px wide at the bottom of the page area, aligned on the page margin.
- **Keyboard and screen reader:** `role="status"` (polite); its action is reachable by keyboard while shown and leaves the Tab order when it closes (`visibility: hidden` or removed); never the only place an error is reported.
- **Angular Material:** `MatSnackBar`. M2 hard-codes a dark container: set `--mdc-snackbar-container-color` to `inverse-surface` and `--mdc-snackbar-supporting-text-color` to `inverse-on-surface` (done in `theme.m2.scss`); M3 follows `--mat-sys-inverse-surface` on its own. Leading 24 px state mark (StateMark A, badge in `inverse-primary` on the inverse surface). Full map and theme files: `angular-material.md`.
