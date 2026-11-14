# aitoolbox-ui

Workspace of `@aitoolbox/ui`, the AIToolbox design system for Angular (see `projects/ui/README.md` for consumers).

| Path | What |
|---|---|
| `projects/ui` | The library (ng-packagr). `styles/` theme files, `tokens/tokens.json` source tokens, `assets/` design-system SVGs, `fonts/`. |
| `projects/showcase` | Demo app: a Runs page in the app shell and a gallery of every component, light and dark. |
| `tools/build-tokens.mjs` | Generates `styles/tokens.css`, `styles/_tokens.scss` and `src/lib/core/tokens.ts` from `tokens.json`. |
| `tools/build-brand.mjs` | Generates the theme-aware logo template from `assets/logos/*-light.svg`. |

## Commands

```bash
npm ci
npm run build:lib        # tokens + brand generation, then ng-packagr → dist/aitoolbox-ui
npm run test:lib         # Vitest unit tests
npm run build:showcase   # after build:lib
npm start -- showcase    # dev server for the showcase
npm run pack:lib         # dist/aitoolbox-ui-<version>.tgz
```

The workspace is on Angular 21.2 on purpose: a library compiled with 21.2 runs in Angular 21 and 22 apps, the reverse is
not true. Move the workspace to 22 when the last 21 app has upgraded, and raise the peer range then.

## Updating from the design system

1. Replace `projects/ui/tokens/tokens.json` with the design system's `project/tokens.json`.
2. Copy changed SVGs into `projects/ui/assets/…` and `angular/theme.*.scss` into `styles/_theme-m3-core.scss` /
   `_theme-m2-core.scss` if the design system changed them.
3. `npm run build:lib && npm run test:lib`, check the showcase, bump the version and the changelog.
