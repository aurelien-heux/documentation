---
id: abb.environments.deployment-service
level: note
updatedAt: 2026-10-22
---

Implements the inbound port: evaluates Reservations through the domain, creates the
Deployment aggregate, asks the outbound port to open the descriptor PR, publishes the event.
Classified in the ABB because it describes the service the business expects, independently
of the component that provides it; the SBB below say how.

Becomes `application.service.DeploymentService`.
