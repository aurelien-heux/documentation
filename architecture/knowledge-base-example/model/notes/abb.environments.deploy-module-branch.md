---
id: abb.environments.deploy-module-branch
level: note
updatedAt: 2026-10-22
---

The exposed use case: given an Environment, an `applicationSlug/moduleName` and a branch,
start a Deployment or refuse it with the reason. Domain-reference command:
CMD-REQUEST-DEPLOYMENT.

Becomes the inbound port `RequestDeploymentUseCase` (`application.port.in`).
