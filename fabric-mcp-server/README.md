# Fabric MCP Server

Native Microsoft Fabric, Power BI, and Power Automate MCP server built with the
official Rust SDK. It targets MCP `2026-07-28`, and accepts the legacy
`initialize` handshake over stdio for hosts that do not yet support it.

The installed Agent Plugin launches one bundled Windows executable over stdio.
It restores no interpreter, package manager, virtual environment, or dependency
set at startup. Azure CLI remains the explicit local authentication provider.

Package 1.10.1 retains the official v1.10.0 executable and includes its
[third-party license notices](THIRD-PARTY-NOTICES.md). Preserve those notices
when redistributing the executable. Compiler source-path strings identify the
Windows build profile and dependency caches; the artifact has not been rebuilt.

## Agent Plugin

The repository root is an Agent Plugins 1.0.0 package with a thin Codex
presentation overlay:

- `plugin.json`: portable package identity.
- `mcp.json`: the single portable MCP declaration.
- `.codex-plugin/plugin.json`: Codex presentation and skill discovery.
- `bin/fabric-mcp-server.exe`: bundled x64 Windows executable.
- `skills/operate-microsoft-fabric/`: target discovery and mutation safety.
- `skills/trace-power-automate-submission/`: read-only, exact-key workflow
  tracing with fail-closed results.

The default package exposes all 74 canonical tools. Compatibility aliases, raw
TMDL, the alternate Power Platform inventory API, and Dataverse metadata remain
explicit opt-ins.

Tool results keep the stable structured envelope. Text content now contains a
short human summary (plus actionable error guidance when needed) instead of a
second complete JSON copy. Clients should consume `structuredContent` for data.

The package contains no credentials. Authenticate once with Azure CLI:

```powershell
az login --allow-no-subscriptions
```

Codex 0.147.0 requires its modern MCP feature for the `2026-07-28` contract:

```powershell
codex --enable mcp_2026_07_28
```

## Standalone stdio

Use `mcpServers.example.json` as the host configuration template, or run the
server directly:

```powershell
.\bin\fabric-mcp-server.exe
```

Start with these calls:

1. `check_local_setup`
2. `describe_capabilities`

`check_local_setup` verifies the Azure CLI account and the Fabric, Power
Automate, Microsoft Graph, Power BI, and OneLake token scopes without returning
credentials.

## Build and validate

The repository pins Rust `1.95.0` and `rmcp` `3.1.2`.

```powershell
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --locked
npm run check:offline
npm run benchmark:native
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build-native-package.ps1
```

The build script creates a statically linked MSVC release executable, verifies
its PE header and version, and reports its SHA-256 digest. Rust tests cover the
public tool/resource contract, input schemas, API clients, pagination and
origin rules, response envelopes, authentication, modern stdio/HTTP protocol
behavior, guarded Power Automate mutations, and the portable package.

The offline gate audits every canonical and opt-in inventory, runs all 11
tool-selection/safety scenarios, and exercises a two-process persistent native
smoke path. MCP Inspector 2.0 is an optional development dependency and is kept
as one compatibility call. Node is not used by
the server or installed plugin.

```powershell
npm ci
npm run smoke:native
npm run inspect:native:smoke
```

Build and validate a staged 16-file release candidate with one command. Add
`-Live` only when authenticated read-only Fabric, Power BI, Power Automate, and
Graph canaries should run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/release-candidate.ps1 -Live
```

The checked-in Inspector profiles set `protocolEra` to `modern`; the server does
not add an obsolete initialization path for older clients.

### Release, install, and rollback

The release-candidate command is local and non-publishing. It produces a
versioned executable, the validated 16-file plugin ZIP, and `SHA256SUMS.txt`
under `target\release-candidate`. Review the clean diff and gate output before
running any command below.

After explicit release authorization, publish the reviewed commit and the exact
validated assets:

```powershell
git push origin main
git tag -a v1.7.0 -m "Fabric MCP Server v1.7.0"
git push origin v1.7.0
gh release create v1.7.0 `
  .\target\release-candidate\fabric-mcp-server-v1.7.0-windows-x64.exe `
  .\target\release-candidate\fabric-mcp-server-1.7.0-windows-x64.zip `
  .\target\release-candidate\SHA256SUMS.txt `
  --repo MylesMCook/fabric-mcp --verify-tag `
  --title "Fabric MCP Server v1.7.0" --generate-notes
```

