---
id: arb.environments.2026-14
level: arb
title: Self-service Deployment on shared Environments
application: environments
board: ARB 2026-14
boardDate: '2026-11-05'
status: in-review
submittedBy: Aurélien Heux
submittedAt: '2026-10-21'
owner: team-platform
updatedAt: '2026-10-23'
from: imp.environments.transition-1
to: imp.environments.target
workItemId: WI-318
requirements: [req.environments.request-deployment, req.environments.reserve-environment]
adr: [adr.environments.auto-merge-pr]
reviewers:
- name: Claire Martin
  role: Enterprise architect
  decision: approved
  at: '2026-10-22'
  note: Traceability complete for the Deployment chain; the target fits the CTX-ENV boundary.
- name: Hugo Lefèvre
  role: Security architect
  decision: changes-requested
  at: '2026-10-22'
  note: Show how the Git connector scopes its token to the descriptor repository, and who can force-release.
- name: Nadia Benali
  role: Platform lead
  decision: pending
- name: Thomas Girard
  role: Data protection officer
  decision: not-required
  note: No personal data beyond user ids already in the IAM directory.
conditions:
- id: C1
  text: Document the token scope of the CTX-INT Git connector (repository, branch protection, rotation).
  owner: team-integration
  due: '2026-11-04'
  status: open
- id: C2
  text: Add the Reservation API detailed design before Transition 1 is extended to self-service.
  owner: team-platform
  due: '2026-11-30'
  status: open
---

## Context and scope

Shared non-production Environments are booked in a Confluence sheet and changed by hand by the
platform team. Transition 1 (live since 2026-10-20) made Reservations enforceable. This submission
covers the move to the target: feature teams request a Deployment of one Module branch, and
Devtoolbox opens an auto-merge PR on the descriptor repository.

In scope: the `environments` Module (Deployment API, Deployment record, DeploymentRequested message),
the CTX-INT Git connector, the change to the Jenkins descriptor job. Out of scope: production
Environments, agent-driven Deployments (OPP-ENV-07).

## Business need

Median lead time from request to placement is 26 hours, and 14 % of manual changes overwrite
another team's placement (2026-Q2). The target outcome is a branch running on a shared
Environment within 5 minutes, without overwrites.

## Architecture overview

The Deployment use case lives in the `environments` Module (hexagonal, Spring Modulith). It reads
active Reservations, records the Deployment, and writes an outbox entry in the same transaction;
the relay opens the auto-merge PR through the Git connector and publishes `DeploymentRequested`.
ArgoCD and the Jenkins descriptor job keep applying the descriptor as today.

## Non-functional requirements

| Requirement | Target | Evidence |
|---|---|---|
| Request latency | p95 < 800 ms | load test on the use case, outbound ports stubbed |
| PR opened | < 30 s after request | outbox relay metric `outbox_lag_seconds` |
| Volume | 200 Deployments / day | sized on 2026-Q2 manual changes × 3 |
| Availability | 99.5 % business hours | same SLO as devtoolbox-backend |

## Security

The Git connector holds the only credential (INV-07). Every Deployment carries the requesting user
and Work item in the PR body. Force-release is limited to the platform admin role and audited.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Unreserved manual changes keep bypassing Devtoolbox | Overwrites continue | Detected by EVT-UNRESERVED-CHANGE-DETECTED (OPP-ENV-04); booking sheet retired (WI-322) |
| Git hosting rate limits during peaks | PRs delayed | Outbox relay with backoff; alert above 60 s lag |

## Open questions

- Should a Deployment wait for the first Rollout before the Reservation can be released?
