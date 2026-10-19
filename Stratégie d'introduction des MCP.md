# MCP introduction strategy

Oct 19, 2026 · @Aurélien

## Context and goals

We are introducing MCP (Model Context Protocol) as the standard layer for exposing our microservices to AI agents, starting with two read-only MVPs: Documents and Covenants. Today, every AI initiative builds its own integration; MCP gives us a single, secure and auditable contract.

What the MVPs must prove:

- **Technical feasibility** in our stack: Spring Boot, hexagonal architecture, Spring Cloud Gateway.
- **Security acceptable for the bank**: end-to-end user identity from the LDAP directory, existing access rights enforced, full audit trail.
- **Business value**: at least one demonstrable use case per domain.
- **Reproducibility**: a pattern other teams can copy for their own domain.

## Introduction strategy

We introduce MCP in small steps, each validated by a gate before moving on: read before write, internal before external, one proven domain before generalising.

&#91;embedded content: roadmap · 4 phases, 3 validation gates\]

- **Phase 0, framing**: choose the OIDC IdP, validate the LLM with compliance, get the rules below adopted.
- **Phase 1, Documents MVP**: validate the full technical and security chain on a simple domain.
- **Phase 2, Covenants MVP**: prove value on structured business data and on combining two servers.
- **Phase 3, industrialisation**: internal Spring starter, rollout to other domains, then confirmed write operations and approved external clients.

## Team guidelines

These rules are a starting baseline; any exception goes through an architecture review.

**Tool design**

1. One MCP server per business domain (bounded context), never a catch-all server.
2. Tools reflect user intents (`search_documents`, `get_covenant_status`), not CRUD endpoints.
3. Expose BFF APIs first, since they are already use-case oriented; raw CRUD is not exposed.
4. Every tool has a clear description, typed parameters and bounded values (page size, date ranges).
5. No delete or bulk operation exposed without an explicit waiver.
6. Every write follows the two-step `prepare_*` then `confirm_*` pattern, with an idempotency key.

**Hexagonal architecture**

1. The MCP server is an inbound adapter (`adapter/in/mcp`), at the same level as REST controllers.
2. It only calls input ports (use cases) or, in a dedicated MCP server, output ports towards the BFFs.
3. Never direct access to a database, a repository or a REST controller.
4. MCP-specific DTOs and mappers: smaller responses, masked data, designed for an LLM.
5. No business rules in the MCP adapter: they stay in the domain.

**Security**

1. The agent always acts on behalf of an identified user; no shared technical account.
2. OAuth tokens with a dedicated audience per MCP server and a short lifetime (5 to 10 minutes).
3. No passthrough of the received token downstream: token exchange is mandatory.
4. One scope per tool, prefixed `mcp.` and separate from the Angular application scopes.
5. All returned content (document text, comments) is treated as untrusted (prompt injection risk).
6. Data minimisation: IBANs, card numbers and customer identifiers masked by default.

**Operations**

1. Every tool call is logged: user, agent, tool, parameters, result, duration.
2. Quotas per tool and per user, enforced at the gateway and on the server.
3. A kill switch per MCP server, usable without a deployment.
4. Mandatory tests before production: MCP Inspector, access-denied cases, prompt injection tests.
5. MCP servers are versioned; a breaking tool change requires a new version.

## Target architecture

MCP servers are new adapters behind the gateway; BFFs, microservices and LDAP stay unchanged.

&#91;embedded content: target architecture · Documents and Covenants MVPs\]

Two channels coexist and never cross before the BFFs. The **UI channel** is unchanged: the Angular front end calls its BFFs through the gateway's `/api` routes. The **agent channel** goes through the `/mcp` routes and the MCP servers, which exchange the user token with the IdP before calling the same BFFs, and log every call. Downstream, BFF-to-service and service-to-service calls (for example Covenants to Documents) are unchanged and apply their own checks.

## Authentication and authorisation

Users authenticate through an OIDC server backed by our LDAP, and the agent never gets more rights than the user. MCP relies on OAuth 2.1; LDAP remains the reference directory but does not issue tokens.

**Authentication**

- **OIDC provider**: preferably the existing enterprise IdP if already federated with LDAP; otherwise a Spring Authorization Server authenticating against LDAP.
- **Flow**: authorization code + PKCE; pre-registered MCP clients (allow-list), no open dynamic registration.
- **Discovery**: each MCP server returns 401 with a link to `/.well-known/oauth-protected-resource`.
- **LDAP groups** mapped to scopes and roles in the JWT; services never query LDAP directly.

