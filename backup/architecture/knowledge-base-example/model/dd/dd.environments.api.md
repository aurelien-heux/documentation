---
id: dd.environments.api
level: dd
kind: api
title: api — DeploymentController
application: environments
module: environments/service
owner: team-platform
status: ready
updatedAt: 2026-10-22
realizes: [sbb.environments.deployment-api]
dependsOn: [dd.environments.application]
workItemId: WI-318
---

# api

`DeploymentController` (`POST /environments/{env}/deployments`) maps the OpenAPI contract to `RequestDeploymentUseCase`:

- `RequestDeploymentDto` → `RequestDeploymentCommand` (module split into
  `applicationSlug` and `moduleName`, validated against the Catalog slug pattern)
- `ReservationConflict` → `409` with `holder`, `expiresAt`
- `EnvironmentNotEligible` → `422` with the invariant id in `reason`

```mermaid
classDiagram
  direction LR
  class DeploymentController {
    <<RestController>>
    -RequestDeploymentUseCase useCase
    -DeploymentDtoMapper mapper
    +requestDeployment(env, RequestDeploymentDto) ResponseEntity
  }
  class RequestDeploymentDto {
    <<record>>
    +String module
    +String branch
    +String workItemId
  }
  class DeploymentDto {
    <<record>>
    +UUID id
    +String environment
    +String module
    +String branch
    +String status
    +URI prUrl
  }
  class ReservationConflictDto {
    <<record>>
    +String holder
    +String scope
    +Instant expiresAt
  }
  class DeploymentDtoMapper {
    +toCommand(env, dto, user) RequestDeploymentCommand
    +toDto(DeploymentView) DeploymentDto
  }
  class ApiExceptionHandler {
    <<ControllerAdvice>>
    +ReservationConflict to 409
    +EnvironmentNotEligible to 422
  }
  DeploymentController ..> RequestDeploymentDto
  DeploymentController ..> DeploymentDto
  DeploymentController --> DeploymentDtoMapper
  ApiExceptionHandler ..> ReservationConflictDto
```

Tested by: contract tests generated from `contracts/deployments.openapi.yaml`; web layer
tests with the use case mocked.
