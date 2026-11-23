---
id: dd.environments.application
level: dd
kind: application
title: application — RequestDeployment use case
application: environments
module: environments/service
owner: team-platform
status: ready
updatedAt: 2026-10-22
realizes: [sbb.environments.environments-module]
dependsOn: [dd.environments.domain, dd.environments.ports]
workItemId: WI-318
---

# application

`DeploymentService implements RequestDeploymentUseCase`:

1. `EnvironmentCatalog.find(env)` — step 1.1
2. `ReservationRepository.findActiveCovering(env, module, now)` — step 1.2
3. `Deployment.request(cmd, environment, active)` — steps 1.3 / 1.4
4. `DeploymentRepository.save` + `OutboxPort.append(OpenPr, DeploymentRequested)` — one transaction
5. After commit, `OutboxRelay` (infrastructure) opens the PR — step 1.5 — and publishes the event — step 1.6

```mermaid
classDiagram
  direction LR
  class RequestDeploymentUseCase {
    <<port.in>>
    +request(RequestDeploymentCommand) DeploymentView
  }
  class DeploymentService {
    -EnvironmentCatalog environments
    -ReservationRepository reservations
    -DeploymentRepository deployments
    -OutboxPort outbox
    -Clock clock
    +request(RequestDeploymentCommand) DeploymentView
  }
  class RequestDeploymentCommand {
    <<record>>
    +EnvironmentName environment
    +ModuleRef module
    +BranchName branch
    +UserId requestedBy
    +WorkItemId workItemId
  }
  class DeploymentView {
    <<record>>
    +id
    +status
    +prUrl
  }
  RequestDeploymentUseCase <|.. DeploymentService
  DeploymentService ..> RequestDeploymentCommand
  DeploymentService ..> DeploymentView
```

```mermaid
sequenceDiagram
  autonumber
  participant UC as DeploymentService
  participant ENV as EnvironmentCatalog
  participant RES as ReservationRepository
  participant D as Deployment
  participant REPO as DeploymentRepository
  participant OB as OutboxPort
  UC->>ENV: find(env)
  ENV-->>UC: Environment
  UC->>RES: findActiveCovering(env, module, now)
  RES-->>UC: List of Reservation
  UC->>D: request(cmd, environment, active)
  alt ReservationConflict or not eligible
    D-->>UC: throw
  else free
    D-->>UC: Deployment(requested) + DeploymentRequested
    rect rgba(120,120,200,0.12)
      note over UC,OB: one transaction
      UC->>REPO: save(deployment)
      UC->>OB: append(OpenPr, DeploymentRequested)
    end
  end
```

Transactional boundary: steps 2–4 in one transaction; the PR call is executed after commit
through an outbox so a failed Git call never leaves a Deployment without a PR nor a PR
without a Deployment.

Tested by: use-case test with all outbound ports stubbed, one scenario per acceptance row.
