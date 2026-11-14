# Changelog

## 1.0.0 — 2026-10-27

First release, from design system 4.5.0 (tokens 4.5.0).

- Theme entry files `aitoolbox-m3.scss` (Material 3, Angular Material 22 and 21) and `aitoolbox-m2.scss` (M2 API, 21).
- Tokens regenerated from `tokens.json` with `light-dark()`; the design system's published `tokens.css` was stale (old
  navy palette) and is replaced by this one.
- Global overrides for Table, Paginator, Sort, Expansion, Stepper, Tree and Tooltip; `dt-tonal` and `dt-danger` classes.
- Components: AppShell, AppHeader, SearchAsk, StateMark, StatusChip, LogLevel, PenOrbit, GuideLine, WorkingDots,
  ConstructorProgress, BrandLoader, Logo, ChatbotMark, AiChip, Banner, EmptyState, AitSnackBar, AitConfirm,
  AitDialogTitle, AitDisabledReason, button-role directives (`aitRun`, `aitRunText`, `aitTonal`, `aitDanger`, `aitAi`),
  AitWindowClass, `provideAitIcons()`.