Publish the same staged 16-file tree to the `mcook-plugins-local` marketplace
entry only after its package validator passes. Then install and verify in a new
Codex task so plugin discovery reloads:

```powershell
codex plugin marketplace upgrade mcook-plugins-local
codex plugin remove fabric-mcp-server@mcook-plugins-local
codex plugin add fabric-mcp-server@mcook-plugins-local
codex plugin list --json
```

Rollback is the same controlled path: restore the marketplace entry to the
v1.4.1 16-file package and hashes, validate and publish that marketplace change,
then rerun the four commands above. The restored executable must report
`fabric-mcp-server 1.4.1` and match the v1.4.1 release checksum. If Windows
reports `Access is denied`, identify and stop only processes whose executable
path is the old Fabric MCP plugin cache; never terminate unrelated Codex or MCP
processes.

## Protocol contract

- MCP version: `2026-07-28`. Stdio also accepts the legacy `initialize` and
  `ping` handshake (negotiating `2025-11-25` or `2025-06-18`) because some hosts,
  including Claude Code, still open stdio servers with `initialize`.
- Discovery: `server/discover` with `resultType: complete`.
- Cache metadata: `ttlMs: 300000`, private scope, and server identity.
- Resources: standard `uri`, `mimeType`, and `text` contents.
- HTTP: stateless Streamable HTTP, required modern metadata and routing
  headers, loopback-only binding, bearer authentication, Host/Origin checks,
  and no session ID.
- Streamable HTTP stays `2026-07-28` only: `initialize` and `ping` return
  method-not-found there.

See `docs/rust-1.0-parity.md` for the v1 behavior map and intentional MCP/Rust
changes.

## Domains

- Fabric workspaces, items, pipelines, job/activity runs, lakehouses, tables,
  semantic models, and TMDL summaries.
- Power BI datasets, refresh metadata, data sources, reports, gateways, status,
  and bounded read-only DAX.
- Power Automate environments, searchable bounded connector and exact operation metadata, flows, definitions, summaries, runs, sanitized
  action diagnostics, disabled definition-based creation, guarded action patches and full updates,
  state control, resubmission, and Graph-backed connector resource discovery.
- SharePoint site sources, OneDrive/SharePoint document libraries, files,
  folders, workbooks, and Office Script IDs, including verified Excel Run
  script action resource-parameter blocks.
- Optional Power Platform cloud-flow inventory and Dataverse metadata.

Workbook data operations, Office Script execution, and MCP prompts remain out
of scope. Graph-backed discovery is read-only and currently supports global
Microsoft 365 SharePoint URLs.

## Safety and configuration

- `FABRIC_MCP_READ_ONLY=true` removes every mutating tool.
- `FABRIC_MCP_ENABLE_ALIASES=true` enables 16 short compatibility aliases.
- `FABRIC_MCP_ENABLE_RAW_TMDL=true` enables four raw semantic-model tools.
- `FABRIC_MCP_ENABLE_POWER_PLATFORM_API=true` enables three optional inventory
  tools and requires `PowerAutomate.Flows.Read`.
- `FABRIC_MCP_TOOL_DOMAINS=all` keeps the full default surface. A comma-separated
  subset of `fabric,powerbi,power_automate,graph,power_platform,dataverse`
  reduces discovery size and skips unrelated authentication checks; setup tools
  remain available.
- `FABRIC_MCP_DATAVERSE_WEB_API_URL=https://<org>.api.crm.dynamics.com/api/data/v9.2`
  enables two metadata-only tools after strict URL validation.
- `FABRIC_MCP_HTTP_TIMEOUT_MS=20000` sets the upstream request timeout.

The packaged and example profiles explicitly leave the Dataverse URL empty, so
an ambient machine setting cannot expand the default non-Dataverse surface.
Invalid booleans, domain names, timeouts, and Dataverse URLs fail at startup
with the setting name and allowed values.

Standard lists default to 100 records (maximum 1000). History calls default to
20 (maximum 100). Connector lists use 100/250 and connector searches 20/100.
Paging reports proven facts; a null `truncated` value does not claim that an
upstream collection is complete.

