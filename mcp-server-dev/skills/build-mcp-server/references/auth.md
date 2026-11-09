# Authentication And Authorization

Use current MCP and OpenAI Plugins auth documentation before implementing version-sensitive flows.

## Default remote model

A remote MCP server should:

1. publish protected-resource metadata
2. point clients to the correct authorization server
3. validate bearer tokens before MCP dispatch
4. validate issuer, audience, expiry, and scopes
5. establish a small authenticated principal in request context
6. authorize every protected resource and action
7. keep upstream credentials separate

## Client registration

For MCP `2026-07-28`, prefer current client metadata document behavior where supported. Keep Dynamic Client Registration only when a required client still needs it.

Do not build a custom OAuth server unless product requirements justify owning that security surface.

## Token rules

- Never forward the incoming MCP bearer token to an upstream API.
- Use token exchange, delegated upstream authorization, or service-owned credentials.
- Reject a valid token minted for another audience.
- Apply least-privilege scopes.
- Do not log bearer tokens, refresh tokens, authorization codes, or sensitive claims.
- Rotate signing keys and cache discovery documents with bounded lifetimes.

## State

Modern remote MCP has no transport session to own user state.

Use:

- authenticated principal ID for durable user data
- request context for one call
- signed or encrypted `requestState` for multi-round-trip flows
- server-side stores for durable jobs and preferences

Do not key token storage or business state by MCP session ID.

## Local servers

For a local stdio server:

- prefer host-provided environment or secure configuration for static credentials
- use the OS keychain for durable user tokens
- open a browser and localhost callback only when OAuth is unavoidable
- scope filesystem and process access independently of authentication

MCPB does not create a sandbox.

## Authorization tests

Test:

- missing token
- invalid signature
- wrong issuer
- wrong audience
- expired token
- insufficient scope
- cross-user resource access
- revoked account or entitlement
- write action without confirmation where confirmation is required
- upstream token exchange failure
