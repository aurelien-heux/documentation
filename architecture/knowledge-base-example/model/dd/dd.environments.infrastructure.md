---
id: dd.environments.infrastructure
level: dd
kind: infrastructure
title: infrastructure — outbound adapters
application: environments
module: environments/service
owner: team-platform
status: ready
updatedAt: 2026-10-22
realizes: [sbb.environments.environments-module, sbb.environments.deployment-requested-event]
adr: [adr.environments.auto-merge-pr]
workItemId: WI-318
---

# infrastructure

| Adapter | Implements | Talks to |
|---|---|---|
| `git.DescriptorPrAdapter` | `DescriptorPrPort` | CTX-INT Git connector (REST); edits the Environment descriptor, opens a PR with auto-merge |
| `messaging.DeploymentEventPublisher` | `EventPublisher` | CTX-INT event bus, AsyncAPI contract |
| `persistence.JpaDeploymentRepository` | `DeploymentRepository` | PostgreSQL, `environments` schema |
| `persistence.JpaReservationRepository` | `ReservationRepository` | same |
| `catalog.EnvironmentDescriptorCatalog` | `EnvironmentCatalog` | descriptor projection refreshed by CMD-SYNC-ENVIRONMENTS |
| `outbox.JdbcOutbox` + `outbox.OutboxRelay` | `OutboxPort` | `outbox` table; the relay calls the PR and event adapters after commit |

```mermaid
classDiagram
  direction LR
  class DescriptorPrPort {
    <<port.out>>
  }
  class EventPublisher {
    <<port.out>>
  }
  class DeploymentRepository {
    <<port.out>>
  }
  class ReservationRepository {
    <<port.out>>
  }
  class EnvironmentCatalog {
    <<port.out>>
  }
  class OutboxPort {
    <<port.out>>
  }
  class DescriptorPrAdapter {
    -GitConnectorClient git
    +openAutoMergePr(Placement) PrRef
  }
  class DeploymentEventPublisher {
    -EventBusClient bus
    +publish(DomainEvent)
  }
  class JpaDeploymentRepository {
    -DeploymentJpa jpa
    -DeploymentMapper mapper
  }
  class JpaReservationRepository {
    -ReservationJpa jpa
  }
  class EnvironmentDescriptorCatalog {
    -DescriptorProjection projection
  }
  class JdbcOutbox {
    +append(...)
  }
  class OutboxRelay {
    <<scheduled>>
    +relay()
  }
  DescriptorPrPort <|.. DescriptorPrAdapter
  EventPublisher <|.. DeploymentEventPublisher
  DeploymentRepository <|.. JpaDeploymentRepository
  ReservationRepository <|.. JpaReservationRepository
  EnvironmentCatalog <|.. EnvironmentDescriptorCatalog
  OutboxPort <|.. JdbcOutbox
  OutboxRelay ..> DescriptorPrPort
  OutboxRelay ..> EventPublisher
```

```mermaid
sequenceDiagram
  autonumber
  participant R as OutboxRelay
  participant OB as outbox table
  participant GIT as DescriptorPrAdapter
  participant CI as CTX-INT Git connector
  participant BUS as DeploymentEventPublisher
  participant REPO as JpaDeploymentRepository
  R->>OB: lock next pending entries
  R->>GIT: openAutoMergePr(placement)
  GIT->>CI: POST /descriptor-prs (auto-merge)
  CI-->>GIT: prUrl
  R->>REPO: deployment.prOpened(prUrl), save
  R->>BUS: publish(DeploymentRequested)
  R->>OB: mark done
  note over R,OB: retry with backoff, keyed by deploymentId
```

No adapter holds a credential; the CTX-INT connector authenticates (INV-07, INV-ENV-03).

Tested by: integration tests with Testcontainers (PostgreSQL) and a stubbed Git connector.
