# Changelog

## 1.11.0 - 2026-11-13

- Add offline Fabric REST API docs (`fabric_docs` domain): `fabric_list_api_docs` and
  `fabric_get_api_doc` return operation indexes, single operations with resolved schemas
  and examples, item definition guides and best-practice guides, capped by `max_bytes`.
  Sources are pinned `microsoft/fabric-rest-api-specs` and `microsoft/mcp` content (MIT),
  embedded in the executable; no Azure sign-in or Fabric call.
- Add read-only discovery: `fabric_get_item_definition` (any item type, stable hash,
  resumable exports, semantic model parts withheld unless raw TMDL is enabled),
  `fabric_search_catalog` (Fabric preview), `fabric_list_folders`,
  `fabric_list_capacities`, `fabric_get_operation_state`, `fabric_list_item_schedules`
  and `fabric_get_item_schedule`. Schedule owners and configuration are projected.
- The generic definition hash is separate from the notebook and pipeline edit hashes.
- Declare each tool once next to its typed handler, with its wire contract in
  `rust-server/contract/tools`. A golden snapshot pins every profile's tool list; new
  tools must pass a contract lint. Every 1.10.0 tool contract is unchanged.
- Expose 83 canonical / 65 read-only tools. The operator guide and
  `describe_capabilities` describe the new capabilities.

## 1.10.1 - 2026-11-08

- Include third-party dependency license and notice files with the bundled
  Windows executable. The executable remains the official v1.10.0 artifact.

## 1.10.0 - 2026-10-12

- Add pipeline and Copy Job creation, metadata retrieval/update, and reviewed deletion.
- Add full Copy Job definition retrieval and guarded mapping/property patches.
- Add bounded connection discovery with metadata projection and no credential values.
- Retain the pipeline activity patch contract. Shared item locks cover definition edits,
  metadata updates and deletion.
- Bind confirmed applies to reviewed hashes, submit each mutation once, and verify
  readback. Uncertain creates never retry automatically.
- Deletion exports recovery material and blocks on runs, schedules, known references
  or incomplete scoped checks. No permanent deletion, implicit execution or scheduling.
- Expose 74 canonical / 56 read-only tools. Live lifecycle verification remains separate.

## 1.9.0 - 2026-10-06

- Add `fabric_apply_notebook_patch` for ordered code/Markdown cell insertion,
  source/type updates, removal and reordering. Existing source-only edits stay compatible.
- Preview cell counts, order, types and discarded field names. Type conversions
  require explicit opt-in before discarding populated incompatible outputs or attachments.
- Preserve metadata, bindings, parameter tags, existing IDs and unrelated definition parts.
  New cell IDs are deterministic; Fabric notebooks with missing IDs remain supported.
- Reuse the notebook update lock, two drift checks, single update submission and
  readback reconciliation. Never execute notebooks/pipelines or change schedules.
- Keep definitively failed/cancelled operations as failures; distinguish an accepted
  update's polling permission failure from rejection of the initial update request.
- Expose 61 canonical / 50 read-only tools. Structural editing is hidden in read-only mode.

## 1.8.1 - 2026-10-01

- Accept the legacy `initialize`/`ping` handshake over stdio (negotiating
  `2025-11-25` or `2025-06-18`) so hosts such as Claude Code can connect.
  Discovery and Streamable HTTP remain `2026-07-28` only.

## 1.8.0 - 2026-09-17

- Add fabric_list_onelake_files for bounded, paginated OneLake path listing under Files/ or Tables/.
- Add fabric_read_onelake_file for exact-path byte-slice reads with auto/utf8/base64 encoding and truncation metadata.
- Enforce fixed HTTPS DFS origin, byte caps (2 MiB listing, 1 MiB read, 64 KiB error) via streaming transport, and ETag If-Match on resumed reads.
- Read-only tool surface: 60 canonical / 50 read-only tools. No SQL, Spark, Parquet decoding, or Delta snapshot reconstruction.


## 1.7.0 - 2026-09-15