The primary `power_automate_*` management adapter uses
`api.flow.microsoft.com`. Microsoft does not support that endpoint, so the
adapter is isolated behind stable MCP contracts and guarded readback behavior.
See `docs/power-automate-bridge.md`.

`power_automate_create_flow` uses that compatibility backend directly. It
validates the complete definition and exact connection-reference coverage
before authentication, defaults to dry-run, sends one non-retried POST only
after explicit mutation approval, always requests `state=Stopped`, and verifies
the new flow by independent readback. It never enables, invokes, resubmits, or
deletes the created flow and never falls back to Dataverse.

## Optional loopback HTTP

The same executable can serve authenticated, stateless Streamable HTTP for a
client that cannot launch stdio:

```powershell
$env:FABRIC_MCP_HTTP_BEARER_TOKEN = '<strong-random-secret>'
.\bin\fabric-mcp-server.exe --transport streamable-http --host 127.0.0.1 --port 8765 --path /mcp
```

The server refuses non-loopback binding. The portable plugin does not use this
mode and does not create a task, service, listener, or singleton.

## Repository layout

- `rust-server/`: native source and tests.
- `rust-server/contract/public_mcp_contract.json`: canonical base schemas.
- `rust-server/src/tool_registry.rs`: typed handler, safety, surface, and list
  policy registry for canonical and opt-in tools.
- `scenarios/`: executable tool-selection and safety fixtures.
- `bin/`: packaged executable.
- `inspector/`: MCP Inspector 2.0 profiles.
- `scripts/`: native build and cloud validation commands.

### Notebook source and structure editing

Use `fabric_get_notebook_definition` with workspace and notebook IDs to retrieve
the complete definition, decoded ipynb and `definition_sha256`.
Pass that hash as `expected_definition_sha256` to `fabric_update_notebook_cells`
with `cell_edits: [{"cell_index": 0, "source": "new source\n"}]`. It defaults to
dry run; an authorized write needs `dry_run=false` and `confirm=true`. Only
existing cell sources change. Other cells, metadata, attachments, bindings and
extra parts are preserved; item display metadata is not updated. No execution occurs.

Use `fabric_apply_notebook_patch` for structural changes. It accepts the same
workspace/notebook IDs, retrieval hash and confirmation controls, with
`cell_operations` containing 1–100 ordered operations:

| Operation | Fields | Result |
| --- | --- | --- |
| `insert` | `cell_index`, `cell_type`, `source` | Insert before the index; the current cell count appends. New types are `code` or `markdown`. |
| `update` | `cell_index`, `source` and/or `cell_type`, optional `discard_incompatible_fields` | Replace source, convert type, or both. |
| `remove` | `cell_index` | Remove the cell and its properties. |
| `move` | `cell_index`, `to_index` | Remove the cell and insert it at `to_index` in the remaining array. |

Indices are zero-based and follow preceding operations. The complete patch is
validated locally before any update is submitted. Local validation does not
prove that Fabric will accept the definition. Each requested source is limited
to 1,000,000 UTF-8 bytes.

For example, add an introduction and split a one-cell notebook into sections:

```json
{
  "cell_operations": [
    {"op": "insert", "cell_index": 0, "cell_type": "markdown", "source": "# Introduction\n"},
    {"op": "update", "cell_index": 1, "source": "value = 1\n"},
    {"op": "insert", "cell_index": 2, "cell_type": "code", "source": "result = value + 1\n"}
  ]
}
```

New cells have empty metadata and deterministic unique IDs. Existing IDs,
missing IDs, parameter tags, root metadata, bindings, raw cells and unrelated
properties and parts are preserved. Type conversion requires
`discard_incompatible_fields=true` when it would discard populated code outputs,
a non-null execution count, or Markdown/raw attachments. Empty incompatible
fields are removed automatically; conversion to code initializes empty outputs
and a null execution count. Source-only updates retain existing outputs.

Preview returns `definition_sha256`, `target_definition_sha256` and a `preview`
object with `cells_before`, `cells_after`, ordered `layout`, and `changes`.
Changes identify types, indices, changed sources and discarded field names;
they omit source and output content. Apply returns the verified final hash and
the same preview. Retrieve the full notebook to inspect the resulting sources.
Both writers use the same lock and safeguards described below. The structural
tool is marked destructive and is hidden in read-only mode. It never changes
schedules or executes notebooks or pipelines.

