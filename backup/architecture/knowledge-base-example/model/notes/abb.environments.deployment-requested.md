---
id: abb.environments.deployment-requested
level: note
updatedAt: 2026-10-22
---

Raised when a Deployment passes the Reservation check and the descriptor PR is about to be
opened. Domain-reference name: EVT-DEPLOYMENT-REQUESTED. Subscribers: CTX-INT (opens the PR),
CTX-AST (status answers).

Payload: `deploymentId`, `environment`, `applicationSlug/moduleName`, `branch`, `requestedBy`,
`workItemId?`, `requestedAt`.
