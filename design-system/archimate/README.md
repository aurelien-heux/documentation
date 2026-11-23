# ArchiMate notation · Notation 2.0

How AI Toolbox draws its architecture: the ArchiMate figures for the model, and the diagram kinds the model needs beyond
ArchiMate (business workflows, process changes, life cycles, detailed design). Every diagram is generated from a YAML
view as **PlantUML or Mermaid** with one AIToolbox theme, in light and dark (DEC-14). Nobody styles a diagram by hand.

Notation 2.0 · tokens 5.0.1 · PlantUML 1.2026.8 · Mermaid 11.16. Replaces Notation 1.x (LikeC4).

| Path | What |
|---|---|
| `theme/aitoolbox.puml` | The PlantUML theme: both themes' colours, design-system glyphs as sprites, one procedure per element type, relationship, step, gate and event procedures, styles for activity, state, class, sequence, component and entity diagrams. |
| `theme/aitoolbox-mermaid.json` | The Mermaid theme: per theme (`light`, `dark`) a `config` (base theme + themeVariables) and the `classDefs` to append. |
| `examples/<kind>.yaml` | The YAML view of each diagram kind. |
| `examples/<kind>.puml`, `.mmd` | The PlantUML and Mermaid sources generated from it. |

Rules, diagram kinds, colour rules and the component list: [`docs/architecture/archimate-notation-components.md`](../../docs/architecture/archimate-notation-components.md).
The rendered reference page: [`architecture/pages/archimate-notation.html`](../../architecture/pages/archimate-notation.html)
(live: the ArchiMate Notation artifact in [`docs/artifact-index.md`](../../docs/artifact-index.md)).
Generator: [`tooling/archimate/`](../../tooling/archimate/).

## Use

PlantUML — include the theme; set the dark theme before the include:

```plantuml
@startuml
!$AX_THEME = "dark"   ' leave out for light
!include aitoolbox.puml
AX_BusinessProcess(prc04, "Change the architecture model")
AX_Agent(apc07, "Architecture agent")
AX_RelAssignment(apc07, prc04, "drafts the update")
@enduml
```

The theme sets `!pragma layout smetana`, so no Graphviz is needed and the in-browser engine (`@plantuml/core`) renders
under a strict content security policy.

Mermaid — pass `config` of the chosen theme to the renderer (`mmdc -c`, or `mermaid.initialize`) and, for flowcharts,
state and class diagrams, append the `classDefs` lines to the source. The example `.mmd` files carry the class names
(`:::agent`, `:::gate`, `:::added`…) but not the `classDefs`: the generator appends them per theme.

## Diagram kinds and default renderer

| Kind | Default | Why |
|---|---|---|
| ArchiMate view (`layered`) | PlantUML | ArchiMate figures and end markers |
| Business workflow (`workflow`) | PlantUML | swimlanes |
| Process change (`process-change`) | PlantUML | swimlanes with change marks |
| State machine (`state-machine`) | Mermaid | native in Markdown hosts |
| Domain model (`class`) | Mermaid | native in Markdown hosts |
| Interaction (`sequence`) | Mermaid | native in Markdown hosts |
| Components and interfaces (`component`) | PlantUML | interface lollipops |
| Data model (`er`) | Mermaid | native in Markdown hosts |

Both renderers are supported for every kind; the default is a proposal for the Preliminary open point "PlantUML or Mermaid".
