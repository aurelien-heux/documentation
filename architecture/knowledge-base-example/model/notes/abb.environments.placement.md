---
id: abb.environments.placement
level: note
updatedAt: 2026-10-22
---

The declaration "Module M runs on Environment E from branch B", stored in the Environment
descriptor. A Deployment changes a Placement once; Rollouts then follow each push of B.

Two readings of a Placement exist and the UI always shows which applies:

- **Local placement** — declared on E itself.
- **Effective placement** — the Local placement if one exists, otherwise the Upstream
  environment's placement.

The branch is declared; the running commit and Package are observed, not declared
(DEC-ENV-04).
