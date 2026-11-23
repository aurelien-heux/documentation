---
id: dd.environments.data-model
level: dd
kind: data-model
title: data-model — environments schema
application: environments
module: environments/service
owner: team-platform
status: ready
updatedAt: 2026-10-22
realizes: [sbb.environments.deployment-record]
workItemId: WI-318
---

# data-model

Liquibase changelog `db/changelog/environments/0001-deployment-reservation.yaml`:
tables `deployment` and `reservation` as in the SBB data object, the `outbox` table used by the
application layer, plus

- unique partial index on `reservation (environment)` where `scope = 'environment' and
  status = 'active'` — one environment-wide Reservation at a time (INV-ENV-05)
- check constraint `expires_at > starts_at` (INV-ENV-07)
- index `deployment (environment, application_slug, module_name, requested_at desc)`

```mermaid
erDiagram
  deployment {
    uuid id PK
    varchar environment "NOT NULL"
    varchar application_slug "NOT NULL"
    varchar module_name "NOT NULL"
    varchar branch "NOT NULL"
    varchar status "CHECK in lifecycle"
    varchar pr_url
    varchar requested_by "NOT NULL"
    varchar work_item_id
    timestamptz requested_at "NOT NULL"
    bigint version "optimistic lock"
  }
  reservation {
    uuid id PK
    varchar environment "NOT NULL"
    varchar scope "environment|application|module"
    varchar target "NOT NULL"
    varchar holder "NOT NULL"
    varchar reason
    timestamptz starts_at "NOT NULL"
    timestamptz expires_at "CHECK > starts_at"
    varchar status "active|released|expired"
  }
  outbox {
    uuid id PK
    varchar type "OpenPr|Publish"
    uuid aggregate_id FK
    jsonb payload
    varchar status "pending|done|failed"
    int attempts
    timestamptz next_attempt_at
  }
  deployment ||--o{ outbox : "aggregate_id"
```

Tested by: integration tests on a real PostgreSQL (Testcontainers).
