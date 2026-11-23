---
id: sbb.environments.deployment-api
level: note
updatedAt: 2026-10-22
---

REST surface of the use case. `POST /environments/{env}/deployments` with
`{ module: "applicationSlug/moduleName", branch }`; `201` with the Deployment, `409` with the
blocking Reservation (holder, expiresAt), `422` for an Upstream or production Environment.

```mermaid
sequenceDiagram
  autonumber
  actor U as User (portal / Assistant)
  participant API as api.DeploymentController
  participant UC as application.service.DeploymentService
  participant DOM as domain.Deployment
  participant GIT as infrastructure.git.DescriptorPrAdapter
  participant BUS as infrastructure.messaging
  U->>API: POST /environments/{env}/deployments
  API->>UC: request(env, module, branch, user)   %% 1.1
  UC->>DOM: Deployment.request(…, activeReservations)   %% 1.2 · 1.4
  alt covered by another Holder
    DOM-->>UC: ReservationConflict
    UC-->>API: 409 holder, expiresAt   %% 1.3
  else free
    DOM-->>UC: Deployment(requested)
    UC->>GIT: openAutoMergePr(placement)   %% 1.5
    UC->>BUS: publish(DeploymentRequested)   %% 1.6
    UC-->>API: 201 Deployment
  end
```

The step comments map to the business process steps so a contract test and the use-case
test share labels.
