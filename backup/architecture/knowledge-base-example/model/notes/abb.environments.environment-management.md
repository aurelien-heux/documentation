---
id: abb.environments.environment-management
level: note
updatedAt: 2026-10-22
---

The ability to see which Module branch runs on which Environment, to place a branch there,
and to protect that placement with a time-boxed Reservation. It is the bounded context
CTX-ENV; its Module boundary in code is the `environments` Spring Modulith module.

## Value stream

Browse Environments → reserve (optional) → request Deployment → first Rollout →
subsequent Rollouts on each push → release Reservation.

## Business functions grouped here

- Environment visibility (list, Effective placement, Drift)
- Reservations (reserve, extend, release, force-release)
- Deployments (request, remove placement)
