# Backup

Files kept for history only, superseded since the TOGAF restart (2026-11-19) and the ArchiMate notation 2.0
(2026-11-23). Paths below `backup/` mirror where they used to live.

| Path | What | Superseded by |
|---|---|---|
| `architecture/knowledge-base-example/` | The pre-restart architecture knowledge base example: LikeC4 model, ArchiMate notation 1.x (CSS, LikeC4 kinds, `@aitoolbox/architecture` Angular library), ADRs, ARB, detailed design, validation and site tools. | The TOGAF framing (YAML model validated by JSON Schema) and `design-system/archimate/` (notation 2.0, PlantUML and Mermaid). |
| `architecture/pages/` | Published pre-restart architecture pages: Meridian Bank, Environments, Architecture Change Process, Jira 3-tier, Wide Views Demo (LikeC4). | The TOGAF framing documents (links in `docs/artifact-index.md`). |

`tooling/canvas/architecture-board/data_prep.py` reads the model of `architecture/pages/architecture-meridian-bank.html`,
now under `backup/`, to rebuild the old Architecture board.

To restore a file, move it back to its old path (`git mv backup/<path> <path>`).