**Three layers of authorisation**

| Layer | Checks |
| --- | --- |
| Spring Cloud Gateway | Valid JWT, audience, coarse scope per route, quotas, kill switch |
| MCP server | `@PreAuthorize` per tool, tool list filtered by scopes, write confirmation, audit |
| Business microservices | Existing checks unchanged (rights on the document, the customer, the credit file) |

**Downstream propagation**: the MCP server exchanges the received token (RFC 8693) for a token intended for the BFF, carrying the user (`sub`) and the agent (`act`). Audit logs keep both.

**Open question**: which OIDC IdP is already available in the bank and federated with LDAP?

## MVP 1: Documents MCP

The first MCP server, read-only, on a non-sensitive document category (internal procedures, policies, product documentation). It is the domain most requested by AI initiatives and the easiest to isolate.

**Demo use case**: "Find the procedure for opening a business account and summarise the key steps."

| Tool / resource | Purpose | Scope |
| --- | --- | --- |
| `search_documents(query, type, dateFrom, dateTo)` | Search; returns metadata only (id, title, type, date) | `mcp.documents:read` |
| `get_document_metadata(id)` | Metadata details for one document | `mcp.documents:read` |
| `get_document_text(id, page)` | Extracted text, paginated and size-bounded; never the raw PDF | `mcp.documents:read` |
| Resource `doc://{id}` | Content access for clients that support MCP resources | `mcp.documents:read` |

**Out of scope**: upload, update, delete, customer documents (ID documents, statements, contracts).

**Risks and mitigations**

- **Prompt injection** through document text: read-only, no write tool in the same agent, adversarial tests.
- **Leakage through search**: the Documents service's access rights also apply to search results, titles included.
- **Size and cost**: pagination, maximum length per response, upstream text extraction.
- **Compliance**: validate the LLM and its hosting location with compliance before any real data.

## MVP 2: Covenants MCP

The second MCP server, read-only, for monitoring covenants on corporate loans. It proves we can expose structured, confidential business data, beyond documents.

**Demo use case**: "Which covenants in my portfolio have a test date in the next 30 days, and which are close to their threshold?"

| Tool | Purpose | Scope |
| --- | --- | --- |
| `list_covenants(clientId, status)` | Covenants for a customer or for the user's portfolio | `mcp.covenants:read` |
| `get_covenant_status(covenantId)` | Threshold, last tested value, headroom, status (compliant, warning, breach) | `mcp.covenants:read` |
| `list_upcoming_tests(days)` | Upcoming test dates and expected documents | `mcp.covenants:read` |
| `get_covenant_history(covenantId)` | Test history and waivers granted | `mcp.covenants:read` |

**Link with Documents**: an agent can combine both servers, for example to find the loan agreement clause that defines a ratio. This is the most convincing demonstration of the MCP approach.

**Specific safeguards**

- Portfolio filtering: a relationship manager only sees their own files, as in the current application.
- No ratio calculation or breach decision by the agent: values come from the business service.
- No writes (waiver, value entry) in the MVP; a future write will go through `prepare_*` / `confirm_*` and four-eyes approval.
- Confidential customer data: demo on a synthetic dataset until compliance has validated the LLM.

**Assumption to confirm**: "covenant" here means the financial covenants of corporate loan agreements, tracked by a dedicated microservice.

## Success criteria and next steps

The MVPs succeed if the five criteria below are demonstrated end to end, on both domains.

**Success criteria**

- [ ] A user signs in through the LDAP-backed OIDC provider from an MCP client (internal agent or Claude).
- [ ] The call goes through Spring Cloud Gateway, the MCP server, then the BFF via token exchange.
- [ ] Existing access rights filter the results, and an access-denied case is demonstrated.
- [ ] Every tool call is logged with the user and the agent.
- [ ] Both demo use cases work, including the Documents + Covenants combination.

**Next steps**

- [ ] Identify the available OIDC IdP and its federation with LDAP.
- [ ] Validate the LLM and its hosting with compliance.
- [ ] Choose the document category and the synthetic covenants dataset.
- [ ] Create the MCP server skeleton (hexagonal Spring Boot module, Spring AI MCP starter, security).
- [ ] Present this framework at the architecture review and the security committee.