- Add full DataPipeline definition retrieval and guarded JSON Pointer patches below /properties.
- Preserve unrelated properties, definition parts and display metadata; never run pipelines or change schedules.
- Default to dry run, validate nested activity graphs, check drift twice and reconcile a single write by readback.
- Distinguish rejected updates from permission failures while polling accepted operations.
- Keep the existing pipeline summary contract stable; expose editing availability in capabilities.
- Upstream atomic concurrency protection is unavailable; validation is structural, not execution proof.

## 1.6.0 - 2026-09-14

- Add notebook definition/source retrieval and guarded cell-source replacements.
- Preserve unrelated cells, metadata, attachments and definition parts; never execute notebooks.
- Reject observed source drift, send one update, and verify or reconcile by readback.
- Report notebook support, enablement and permission boundaries in capabilities.
- Atomic concurrency protection is unavailable in the documented upstream API.


## 1.5.1 - 2026-09-14

- Validate Foreach actions using their `foreach` field instead of incorrectly
  requiring `expression`; preserve nested-action and other control validation.
- Add regression tests for valid loops, invalid sources, and nested failures.
- Validate the staged release package, allowing arbitrary worktree folder names.

## 1.5.0 - 2026-08-25

- Stop duplicating complete structured envelopes in tool text, preserving a
  concise summary and actionable error guidance while cutting the measured
  create-flow dry-run wire response by about 59%.
- Add a flat typed registry for all 54 canonical tools and every opt-in tool,
  with compile-time handler/safety ownership, read-only filtering, domain
  scoping, and centralized list policies.
- Standardize positive list bounds, defaults, paging facts, and timing
  diagnostics; make invalid configuration fail with actionable allowed values.
- Replace the repeated Inspector process loop with a two-process persistent
  native smoke, make all 11 agent scenarios executable, and retain one real
  Inspector compatibility call.
- Add a credentials-free Windows CI gate, targeted official MCP 2026-07-28
  conformance scenarios, portable/OpenAI/skill validation, and a version-locked
  one-command release-candidate builder.
- Explicitly disable ambient Dataverse configuration in packaged/example test
  profiles while preserving intentional validated opt-in and the existing
  unsupported Power Automate compatibility adapter.

## 1.4.1 - 2026-08-24

- Enforce connector and operation-result limits locally when Microsoft's
  environment API ignores request bounds, and return total/returned/truncated
  paging metadata.
- Add case-insensitive connector-name search and keep connector list rows to
  the promised name, display name, and tier fields.
- Recheck connector, action/trigger, and deprecation filters locally, normalize
  trigger kinds, and use Microsoft's exact `operationType` for workflow JSON.

## 1.4.0 - 2026-08-24

- Add three native read-only tools to list Power Automate connectors, search
  non-deprecated actions and triggers, and inspect exact operation parameters.
- Use the environment-scoped Power Platform API with the existing Flow token;
  require no Dataverse product, connection mutation, or generic connector
  invocation surface.
- Add strict environment-host derivation, exact-origin enforcement, bounded
  normalized results, non-retried operation search, native contract/client
  tests, and a live Inspector list/search/detail proof.

## 1.3.0 - 2026-08-20

- Add `trace-power-automate-submission`, a reusable read-only workflow for
  tracing one exact correlation key across Power Automate runs, authoritative
  business records, and delivery artifacts.
- Keep system-specific asset maps and completion rules in each system's
  runbook, and never treat missing or ambiguous evidence as permission to retry.

## 1.2.0 - 2026-08-11

- Add `power_automate_apply_guarded_patch` for one to 64 ordered RFC 6902
  `add`, `remove`, or `replace` operations under `/actions`.
- Derive the complete target definition from a fresh live snapshot and preserve
  its complete connection-reference map without requiring either payload from
  the caller.
- Return changed paths, validation details, and before/target hashes on dry run,
  then reuse the existing non-retried update, readback, and state-restoration
  lifecycle for approved live changes.

## 1.1.1 - 2026-08-11

- Reconcile guarded-update activation with a fresh bounded flow readback when
  the activation request times out or errors, without retrying the definition
  update or activation request.
- Treat a verified `Started` readback as successful restoration even when the
  activation response was ambiguous.
