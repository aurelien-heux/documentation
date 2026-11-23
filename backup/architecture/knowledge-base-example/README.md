# Devtoolbox architecture knowledge base — example

From intent to code, for one feature (Environment Management, CTX-ENV), with a web page to prepare
Architecture Review Board (ARB) submissions and their Architecture Solution Design (ASD).

| What | Format | Where |
|---|---|---|
| Building blocks (TOGAF): motivation, requirements, ABB, SBB, plateaus, work packages, gaps | **LikeC4** (graph, ArchiMate types) | `model/bb/*.c4` |
| Requirement details: acceptance criteria, decision table, operational figures | Markdown | `model/requirement/<id>.md` |
| Detailed design (DD), one file per hexagonal layer, UML in Mermaid | Markdown (text, optional graph) | `model/dd/*.md` |
| Notes on a building block (state machines, sequences) | Markdown | `model/notes/<id>.md` |
| Architecture decisions | Markdown (MADR) | `model/adr/*.md` |
| ARB submission: reviewers, conditions, ASD narrative | Markdown | `model/arb/*.md` |
| ArchiMate notation of the design system | JSON, CSS, SVG, LikeC4 spec, catalog page | `design-system/archimate/` |

```
model/bb/
  environments.c4        building blocks of the feature (source of truth)
  views.c4               views written by hand (motivation)
  _archimate.spec.c4     generated: one LikeC4 element kind per ArchiMate type (do not edit)
  likec4.config.json
design-system/archimate/
  notation.json          62 element types, 11 relationships, 8 layers, change overlay, 9 components
  tokens.ax.json         --ax-* tokens (W3C Design Tokens, dark in $extensions) → merge into the design-system tokens.json
  archimate.css          components on --md-sys-color-*; --ax-* on html.light / html.dark (load after css/tokens.css)
  tokens-bridge.css      the AIToolbox roles for pages without tokens.css (catalog, previews, Storybook) — never in the app
  components.md          component rules (anatomy, sizes, states, a11y, Angular) — also the project doc
  archimate-likec4.css   LikeC4 skin for the layer colours
angular/architecture/    @aitoolbox/architecture: standalone Angular components (21 / 22), Jest tests, stories, M2 bridge
  archimate.c4           LikeC4 specification (icons ./icons/likec4)
  icons/                 24 px glyphs (currentColor) · icons/likec4/ (ink baked in, for LikeC4)
  index.html             notation catalog page
tools/
  notation_data.py       the notation, single source → build_notation.py
  ea_model.py            loaders: LikeC4 export, Markdown, gap between plateaus
  validate.py            checks + ARB readiness → dist/validation.json, dist/bb.json
  generate.py            dist/likec4/ (with generated views), dist/model.json, dist/index.html
  build_likec4.py        LikeC4 site + <likec4-view> embedded in dist/index.html
  site.template.html     the Architecture feature page (AIToolbox shell and design system)
  likec4/aitoolbox-likec4.css   AIToolbox chrome for LikeC4 (fonts, surfaces, Mantine accent)
```

## Angular library

```bash
cd angular/architecture && npm install
npm run build      # ng-packagr → dist/angular-architecture
npm test           # 17 Jest specs
node harness/build.mjs && python3 -m http.server 8787   # visual harness: harness/index.html (after `npx ngc -p harness/tsconfig.json`)
```
`notation.generated.ts`, `assets/archimate-sprite.svg` and `styles/*.css` are written by `tools/build_notation.py`.

## Run

```bash
pip install pyyaml jsonschema markdown
npm i -g @mermaid-js/mermaid-cli          # UML in DD → inline SVG (light + dark); optional
python3 tools/build_notation.py           # when tools/notation_data.py changes
npx likec4@1.41.0 validate model/bb       # syntax of the building blocks
python3 tools/validate.py                 # checks; exit 1 on a blocking error
python3 tools/generate.py                 # dist/likec4/, dist/model.json, dist/index.html
python3 tools/build_likec4.py             # dist/likec4-site/ and LikeC4 views embedded in dist/index.html
npx likec4@1.41.0 mcp dist/likec4         # the same model for agents (MCP)
```
`LIKEC4=/path/to/likec4` uses a local binary; `MMDC` / `MMDC_PUPPETEER` point at mermaid-cli.

## Conventions in `model/bb`

