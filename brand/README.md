# AIToolbox brand package

Every SVG exists in two versions:

- `light/` — colours for **light backgrounds** (night #0D0B14 box with a white `>` and the neon #00F29E cursor, ink + violet wordmark).
- `dark/` — colours for **dark backgrounds** (lavender #C4C0FF box with a night `>` and the emerald #006C44 cursor, light wordmark).

Colours are fixed in each file (no automatic switching), so you choose the file that matches the surface. All backgrounds are transparent except the favicon tile and the app icon.

## logos/
- `aitoolbox-logo-horizontal.svg` — mark + wordmark, the wordmark centred vertically on the whole mark (badge to box bottom), equal clear space baked in on all sides.
- `aitoolbox-logo-stacked.svg` — centred lockup for square slots and splash screens: mark (badge included) and wordmark centred on one vertical axis.
- `aitoolbox-mark.svg` — the toolbox prompt with the AI badge (light teal `ai` #80D5D4 with "AI" in #003737 — the same in both themes, only `ai-container` changes) on its top-right corner, cut out of the mark; use from 24 px up.
- `aitoolbox-mark-plain.svg` — the mark without the badge, for the favicon, app icon, loader and anything under 24 px.
- `aitoolbox-wordmark.svg` — "AIToolbox" alone, "AI" in ink and "Toolbox" in deep violet (Manrope 800, outlined — no font needed).
- `aitoolbox-mark-once.svg` / `aitoolbox-mark-loop.svg` — the mark animated with the Constructor motion: `-once` builds the logo one time and holds it (splash, app start); `-loop` repeats it (brand loader). Same files as `loading-states/brand-loader-once.svg` and `brand-loader.svg` (AI-tag intro, 4.8 s), here next to the logo. viewBox `-4 2 76 64`.
- `aitoolbox-mark-once.gif` / `aitoolbox-mark-loop.gif` — the same motions as GIF, 256 px on the surface colour (light #FDF8FD, dark #14121E); `-once` has no loop flag and plays one time. For slides, wikis, READMEs and email.
- `aitoolbox-mark-tag-in-once.svg` / `aitoolbox-mark-tag-in-loop.svg` — the AI-tag intro on the finished mark, for places that show the static logo rather than the loader: the plain toolbox sits alone, its top-right corner is carved out, the teal tile grows into the gap, "A" then "I" rise into it and a light sheen crosses it. `-once` (1.4 s) goes from the plain mark to `aitoolbox-mark.svg` and holds it (header logo on first load, login, about box, end slide); `-loop` (4 s) brings the tag in, holds it with a second sheen, folds it back and returns to the plain mark, so it can stop at the end of any cycle (idle screens, wiki banners). viewBox `0 0 74 64`, the same as `aitoolbox-mark.svg`. GIF versions next to them (`-once` plays one time).
- `aitoolbox-mark-24.png` … `aitoolbox-mark-512.png` (height; width = 74/64 × height) and `aitoolbox-logo-horizontal@2x.png`, `aitoolbox-logo-stacked@2x.png`, `aitoolbox-wordmark@2x.png` — transparent PNGs for tools that don't take SVG (Google Slides, older Office, tool avatars, email signatures).

## favicon/
- `favicon.svg` — the `>_` glyph on a rounded night tile (lavender in `dark/`; the tile is the box). Use `light/` as the default favicon; browsers in dark mode can be served `dark/` via `<link rel="icon" media="(prefers-color-scheme: dark)">`.
- `favicon-glyph.svg` — the `>_` glyph alone, no tile, for your own backgrounds.
- `app-icon.svg` — full mark reversed on the night tile (white box, night `>`, emerald cursor), 512 px, for home-screen / PWA icons (maskable-safe).

## loading-states/
- `brand-loader.svg` — Constructor: the AI tag is introduced first — its teal tile grows on the corner, "A" then "I" rise into it and a light sheen crosses it (0.9 s) — then dashed construction guides appear, a teal pen leaves the tag and draws the toolbox in one trip, goes home, and the night toolbox becomes solid while the tag pulses; holds on the logo, loops with a clean cut (4.8 s). The "AI" letters are outlined paths (no font needed). Its viewBox is `-4 2 76 64` (badge, guides and pen all inside, nothing clipped), so size it by height: 96 px tall = 114 px wide.
- `brand-loader-once.svg` — same, plays once and stays on the logo (splash intro).
- `circular-indeterminate.svg` (48 px) and `circular-indeterminate-small.svg` (24 px, also 18 px inside a button) — pen orbit: a violet arc with the teal pen at its head runs around a faint track. Same sizes and roles as Material's circular indicator (`mat-progress-spinner` keeps its slot; this is its skin).
- `linear-indeterminate.svg` / `linear-determinate.svg` — guide line: a dashed teal construction guide as the track, the violet bar runs along it with the pen at its leading edge; determinate = violet to the value, pen on the edge, dashes for the rest. 4 px, top of the app bar, cards, table loading rows (`mat-progress-bar`).
- `brand-progress.svg` — Constructor determinate for long operations with a known value (install, deploy, migration): the pen draws the box in proportion to `--p` (0–100); at 100 add `ait-cd-done` and the toolbox fills. 64–96 px, dialogs and empty states. `brand-progress-demo.svg` loops the cycle.
- `working-dots.svg` (green, a command is executing) and `working-dots-ai.svg` (teal, a model is thinking) — inline after a log line or a chat message.

All animated files respect `prefers-reduced-motion`: they stop on their rest frame (the orbit included).

## css/
- `tokens.css` — the whole design system as CSS custom properties (`--md-sys-color-*`, type scale, shape, elevation, motion). Light by default, dark via `prefers-color-scheme` or `<html data-theme="dark">`.
- `loading-states.css` — the keyframes and classes for the loaders when you inline the SVG markup, wired to the tokens so one markup serves both themes.
- `tooltips.css` — the tooltip formats A–G (plain, shortcut, data, status, disabled reason, rich, AI rich) on the tokens, with the `matTooltip` overrides and the `ait-tip-data` / `ait-tip-status` panel classes; spec in `design-system/components/Tooltip.md` and `mockups/22-tooltips`.
- The token source for build tools is `design-system/tokens.json` at the repository root.

Tokens 5.0.1 (the Sweep palette): the Run action is `--md-sys-color-tertiary-container` (the Sweep lime #DCEAB4, both themes) with `--md-sys-color-on-tertiary-container` (the Sweep purple #39235F); `tertiary` is a signal only (running dots: olive #404B23 in light, pale lime in dark); the focus ring is `primary`; AI marks use `ai` (deep teal #004F50 in light, #80D5D4 in dark); the brand loader uses the brand tokens `logo-ai` / `on-logo-ai`. The 4.x names (`run*`, `nav-active`, `focus-ring`, `ai-strong`, `surface-variant`) remain as aliases at the end of `css/tokens.css` until 5.1. `css/tokens.css` ends with the helpers: the `:focus-visible` rule, `.ait-nav-active`, `.ait-hidden`, `.ait-sr-only` and the reduced-motion stops.

Palette: the Sweep palette (primary the Sweep purple #39235F in light and the lavender #C4C0FF in dark, secondary from the pale purple #DED7EB, tertiary from the lime #DCEAB4; night neutrals from #0D0B14 with the violet `nav-container` band; teal `ai`; the logo family on the night box; shape ceiling 16 px), v5.0.1. SVG files use the Sweep purple; PNG and GIF exports of the logos and feature marks (except Architecture) still carry the 4.5 violet #35307E and need a re-export.

## states/
The state mark is the logo's construction with the state in the badge instead of "AI": the toolbox never changes, the corner badge carries the state role and a symbol (✓ success, i info, ! warning, ✕ error). Pick the file by size:
- `state-<state>-badge.svg` — alone on a surface, 24–40 px: snackbars (24, dark file on the inverse surface), inline alerts and banners (24–28), popin headers (32–40).
- `state-<state>-circle.svg` — in a circle, 56–96 px: table-, panel- or popin-level empty/error states (56–64), page empty states (72–96). Disc in the state role, toolbox reversed, badge in the state container.
- `state-<state>-tile.svg` / `state-<state>-tile-tinted.svg` — tile glyph, 18–20 px: table cells and rows (filled), status chips and dropdown options (tinted).
- `state-pending.svg` — the same circle slot while a request is pending (pen-orbit ring around the plain mark); swap it in place for the state when the request resolves: warning after a timeout, error with Retry on failure. Small slots use the 24 / 18 px pen orbit from `loading-states/`.
Info uses the primary colour. Never below 18 px, never recoloured, no entrance animation.

## Angular
The Angular theme files live in `design-system/angular/` (`theme.m2.scss`, `_theme-colors.scss`, `theme.m3.scss`, `mat-sys-bridge.css`) and in the `packages/aitoolbox-ui` library.

## feature-marks/
Marks for the AIToolbox features, one folder per feature, then `light/` and `dark/`: `sweep/` (agentic SDLC pipeline · broom & sparkle), `architecture/` (the architecture knowledge base; static, once, loop SVG and PNG, no lockup or GIF yet), `docs/` (documentation · shelf), `environments/` (environment management · promotion) `chatbot/` (assistant · the brace box `{ >_ }`, never the brand mark, 24 px minimum) and `notifications/` (notification centre · bell; in the header without its dot, with a count badge). Each theme folder holds the static SVG, `-once.svg` (an entrance that plays one time and holds the mark), `-loop.svg` (a different, working motion that repeats), the outlined lockup, PNGs from 16 to 512 px (Chatbot from 24), the lockup at 2× and once / loop GIFs. Preview: `feature-marks/index.html`; rules and uses: `feature-marks/README.md`.

## fonts/
- `BNPPType-Regular.woff2` — the UI face declared by `tokens.css` (weight 500). Open Sans (body, code) loads from Google Fonts.

