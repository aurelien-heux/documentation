---
id: sbb.environments.environments-module
level: note
updatedAt: 2026-10-22
---

The deployable unit for CTX-ENV: one Spring Modulith module in the `devtoolbox-backend`
repository, packaged as one container image, deployed by `argocd` (Module field `deployer`).

```mermaid
flowchart TB
  subgraph environments ["environments (Spring Modulith module)"]
    api --> application
    application --> domain
    application --> ports["application.port.out"]
    infrastructure -.implements.-> ports
    infrastructure --> git["CTX-INT Git connector"]
    infrastructure --> bus["CTX-INT event bus"]
    infrastructure --> db[("PostgreSQL · environments schema")]
  end
```

Owns the aggregates Deployment and Reservation; reads Environment descriptors through
CTX-INT; never holds credentials (INV-07).
