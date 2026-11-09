# Rust 1.0 parity and modernization ledger

Rust 1.0 keeps the useful v1 product behavior and replaces implementation
mechanics that no longer fit the current MCP contract. The retired FastMCP
source was the behavioral oracle until the native server passed contract tests,
Inspector, and real Codex acceptance.

| v1 behavior | Native implementation | Invariant or intentional change | Proof |
| --- | --- | --- | --- |
| Canonical Fabric, Power BI, and Power Automate tools | `rust-server/src/contract.rs` and `operations/` | All 44 original default contracts remain; native stopped-only flow creation, five Graph resource-resolution tools, guarded action patching, and three connector-catalog tools bring 1.4 to 54 | Frozen base-contract test; generated contract tests; Inspector and Codex tool counts |
| Optional aliases and domain tools | Contract inventory filters | 16 aliases, four raw-TMDL, three Power Platform, and two Dataverse tools remain opt-in | Inventory tests for default, read-only, and all-enabled profiles |
| Standard response envelope | `model.rs` | `{ok, summary, data, error, paging, diagnostics}` and explicit null fields remain stable; full JSON is not duplicated in text | Model, operation, native smoke, and byte benchmarks |
| Tool ownership and safety | `tool_registry.rs` | One flat typed registry owns handlers, surfaces, annotations, read-only exposure, and list policy for all 79 possible tools | Registry, runtime-audit, and inventory-profile tests |
| Azure CLI auth | `auth.rs` | Exact resource scopes, sanitized diagnostics, Windows environment normalization, token cache/skew, and serialized acquisition remain | Auth tests and real Codex setup call |
| Fabric and Power BI API helpers | `clients/fabric.rs` and `clients/powerbi.rs` | HTTPS allowlists, bounded pagination, no redirects, origin validation, sanitized errors, safe-method retry only | Local mock API client tests |
| Power Automate compatibility adapter | `clients/power_automate.rs` | Existing endpoint shapes, pagination, safe field projection, run/action diagnostics, and resubmit body remain | Mock endpoint/path/body tests |
| Connector authoring metadata | `clients/power_automate.rs` and `operations/power_automate_connectors.rs` | Strict environment-host derivation, read-only connector/operation projection, no Dataverse, and no generic invocation | URL, request-shape, non-retry, normalization, inventory, Inspector, and live-read tests |
| Guarded flow changes | `operations/power_automate.rs` and `power_automate_logic.rs` | Per-flow locks, drift hashes, dry run, stop/write/readback/restore, deadlines, and ambiguous-write reconciliation remain | Ten mutation state-machine tests, including failure paths |
| Native flow creation | `clients/power_automate.rs` and `operations/power_automate.rs` | Complete local validation, exact connection coverage, dry-run default, one non-retried POST requesting `Stopped`, trusted 202 polling, and exact readback; no Dataverse fallback | Client request tests, zero-request validation tests, failure matrix, Inspector call, and one approved live stopped flow |
| Setup and capability calls | `operations/setup.rs` | Same operational intent, now reports `runtime=rust`, native executable, and the current package version | Inspector and real Codex tool calls |
| Operator guide resource | Embedded public contract plus `operator_guide()` | Guide content and `fabric://operator-guide` remain; wire fields intentionally use standard `uri`, `mimeType`, and `text` | Resource list/read tests |
| MCP startup | `rmcp` server lifecycle | `server/discover` replaces `initialize`; `ping` is not part of the sole `2026-07-28` target | In-process, HTTP, Inspector, and Codex acceptance |
| Modern result metadata | Server handler and HTTP transport | Results use `resultType: complete`, `ttlMs: 300000`, private cache scope, and `io.modelcontextprotocol/serverInfo` | Protocol tests |
| Streamable HTTP | `serving.rs` | Stateless, loopback-only, bearer protected, modern metadata/routing headers required, no session ID | Adversarial HTTP test |
| Portable plugin launch | `mcp.json` and `bin/fabric-mcp-server.exe` | One direct executable; no interpreter, package restoration, listener, or singleton in the plugin path | Rust package contract and PE/version checks |
| Agent evaluation cases | Root `scenarios/` | All 11 fixtures are preserved and execute against current native schemas as tool-selection and safety contracts | Package and agent-scenario gates |

## Fixes found during the port

- Path segments now use RFC 3986 percent encoding. Spaces become `%20`, not
  form-style `+`, before API requests are sent.
- Writes are never automatically retried. A timeout or ambiguous upstream
  response requires a fresh live read before another mutation.
- Pagination and operation `Location` URLs must remain on the expected HTTPS
  origin.
- Timing diagnostics preserve their dynamic stage names instead of flattening
  them into a framework-specific shape.

## Current release boundaries

- The bundled Agent Plugin artifact is Windows x64. The source is portable, but
  macOS, Linux, and Windows ARM64 packages need their own native archive with
  the same relative MCP command contract.
- The private Windows build is not Authenticode-signed. The build reports a
  SHA-256 digest for verification.
- Codex 0.147.0 supports the modern path behind `mcp_2026_07_28` and emits an
  under-development feature warning. The server does not weaken its protocol to
  remove that client-side warning.
- The primary Power Automate management endpoint remains unsupported by
  Microsoft. Its compatibility risk is isolated in one client adapter; stable
  MCP contracts and guarded operation behavior must not change during repairs.
- Definition-based creation intentionally uses that same explicit compatibility
  backend because the proven non-Dataverse path covers the target environment.
  It never silently routes to Dataverse.
- Real acceptance performed setup/auth, capabilities, bounded Fabric and Power
  Automate reads, a controlled Power BI error path, and the one explicitly
  approved connector-free creation proof. The created flow returned HTTP 201,
  remained `Stopped`, and passed an independent MCP readback with one
  Request/Button trigger, one Compose action, and zero connection references.
