# AIToolbox · documentation and design workspace

Everything behind AIToolbox (formerly Devtoolbox): the design system, the brand files, the design canvases (system
boards, decision labs, product prototypes), the Angular component library, the architecture knowledge base and the
product and architecture documents. The live versions are Claude artifacts (links in
[`docs/artifact-index.md`](docs/artifact-index.md)); this repository is their source of record.

| Folder | What it holds | Start with |
|---|---|---|
| [`design-system/`](design-system/) | The AIToolbox design system, tokens 5.0.1 (the Sweep palette): `tokens.json` (source), `tokens.css`, colour roles and principles, component rules with the Angular Material 21 (M2) and 22 (M3) tokens, one folder per component (rules + preview), the Angular theme files, the asset groups (logos, state marks, chatbot, feature marks). | `design-system/README.md` |
| [`brand/`](brand/) | Production brand files: logos and wordmark, favicon and app icon, loaders and progress indicators, state marks, feature marks (Sweep, Docs, Environments, Chatbot, Notifications, Architecture), `css/` (tokens with `--md-sys-color-*`, loaders, tooltips), the BNPP Type font. | `brand/README.md` |
| [`canvases/`](canvases/) | The three Design canvases as source files (`canvas.json` + one `.dc.html` per board): `design-system/` (foundations, components, app shell, brand), `labs/` (decision labs, including the colour review), `prototypes/` (live product prototypes, the production vision). | `canvases/README.md` |
| [`packages/aitoolbox-ui/`](packages/aitoolbox-ui/) | Angular workspace of `@aitoolbox/ui`: the component library (ng-packagr) and its showcase app. | `packages/aitoolbox-ui/README.md` |
| [`architecture/`](architecture/) | `knowledge-base-example/`: the architecture knowledge base example (LikeC4 model, ArchiMate notation, ADRs, ARB, detailed design, validation and site tools). `pages/`: the published architecture pages (Meridian Bank, Environments, change process, wide views demo, ArchiMate notation, Jira 3-tier). | `architecture/knowledge-base-example/README.md` |
| [`docs/`](docs/) | Domain reference, architecture decisions and notes, design-system notes (colour review, feature marks), product notes, the Git model and release cycle, the artifact index. | `docs/README.md` |
| [`tooling/`](tooling/) | Scripts that generate the canvas boards and prototypes (`canvas/`), the colour review lab (`colour-review/`). | `tooling/README.md` |

## Conventions

- One source per thing: the design tokens live in `design-system/tokens.json`; `design-system/tokens.css`,
  `brand/css/tokens.css`, the Angular themes and `packages/aitoolbox-ui` follow it.
- No archives and no build output in the repository (`.gitignore`): build the library, the knowledge-base site and the
  standalone canvas pages locally.
- Content in English (`docs/product/mcp-introduction-strategy.fr.md` is the French original).

## History

Until 2026-11-14 this repository held uploaded zips, exports and loose pages. That state is kept on the branch
`archive/2026-11-14-uploads` (zips of the brand 3.3 / 4.1 / 4.5 packages, the 2026-10-28…30 exports, the
architecture, vision-review and intake-tracks updates, the `@aitoolbox/ui` 1.0.0 tarball, the 4.5 mockups and
storybook).
