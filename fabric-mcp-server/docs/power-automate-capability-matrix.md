# Power Automate capability matrix

| Surface | Capability | Write or invoke |
| --- | --- | --- |
| Existing compatibility adapter | Flow definition, disabled definition-based creation, guarded action patch and full update, state control, run diagnostics, and resubmit | Existing writes when read-only mode is off |
| Environment Power Platform API | Searchable connector names and tiers, action/trigger search, and exact operation parameters | Read-only metadata; no connection or connector invocation |
| Power Platform API | Cloud-flow, run, and action inventory; opt-in after `PowerAutomate.Flows.Read` auth | Read only |
| Local classifier | Trigger-shape description | Never executable |
| Microsoft Graph resource resolver | SharePoint connector sources, document libraries, drive items, workbook IDs, folder IDs/paths, and Office Script IDs | Read only |
| Optional Dataverse | Category-5 workflow metadata and ETags | Read only |

The connector catalog uses the existing Flow token and environment ID. It does
not require Dataverse, enumerate connections, call dynamic resolvers, or expose
a generic connector invocation tool. Connector and operation results are
filtered and bounded locally because the upstream catalog can ignore `$top`;
paging reports the matched total, returned count, and truncation state.

The optional Dataverse surface is disabled unless its validated Web API URL is
configured. No surface claims solution membership, executes callbacks, or adds
a generic backend router.

The server never silently falls through from one backend to another. Tool names
identify the backend contract directly.

For connector-backed actions, resolve the current resource chain instead of
copying values from a temporary designer action:

1. Use `power_automate_list_connectors` or
   `power_automate_search_connector_operations` to discover the connector and
   operation.
2. Use `power_automate_get_connector_operation` for exact parameter names,
   required flags, enums, defaults, dynamic-input markers, and Microsoft's
   exact workflow `operationType`.

For resource identifiers required by those parameters, use the Graph-backed
resolution chain:

1. `power_automate_resolve_sharepoint_site`
2. `power_automate_list_document_libraries`
3. `power_automate_list_drive_items` or `power_automate_resolve_drive_item`
4. `power_automate_resolve_excel_script_action` for `RunScriptProd` or
   `RunScriptProdV2`

The Excel resolver verifies that each drive belongs to its declared connector
source, resolves both files live, checks the workbook and `.osts` types, and
returns the exact resource fields plus optional metadata entries. Merge those
fields into `inputs.parameters`; do not replace `ScriptParameters/*` or other
action-specific arguments. The resolver does not run the script or read
workbook contents.

Use `power_automate_apply_guarded_patch` for narrow changes under `/actions`;
it derives the complete definition from a fresh snapshot and preserves the live
connection-reference map. Use `power_automate_apply_guarded_update` when the
caller intentionally owns the complete definition or connection-reference
map. The raw update
tool remains for compatibility and now refuses destructive supplied
connection-reference changes, but it does not provide the guarded tool's fresh
definition/state drift checks, stop/readback/restore sequence, or dry-run
summary.

Use `power_automate_create_flow` only after an explicit approved mutation plan.
It defaults to dry-run, always requests and verifies `Stopped`, sends exactly
one POST without retry, and never enables, invokes, resubmits, deletes, or
falls back to Dataverse.
