# Changelog — @aitoolbox/architecture

## 0.1.0 — 2026-10-23

Prefix of every selector, class, CSS variable and TypeScript name: `atb` (AIToolbox trigram), e.g. `atb-ax-figure`,
`AtbCheckRowComponent`, `--atb-primary`, `atb-architecture-m2-bridge`.

First release of the Architecture components (design system 4.5.0, Angular 21 / 22).

- Tokens: `--ax-<layer>-fill` / `-ink` for the 8 ArchiMate layers, light and dark, on `html.light` / `html.dark`
  like `css/tokens.css`; delivered as `tokens.ax.json` (W3C Design Tokens, dark values in `$extensions.aitoolbox.dark`)
  to merge into the design-system `tokens.json`. Components use `--md-sys-color-*` roles only.
- Notation components: `atb-ax-figure` (62 types, 11 figures, sizes S/M/L, clickable, selected, retired, change chip),
  `atb-ax-tile`, `atb-ax-change`, `atb-ax-track`, `atb-ax-relationship`, `atb-ax-glyph`.
- Review components: `atb-readiness-chip`, `atb-decision-chip`, `atb-check-row`, `atb-asd-section`, `atb-status-chip`.
- Icons: `AxIconRegistry.registerWith(MatIconRegistry)` → `svgIcon="ax:<type>"`; `assets/archimate-sprite.svg`.
- Themes: `styles/archimate.css` (both generations) and `atb-architecture-m2-bridge` for M2 pages without `tokens.css`.
- Tests: 17 Jest specs (rendering, names, states, events). Stories: `stories/architecture.stories.ts` (CSF 3, a11y addon).
- Generated from `tools/notation_data.py` by `tools/build_notation.py`: `notation.generated.ts`, sprite, styles.

Known limits: figure shapes are CSS (clip-path); in LikeC4 views every type is a rectangle with its glyph. Icons are
proposals drawn for this system and need a design review against the ArchiMate standard.
