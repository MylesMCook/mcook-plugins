---
name: operate-microsoft-fabric
description: Operate and diagnose Microsoft Fabric, Power BI, and Power Automate through the bundled microsoft_fabric MCP server. Use for Fabric workspace and item inventory, notebook source inspection and guarded cell edits, pipeline definition edits and job failures, lakehouse and semantic-model inspection, Power BI datasets, refreshes, gateways, reports, DAX queries, and Power Automate flow definitions, connector resource IDs, stopped creation, runs, errors, guarded patches or updates, state changes, or resubmission.
---

# Operate Microsoft Fabric

Use the bundled `microsoft_fabric` MCP server as the authoritative execution
surface. Do not silently switch to another Fabric registration, endpoint, CLI,
or copied server when the bundled server is unavailable.

## Start every operation

1. Call `check_local_setup`.
2. Call `describe_capabilities`.
3. Stop and report the exact missing prerequisite or permission when setup is
   not ready. Never request, print, or persist Azure tokens or credentials.
4. Confirm the relevant domain and optional feature are enabled before choosing
   a tool. Do not infer that raw TMDL, Power Platform inventory, or Dataverse is
   available.

## Resolve targets

- Discover workspaces, environments, items, flows, datasets, runs, connector
  sources, document libraries, and drive items before using their IDs. Never
  invent an ID from a display name or URL.
- Prefer summary and list tools before raw definitions or large payloads.
- Keep list requests bounded. Follow pagination only as far as the user needs.
- Treat `403` as a permission problem and `404` as missing or inaccessible;
  report the distinction without claiming the target was deleted.

## Choose the narrowest workflow

- Fabric: inspect the workspace, then the item, pipeline, job, lakehouse, or
  semantic model involved. When you know an item's name but not its workspace,
  use `fabric_search_catalog`. Use `fabric_list_item_schedules` for when an item
  runs automatically and `fabric_list_job_instances` for past runs.
- Before writing a Fabric request body or editing a definition, check the exact
  shape offline with `fabric_get_api_doc` (operation, examples, or
  `definition_schema`). Topic names come from `fabric_list_api_docs`.
- Read any item's definition with `fabric_get_item_definition`. If it returns
  `status: Running`, check `fabric_get_operation_state`, then call it again with
  the `operation_id`. Its `definition_sha256` is not accepted by the notebook or
  pipeline guarded edit tools; use their own read tools for those.
- Power BI: resolve the dataset, report, or gateway before reading refreshes,
  data sources, status, or executing DAX.
- Power Automate: resolve the environment and flow before inspecting the
  definition, runs, actions, or one sanitized action error.
- For a new SharePoint, OneDrive, workbook, folder, or Office Script reference:
  resolve a SharePoint URL with `power_automate_resolve_sharepoint_site`, list
  its drives with `power_automate_list_document_libraries`, then browse or
  resolve the exact drive item. Use
  `power_automate_resolve_excel_script_action` for a verified Run script
  resource-parameter block. Merge it into `inputs.parameters` and preserve all
  `ScriptParameters/*` fields; do not create a temporary flow just to harvest
  picker IDs.
- Prefer `power_automate_summarize_flow_definition` before retrieving a raw
  flow definition.
- Use the canonical domain-prefixed tools. Compatibility aliases are disabled.

## Guard mutations

For notebooks, discover the Notebook item, then use
`fabric_get_notebook_definition` for the complete definition, decoded ipynb and
`definition_sha256`. Preview existing cell-source replacements with
`fabric_update_notebook_cells`, the hash as `expected_definition_sha256`, and
`cell_edits` containing zero-based `cell_index` and string `source`.
Use `fabric_apply_notebook_patch` for 1–100 sequential `cell_operations`:
`insert`, `update`, `remove`, or `move`. Indices follow preceding operations;
move destination is measured after removal. Insert and type changes support
`code` and `markdown`. Preview uses the same retrieval hash and returns counts,
ordered layout, changes and discarded fields. Populated incompatible outputs,
execution counts or attachments require explicit `discard_incompatible_fields=true`
on a type conversion. Existing metadata, tags, IDs and unrelated fields remain
intact. New cell IDs are deterministic. Local preview does not prove Fabric
service acceptance.
Only an authorized write uses `dry_run=false` and `confirm=true`.
Other cells, metadata, attachments and bindings remain intact. These tools
never execute code or change schedules. A conflict or unverified write requires
fresh retrieval and
review, never a blind retry. Hash prechecks are optimistic; avoid concurrent
editors because Fabric has no documented atomic conditional-write contract.
Even source retrieval requires notebook read/write permissions upstream.