- Preserve verified-definition, restoration-attempt, actual final-state,
  failed-phase, and safe-recovery details when activation does not complete.

## 1.1.0 - 2026-08-11

- Add five read-only Microsoft Graph-backed Power Automate resource tools for
  SharePoint connector sources, document libraries, drive items, exact path/ID
  resolution, and verified Excel Run script action resource parameters.
- Return current workbook, folder, file, and Office Script drive-item IDs plus
  drive-relative paths without requiring temporary picker actions or flows.
- Verify source/drive ownership, current workbook/script existence, and file
  types before producing `RunScriptProd` or `RunScriptProdV2` resource fields.
- Add Microsoft Graph scope diagnostics, Graph pagination/origin protections,
  native tests, Inspector coverage, and live read-only resource proof.

## 1.0.1 - 2026-08-11

- Reject deterministically malformed Workflow Definition Language expressions
  before guarded updates acquire a mutation lock or send any HTTP request.
- Return the exact definition JSON pointer and character offset for local
  expression syntax failures, while preserving the local-only dry-run contract.
- Share the same conservative expression validation with stopped flow creation.

## 1.0.0 - 2026-08-10

- Replace the reference FastMCP implementation with one native Rust executable
  built on the official `rmcp` SDK.
- Preserve the 44 original default tools and add native stopped-only
  `power_automate_create_flow`, for 45 default tools total. Preserve 16 optional
  aliases, four raw-TMDL tools,
  three Power Platform inventory tools, two Dataverse tools, public schemas,
  response envelopes, Azure CLI auth, and guarded Power Automate operations.
- Target MCP `2026-07-28` exclusively with `server/discover`, complete-result
  metadata, private caching, standard resource contents, and stateless modern
  Streamable HTTP.
- Package the Windows x64 executable directly in the Agent Plugin with no
  startup restoration or external runtime dependency.
- Add Rust contract, schema, client, HTTP, mutation, package, and preserved
  agent-scenario tests plus Inspector 2.0 and real Codex acceptance.
- Create Power Automate flows directly through the explicit unsupported
  `api.flow.microsoft.com` compatibility backend with complete local
  validation, dry-run by default, one non-retried POST, no Dataverse fallback,
  and exact disabled-flow readback.

## 0.3.0-beta.4 - 2026-08-10

- Upgrade the portable runtime to FastMCP `4.0.0b2`, including lighter startup
  imports and improved client interoperability.
- Keep root `mcp.json` as the single portable MCP declaration used by the Codex
  Agent Plugins loader and other compatible clients.
- Use uv's normal host-managed runtime cache instead of nesting it below plugin
  data, preventing cold-start installation failures on long Windows paths.
- Install `fastmcp-slim[server]` for the portable runtime while keeping the full
  FastMCP distribution in development, so production declares the exact
  supported server surface without the client meta-package.

## 0.3.0-beta.3 - 2026-08-10

- Launch a bundled Python wheel with fully pinned runtime requirements so first
  launch leaves `${PLUGIN_ROOT}` unchanged and writes only beneath
  `${PLUGIN_DATA}`.
- Require a uv-managed Python 3.13 runtime, avoiding host-interpreter drift and
  project builds inside the installed plugin.
- Launch the Inspector smoke through npm's JavaScript entry point so Windows
  execution policy does not block the harness.

## 0.3.0-beta.2 - 2026-08-10

- Package the repository as an Agent Plugins 1.0.0 portable plugin.
- Add a Codex compatibility manifest and a guarded Microsoft Fabric operator
  skill.
- Launch the bundled MCP from the locked source with writable runtime state in
  `${PLUGIN_DATA}`.
- Keep MCP `2026-07-28`, canonical domain-prefixed tools, and the complete
  read/write server surface.

## 0.3.0-beta.1 - 2026-08-05

- Upgrade the server to FastMCP 4.0.0b1 and MCP SDK/types 2.0.0.
- Adopt MCP `2026-07-28` across repo-owned runtime clients.
- Verify the offline, protocol, Inspector, live-read, singleton, and rollback
  gates before activation.
