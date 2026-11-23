---
id: dd.environments.domain
level: dd
kind: domain
title: domain — Deployment and Reservation aggregates
application: environments
module: environments/service
owner: team-platform
status: ready
updatedAt: 2026-10-22
realizes: [sbb.environments.environments-module, sbb.environments.deployment-record]
workItemId: WI-318
---

# domain

Package `com.devtoolbox.environments.domain`. No framework imports.

```mermaid
classDiagram
  class Deployment {
    +DeploymentId id
    +EnvironmentName environment
    +ModuleRef module
    +BranchName branch
    +DeploymentStatus status
    +UserId requestedBy
    +WorkItemId workItemId
    +static request(cmd, Environment env, List~Reservation~ active) Deployment
    +prOpened(url)
    +merged()
    +firstRollout(RolloutOutcome)
  }
  class Reservation {
    +ReservationId id
    +ReservationScope scope
    +ReservationTarget target
    +Holder holder
    +Instant expiresAt
    +covers(ModuleRef, EnvironmentName) boolean
    +isActive(Instant) boolean
  }
  class Environment {
    +EnvironmentName name
    +Tier tier
    +boolean isUpstream
    +acceptsSelfServiceDeployment() boolean
  }
  class ReservationConflict {
    +Holder holder
    +Instant expiresAt
  }
  Deployment --> ModuleRef
  Deployment ..> Reservation : checks
  Deployment ..> Environment : checks
  Deployment ..> ReservationConflict : throws
```

## Deployment lifecycle (state machine)

```mermaid
stateDiagram-v2
  [*] --> requested : request()
  requested --> pr_opened : prOpened(url)
  pr_opened --> merged : merged()
  pr_opened --> failed : prRejected(reason)
  merged --> first_rollout : rolloutStarted()
  first_rollout --> succeeded : firstRollout(OK)
  first_rollout --> failed : firstRollout(KO)
  succeeded --> [*]
  failed --> [*]
```

Transitions are methods on the aggregate; any other call throws `IllegalTransition`.
`succeeded` and `failed` are final: a new push creates a Rollout, not a new Deployment.

## Rules carried by the aggregate

- `Deployment.request` throws `ReservationConflict` when any active Reservation of another
  Holder covers (environment, module) — decision-table rows 3–5.
- `Environment.acceptsSelfServiceDeployment()` is false for Upstream environments and for
  tier `production` — rows 6–7.
- One Deployment references one Module, one branch, one Environment: enforced by the
  constructor, not by validation annotations (INV-ENV-02).

Tested by: domain unit tests, one per decision-table row.
