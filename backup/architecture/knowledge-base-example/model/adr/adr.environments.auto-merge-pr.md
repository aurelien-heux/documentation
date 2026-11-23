---
id: adr.environments.auto-merge-pr
level: adr
kind: decision
title: Placement changes through auto-merge PRs, never direct commits
application: environments
owner: team-platform
status: done
updatedAt: 2026-10-02
domainRef: DEC-ENV-03
decision: Devtoolbox changes an Environment descriptor only by opening a PR with auto-merge enabled on the Descriptor repository.
affects:
  - sbb.environments.environments-module
  - dd.environments.infrastructure
  - abb.environments.request-deployment-process
---

# ADR · Placement changes through auto-merge PRs

## Context

The Descriptor repository is already the source of truth for CI/CD (DEC-ENV-02). A direct
commit by a service account would bypass the repository's review hooks and leave no trace
linking the change to a user and a Work item.

## Decision

Every Placement change is a PR opened by the CTX-INT Git connector with auto-merge; the PR
body carries `deploymentId`, `workItemId` and the requesting user.

## Consequences

- Latency: a PR with auto-merge lands in seconds; acceptable against the 30 s target.
- Traceability: every descriptor change has a PR, a Deployment and a Work item.
- Unreserved changes made by hand still bypass Devtoolbox; they are detected, not prevented
  (EVT-UNRESERVED-CHANGE-DETECTED, OPP-ENV-04).

## Alternatives rejected

Direct commit (no review trail); manual PR (defeats self-service).
