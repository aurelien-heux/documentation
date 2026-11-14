---
id: dd.environments.domain-events
level: dd
kind: domain-events
title: domain.event — DeploymentRequested
application: environments
module: environments/service
owner: team-platform
status: ready
updatedAt: 2026-10-22
realizes: [sbb.environments.deployment-requested-event]
workItemId: WI-318
---

# domain.event

`DeploymentRequested(deploymentId, environment, module, branch, requestedBy, workItemId,
requestedAt)` — an immutable record emitted by `Deployment.request`. The outbound messaging
adapter maps it to the AsyncAPI message; the domain never references the bus.

```mermaid
classDiagram
  direction LR
  class DomainEvent {
    <<interface>>
    +occurredAt() Instant
  }
  class DeploymentRequested {
    <<record>>
    +DeploymentId deploymentId
    +EnvironmentName environment
    +ModuleRef module
    +BranchName branch
    +UserId requestedBy
    +WorkItemId workItemId
    +Instant requestedAt
  }
  class Deployment {
    -List~DomainEvent~ events
    +pullEvents() List~DomainEvent~
  }
  DomainEvent <|.. DeploymentRequested
  Deployment o-- DomainEvent : registers
```

The aggregate collects events; the use case pulls them after `save` and hands them to
`EventPublisher`, so the domain never knows about the bus.

Tested by: unit test asserting the event is registered on the aggregate after `request`.
