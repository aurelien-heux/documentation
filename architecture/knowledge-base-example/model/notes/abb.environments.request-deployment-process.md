---
id: abb.environments.request-deployment-process
level: note
updatedAt: 2026-10-22
---

Numbered steps; the same labels are reused in the use-case test and the decision table.

```mermaid
flowchart LR
  s1["1.1 Select Environment,<br/>Module, branch"] --> s2["1.2 Check Reservations<br/>(INV-ENV-05, 06)"]
  s2 -- KO --> s3["1.3 Refuse with holder<br/>and expiresAt"]
  s2 -- OK --> s4["1.4 Create Deployment<br/>(requested)"]
  s4 --> s5["1.5 Open auto-merge PR<br/>on Descriptor repository"]
  s5 --> s6["1.6 Publish<br/>EVT-DEPLOYMENT-REQUESTED"]
  s6 --> s7["1.7 Wait for merge<br/>and first Rollout"]
  s7 --> s8["1.8 succeeded | failed"]
```

## Rules

- Step 1.2 is the only place a Reservation is evaluated; it reads the Reservations that are
  `active` at the instant of the request.
- Step 1.5 goes through the CTX-INT Git connector (INV-ENV-03); the process never holds
  credentials.
- Step 1.8 is driven by Observer readings (Jenkins for the PR and Build, ArgoCD or Kubernetes
  for the Rollout), never by a timer.
