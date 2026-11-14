---
id: sbb.environments.deployment-requested-event
level: note
updatedAt: 2026-10-22
---

The integration message for EVT-DEPLOYMENT-REQUESTED on the platform event bus, topic
`devtoolbox.environments.deployment`. Schema in the AsyncAPI contract; consumers are
CTX-INT (opens the PR) and CTX-AST (answers status questions).

Idempotency key: `deploymentId`. Ordering guaranteed per Environment (partition key).