Two fresh hash checks reject observed drift. A single update POST is followed by
readback even on failure; ambiguous updates are never blindly retried. Fabric
operations that definitively fail or are cancelled remain failures even if
readback matches. A permission failure while polling an already accepted
update is reconciled by readback rather than treated as rejection of the POST.
Fabric
does not document atomic conditional updates, so concurrent editors can still
race between the final check and write. An unverified result requires reading
and reviewing the current definition before any new update.

Both endpoints require notebook read/write permissions even for retrieval.
Encrypted sensitivity labels can block retrieval. Capability discovery reports
implementation, enablement and authentication separately; item permissions are
verified only when the notebook request is made.

API references: [get definition](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/get-notebook-definition),
[update definition](https://learn.microsoft.com/en-us/rest/api/fabric/notebook/items/update-notebook-definition).

### Pipeline and Copy Job lifecycle

Use `fabric_get_pipeline` / `fabric_get_copy_job` for metadata and its hash.
`fabric_create_pipeline` / `fabric_create_copy_job` accept a complete definition.
Preview first, then pass `create_request_sha256` back as
`expected_create_request_sha256` for the explicitly authorized apply.
Creation rejects visible name collisions and never runs or schedules the item.

Rename with `fabric_update_pipeline_metadata` /
`fabric_update_copy_job_metadata` using `expected_metadata_sha256`.
An omitted field stays unchanged; an empty description clears it.
Read `fabric_get_copy_job_definition_full` before editing with
`fabric_apply_copy_job_patch`. Its ordered add/remove/replace operations
target `/properties/` or `/activities/`; extra parts and unrelated mappings survive.

`fabric_list_copy_jobs` inventories Copy Jobs. `fabric_list_connections` and
`fabric_get_connection` help select existing connection IDs without exposing
credentials. Metadata visibility proves neither binding permissions nor runtime health.

Deletion uses `fabric_delete_pipeline` / `fabric_delete_copy_job`.
Save the preview's recovery export locally, review coverage and obtain direct
authorization. Apply requires `expected_deletion_preview_sha256`.
Active/unknown runs, enabled or disabled schedules, known references and incomplete
checks block deletion. Reference checks cover declared visible workspaces and supported
literal pipeline references; external consumers remain unverified.
There is no permanent-delete option or automatic cleanup of runs, schedules,
dependencies, connections or destination data. Recreation may require new IDs.

Every mutation defaults to preview. Apply needs `dry_run=false, confirm=true`;
read-only mode hides and rejects mutations. Fresh snapshots and one submission are
followed by independent readback. Unknown creates never automatically retry.

### Activity recipes

Keep using `fabric_apply_pipeline_patch` after full retrieval and hash review.
Add an activity at `/properties/activities/-`; replace a property using its
exact JSON Pointer; remove an activity only after repairing dependent references.
Array order alone does not determine execution order.

| Activity | Definition fields |
| --- | --- |
| Wait | `type: Wait`, `typeProperties.waitTimeInSeconds` |
| Copy | `type: Copy`, source/destination settings and existing connection references |
| Notebook | `type: TridentNotebook`, `typeProperties.notebookId` and `workspaceId` |
| Copy Job | `type: InvokeCopyJob`, `typeProperties.copyJobId` and `workspaceId` |

For a dependent notebook, use `dependsOn` with the Copy Job activity's name
and `dependencyConditions: ["Succeeded"]`. Inside ForEach/Until, patch the
container's `typeProperties.activities`; IfCondition has true/false arrays,
and Switch has case/default arrays. Siblings, expressions and policies remain
intact. Preview checks structure; upstream definition acceptance and execution
are separate verification steps.

## Pipeline definition editing

Use `fabric_get_pipeline_definition_full` with `workspace_id` and `pipeline_id`
to read all definition parts, decoded `pipeline` content and `definition_sha256`.
The existing `fabric_get_pipeline_definition` still returns its activity summary;
it is not a representation suitable for round-trip editing.

Pass the retrieved hash as `expected_definition_sha256` to
`fabric_apply_pipeline_patch`. Its `patch` array accepts 1–64 ordered
add, remove or replace operations below `/properties/`. Paths use JSON Pointer:
`~0` escapes a tilde, `~1` escapes a slash and `-` appends to an array.
Parents must already exist; replace/remove require an existing target. For example:

```json
{
  "patch": [
    {"op": "replace", "path": "/properties/activities/0/typeProperties/waitTimeInSeconds", "value": 10}
  ],
  "dry_run": true
}
```

The example is the patch portion; include workspace/pipeline IDs and the retrieval
hash in the tool call. Dry run is the default. Apply only after reviewing the
candidate and obtaining authorization, with `dry_run=false` and `confirm=true`.
The tool preserves unrelated properties and definition parts, excludes `.platform`
from the update and sends `updateMetadata=false` to preserve item display metadata.
It never starts a pipeline or changes its schedule. Copy Job items are a different
Fabric item type and are outside this tool's scope.

Validation checks the JSON structure, unique activity names, sibling dependency
references and cycles, including ForEach, Until, IfCondition and Switch containers.
It is not exhaustive activity-specific validation, connection permission checking
or proof of successful execution. Definitions and patches are limited to 4 MiB;
activity graphs to 1,000 activities and 16 nested levels. A dry run sends no update
request and does not ask Fabric to validate the candidate.

Both definition endpoints require pipeline read/write permissions, even for reads.
`describe_capabilities.pipeline_editing` distinguishes configured availability
from item permissions, which are only verified by a request. Read-only mode hides
the patch tool. Writes use two fresh hash checks and a single update request,
follow long-running operations and reconcile the resulting definition. The hash
includes item metadata and all parts, with JSON formatting and part order normalized.
There is no documented atomic conditional-write API: a concurrent editor can still
race the update. Unverified outcomes are not retried or rolled back automatically;
retrieve the latest definition and inspect any pending operation before another edit.

Run `npm run smoke:pipeline:live` with the existing local smoke configuration and
Azure CLI authentication to check retrieval, a description dry run and unchanged
readback. It logs no pipeline source or identifiers and performs no live writes.

API references: [get definition](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items/get-data-pipeline-definition),
[update definition](https://learn.microsoft.com/en-us/rest/api/fabric/datapipeline/items/update-data-pipeline-definition),
and [definition format](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/datapipeline-definition).


## OneLake file inspection

Use `fabric_list_onelake_files` with workspace/lakehouse GUIDs and a lakehouse-relative path
starting with `Files` or `Tables` to list one bounded page of paths (default limit 100, max 1000).
Continuation tokens arrive through `paging.continuation_token`; pass them back unmodified.
The listing caps the response body at 2 MiB and never silently drops entries.

Use `fabric_read_onelake_file` for an exact file path to read a bounded byte slice
(default 64 KiB, max 1 MiB) with `offset` and `encoding` (auto, utf8, base64).
The tool sends a `Range` header, verifies the returned range, and reports
`available_bytes`, `truncated`, and `next_offset`. Nonzero offsets require
`expected_etag`, sent as `If-Match`, so resumed reads cannot mix file versions.
Reading under `Tables` inspects raw files only; it does not reconstruct a consistent
Delta table snapshot. Truncated slices may split records.

Both tools are read-only, never execute queries or Spark, never write files, and
require lakehouse read permission on the selected item; a passing token check does
not prove item access. Error bodies are capped at 64 KiB and never leak credentials
or signed URLs.

API references: [OneLake access](https://learn.microsoft.com/fabric/onelake/onelake-access-api),
[Path - List](https://learn.microsoft.com/rest/api/storageservices/datalakestoragegen2/path/list),
[Path - Read](https://learn.microsoft.com/rest/api/storageservices/datalakestoragegen2/path/read).

Configure `onelake.targets` in the ignored `.fabric-smoke.local.json` as an array of
objects containing `workspace_id`, `lakehouse_id`, and a discovered `path`. Use a
directory containing files larger than one byte. Run `npm run smoke:onelake:live`
with Azure CLI authentication to verify listing, paging, one-byte truncation, and
ETag-based continuation. The smoke fails if any check is blocked or fails; it never
falls back to a different workspace. `ONELAKE_TEST_BINARY` selects an installed binary.
Offsets at or beyond EOF return a range error, except an empty file at offset zero.
It logs no file content, paths, identifiers, or signed URLs, and performs no live writes.