For DataPipeline editing, use `fabric_get_pipeline_definition_full` to retrieve
all parts, decoded pipeline content and a drift hash. The older
`fabric_get_pipeline_definition` returns a summary and cannot round-trip edits.
Preview with `fabric_apply_pipeline_patch`, the retrieved hash as
`expected_definition_sha256`, and ordered add/remove/replace operations below
`/properties/`. Only an authorized apply uses `dry_run=false` and `confirm=true`.
Validation is structural, including nested dependency graphs; a successful
preview does not prove connection permissions or execution. The tool preserves
unrelated properties/parts and display metadata and never runs or schedules a
pipeline. Read/write permissions are required even for retrieval. Hash checks
and readback are optimistic; avoid concurrent editors and inspect unverified
outcomes before another edit. Copy Job items require a different workflow.

For pipeline and Copy Job lifecycle, discover targets and use
`fabric_get_pipeline` / `fabric_get_copy_job` for item metadata and
`metadata_sha256`. Creation accepts a complete InlineBase64 definition.
Preview `fabric_create_pipeline` / `fabric_create_copy_job`; only an authorized
apply supplies the preview's `create_request_sha256` as
`expected_create_request_sha256`, with `dry_run=false, confirm=true`.
Creation is not an upsert and does not execute or schedule.

Rename or update description through `fabric_update_pipeline_metadata` /
`fabric_update_copy_job_metadata` with the retrieved metadata hash.
Omitted fields remain unchanged; an empty description clears it.
For Copy Job editing, retrieve `fabric_get_copy_job_definition_full`, then
preview `fabric_apply_copy_job_patch` with its definition hash and 1-64
add/remove/replace operations below `/properties/` or `/activities/`.
Preserve other mappings, IDs, bindings and parts. Definitions and metadata
are edited separately.

Discover existing connections using `fabric_list_connections` /
`fabric_get_connection`. Results are metadata with non-secret credential
flags only. Visibility does not prove permission to bind, healthy credentials,
gateway availability or runtime success. Do not request token/password exports.

Preview `fabric_delete_pipeline` / `fabric_delete_copy_job` before deletion.
Save the returned recovery export locally, review scan coverage and blockers,
and obtain direct authorization for the exact target. Apply requires
`expected_deletion_preview_sha256` from that preview.
Active/unknown runs, enabled or disabled schedules, known incoming references
and incomplete checks block deletion. The default reference scan is the target
workspace; declared additional workspaces are bounded. Other workspace consumers
and external orchestrators remain unverified. No automatic cancellation,
schedule/dependency removal, connection/data deletion or permanent-delete fallback.
Recreation can require new IDs and reference repairs.

These tools share item locks, fresh optimistic hashes, one mutation submission,
bounded operation polling and independent readback. A matching candidate after a
lost create response does not establish attribution. Pending/unknown outcomes
are non-retryable until inspected; never resend automatically.

Treat a request as read-only unless the user explicitly asks for a state change
or write. Before any mutation:

1. Read the current target and record the expected identity and state.
2. Prefer `power_automate_apply_guarded_patch` for narrow changes under
   `/actions`; it reads the complete live definition and connection references
   itself. Use `power_automate_apply_guarded_update` only when the caller
   intentionally owns the complete definition or connection-reference map.
   Run either tool's dry-run path first.
3. State the exact target, intended change, and verification plan.
4. Obtain explicit approval for the concrete mutation in the current task.
5. Send the mutation once, then read the target again and report the observed
   state. Never retry an ambiguous or timed-out write until live state has been
   reconciled.

For `power_automate_create_flow` specifically:

- Validate the complete connector-free or connector-backed definition with the
  default dry-run before requesting approval for `dry_run=false`.
- Name the exact environment and new display name in the approval request.
- Creation always requests `Stopped`. Never enable, invoke, resubmit, or delete
  the created flow as part of creation.
- The POST is non-idempotent and must be sent exactly once. A timeout, 5xx,
  polling problem, or failed readback is ambiguous; do not retry creation.
- Independently read the returned flow ID and verify its stopped state,
  definition/trigger shape, and exact connection references.
- This tool deliberately uses the unsupported `api.flow.microsoft.com`
  compatibility backend. Do not add or silently use a Dataverse fallback.

Do not treat general permission to inspect Fabric as permission to run a
pipeline, update or toggle a flow, or resubmit a run.

## Report results

Lead with the answer or operational status. Include the target identity, the
evidence returned by the MCP, and the next safe action. Separate proven facts
from inferences and unknowns. Avoid returning raw definitions, connection
references, signed links, or other sensitive content unless the user needs that
specific material and the tool is designed to return it safely.

## Known boundaries

- A recurrence-triggered Power Automate flow cannot be forced to run on demand.
- `power_automate_resubmit_flow_run` replays an existing run; it does not invoke
  an arbitrary flow.
- `power_automate_create_flow` only creates a stopped flow from a complete
  definition; it does not enable or execute it.
- Raw TMDL and the alternate Power Platform API are opt-in capabilities.
- Graph-backed resource discovery is read-only and currently targets global
  Microsoft 365 SharePoint URLs. It resolves connector identifiers but does
  not execute Office Scripts or read workbook data.
- The bundled native executable requires no Python, Node, uv, dependency
  restoration, listener, or singleton. Azure CLI authentication is still
  required for tenant calls.
