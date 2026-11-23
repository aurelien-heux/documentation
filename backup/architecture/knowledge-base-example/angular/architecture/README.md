# @aitoolbox/architecture

ArchiMate notation and ARB review components of the AIToolbox design system, as standalone Angular components
(Angular 21 and 22, M2 and M3 themes). Generated from `tools/notation_data.py`: run `tools/build_notation.py` after any
change to the notation, then `npm run build`.

## Install

```ts
// styles.scss — after css/tokens.css (tokens 4.5.0)
@import '@aitoolbox/architecture/styles/archimate.css';
// M2 pages that do not load tokens.css:
@use '@aitoolbox/architecture/styles/theme' as arch;
@include arch.atb-architecture-m2-bridge($dt-light);
html.dark { @include arch.atb-architecture-m2-bridge($dt-dark); }
```

```ts
// optional: mat-icon svgIcon="ax:business-object"
inject(AxIconRegistry).registerWith(inject(MatIconRegistry));
```

## Components

| Selector | Inputs | Notes |
|---|---|---|
| `atb-ax-figure` | `type` `name` `size` (s/m/l) `clickable` `selected` `retired` `change` · output `activate` | role=img, or a button when clickable |
| `atb-ax-tile` | `type` `large` `neutralGlyph` (code/document) | aria-hidden; the row names the type |
| `atb-ax-change` | `change` (new/changed/retired/unchanged) | glyph + word |
| `atb-ax-track` | `plateaus` `member` | aria-label "In …" |
| `atb-ax-relationship` | `type` `highlight` `showName` `width` | SVG sample with ArchiMate markers |
| `atb-readiness-chip` | `readiness` (ready/attention/blocked) | StatusChip |
| `atb-decision-chip` | `decision` | StatusChip |
| `atb-check-row` | `check` · output `open(id)` | finding links |
| `atb-asd-section` | `index` `title` `source` `sectionId` | region, focusable h2 |
| `atb-ax-glyph` | `type` | the 24 px glyph alone |

`notation.generated.ts` exports `AX_TYPES`, `AX_GLYPHS`, `AX_RELATIONSHIPS`, `AX_LAYERS`, `AX_CHANGES` and the types.
`assets/archimate-sprite.svg` has one `<symbol id="ax-<type>">` per type.

## Scripts

`npm run build` (ng-packagr → `../../dist/angular-architecture`) · `npm test` (Jest, jsdom) · `npm run storybook`.
Storybook packages are not in devDependencies: `npx storybook@latest init --type angular` adds them.