- **Ids** `<folder>.<applicationSlug>.<name>`: `mot` motivation · `req` requirements and constraints ·
  `abb` · `sbb` · `imp` implementation & migration. Folders are ArchiMate Groupings.
- **Kinds** are ArchiMate types: `abb.environments.reservation = business-object 'Reservation'`.
- **Plateaus**: `imp.<app>.baseline | transition-1 | target` are Plateau elements, chained by `triggering`.
  Membership is made of relationships, never tags, so parallel changes don't edit the same lines:
  the baseline aggregates what exists (`imp.<app>.baseline -[aggregation]-> x`); each later plateau is the
  previous one, plus what the work packages realizing it realize, minus what they `'retires'`.
- **Changes**: one file per change in `model/bb/changes/<work package>.c4`: the work package, the building
  blocks it introduces (`extend abb.<app> { … }`) and its relationships. `dependsOn` metadata orders changes
  that touch the same blocks. The bot folds a change file into `environments.c4` when its plateau is promoted.
- **New / changed / retired** are derived from membership (changed = in both plateaus and realized by a work
  package). Gaps between any two plateaus are computed the same way.
- **Status** `#draft #ready #done #deprecated`, changed only through a Checkpoint decision (INV-12).
- **Traceability** uses ArchiMate relationships: SBB `-[realization]->` ABB `-[realization]->` requirement;
  a work package `-[realization]->` what it delivers, `-[association]-> … 'retires'` what it removes.
- **Metadata**: `owner`, `module` (applicationSlug/moduleName), `workItemId`, `contract`, `adr`, `domainRef`.

DD files realize SBB ids: `realizes: [sbb.environments.deployment-api]`. Requirement details and notes use
the id of the building block they describe.

## Checks (`tools/validate.py`)

| Group | Check | Level |
|---|---|---|
| Structure | S1 frontmatter matches the schema · S2 references resolve · S3 DD realizes SBB only | blocking |
| Traceability | T1 new/changed ABB realizes a requirement · T2 new/changed application SBB realizes an ABB · T4 every requirement realized · T5 acceptance + operational figures | blocking |
| | T3 technology SBB serves another SBB · T6 new/changed application SBB has a DD | warning |
| Plateaus & gaps | P1 every ABB/SBB in a plateau · P2 change tags agree with plateaus | blocking |
| | P3 every gap item addressed by a work package · P4 plateaus chained | warning |
| Ownership & contracts | O1 owner · O2 contract file exists · O3 Work item on new/changed SBB and ready DD | blocking |
| Decisions | D1 referenced ADR exists · D3 accepted ADR names its domainRef | blocking |
| | D2 new application component covered by an ADR | warning |

## ARB / ASD in the page

- **Landscape**: Baseline / Transition 1 / Target views, Gap between any two plateaus (LikeC4 + gap table with
  the work package that delivers each change), Roadmap.
- **Reviews → submission**: readiness (Ready / Needs attention / Blocked) from the checks on the scope of the
  change (the gap between `from` and `to`, plus its DD and requirements), the ASD sections that must be written,
  reviewer decisions and open conditions.
- **ASD**: 13 sections; 6 written in the submission file, 7 assembled from the model (requirements, baseline,
  target, gap and transition, detailed design, decisions). "Copy ASD as Markdown" exports it.
- **Decision**: reviewers record Approve / Approve with conditions / Request changes. In AIToolbox this is a
  Checkpoint decision (CMD-DECIDE-CHECKPOINT); the preview keeps it in the page only.

## ArchiMate notation

All ArchiMate 3.2 element types offered by Archi (strategy, business, application, technology, physical,
motivation, implementation & migration, other) and the 11 relationships. Layer colours are content colours,
never status. Shapes: active structure square, behaviour rounded, passive structure with a header line,
motivation with cut corners. LikeC4 uses the same types as element kinds, with the glyph as icon; the CSS
pins the exact tokens in light and dark (`archimate-likec4.css`). Open `design-system/archimate/index.html`.

## Limits

- LikeC4 1.41: no `style … where`, so gap views style explicit element lists (generated); status and change
  appear as tag stripes in LikeC4 and as glyph + word chips in the page.
- LikeC4 draws every type as a rectangle with its glyph; the ArchiMate figure shapes are in the CSS and catalog.
- The CSS skin relies on `data-likec4-color` and Mantine variables: re-check it when upgrading LikeC4.
