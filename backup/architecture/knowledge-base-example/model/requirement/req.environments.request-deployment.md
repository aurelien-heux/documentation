---
id: req.environments.request-deployment
level: requirement
updatedAt: '2026-10-22'
acceptance:
- given: a non-production Environment E with no active Reservation covering Module M
  when: a user requests the Deployment of branch B of M on E
  then: a Deployment is created in status requested and an auto-merge PR is opened on the Descriptor repository
- given: another Holder has an active Reservation covering (E, M)
  when: a user requests a Deployment of M on E
  then: the request is refused with the Reservation holder and expiresAt in the answer
- given: E is an Upstream environment
  when: a user requests a Deployment on E
  then: the request is refused (INV-ENV-12)
- given: the auto-merge PR is merged and the first Rollout succeeds
  when: CI reports the Rollout
  then: the Deployment moves to succeeded and EVT-DEPLOYMENT-SUCCEEDED is published
decisionTable:
- case: no Reservation on (E, M)
  outcome: OK
- case: own Reservation on (E, M)
  outcome: OK
- case: other Holder, module Reservation on (E, M)
  outcome: KO
  reason: INV-ENV-06
- case: other Holder, application Reservation covering M
  outcome: KO
  reason: INV-ENV-05
- case: other Holder, environment Reservation on E
  outcome: KO
  reason: INV-ENV-05
- case: E is an Upstream environment
  outcome: KO
  reason: INV-ENV-12
- case: E tier is production
  outcome: KO
  reason: INV-ENV-14
operational:
  p95LatencyMs: 800
  deploymentsPerDay: 200
  prOpenWithinSeconds: 30
---

A developer places a feature branch of one Module on a shared non-production Environment
without editing the Environment descriptor by hand, and without stepping on a colleague's
Reservation.

## Goal

Replace the manual descriptor edit (Git PR by hand, review by a platform engineer) with a
self-service action in the portal and in the Assistant, traceable to a Work item.

## Constraints

- Non-production Environments only (DEC-ENV-01).
- Devtoolbox never commits directly: every Placement change is an auto-merge PR (DEC-ENV-03).
- The Deployment targets exactly one Module, one branch, one Environment (INV-ENV-02).
- Reservations are checked before the PR is opened, never after (INV-ENV-06).

## Out of scope

Agent-driven Deployments (OPP-ENV-07) and production Environments (OPP-ENV-06).
