# Power Automate Bridge

Power Automate is a first-class domain in this server. Its tools use:

- base URL: `https://api.flow.microsoft.com/providers/Microsoft.ProcessSimple`
- API version: `2016-11-01`
- Azure CLI scope: `https://service.flow.microsoft.com/.default`

Microsoft documents `api.flow.microsoft.com` as unsupported and recommends the
Dataverse Web API for flows on the Solutions tab. That replacement does not
cover every flow this server must manage: Microsoft also documents that flows
under My Flows are not currently supported with code. Do not remove or gate the
bridge solely because of the support label.

## Stable MCP Boundary

Keep the MCP tool names, parameters, and result envelopes stable. Isolate any
upstream response changes in `rust-server/src/clients/power_automate.rs`.

If the upstream API changes:

1. Reproduce the failure with the smallest read-only client operation.
2. Record the failing endpoint shape, status, and sanitized response structure.
3. Compare list, detail, run, update, and resubmit behavior separately.
4. Update the client adapter and its fixtures without reshaping MCP tools.
5. Run the Power Automate client tests and full server contract suite.
6. Perform one bounded live read before testing an approved disposable write.

## Primary local path and optional supported inventory

The existing `power_automate_*` bridge remains active. It is not hidden behind
legacy modes. It is the primary local path for flow inventory, definitions, run
history, action diagnostics, creation, updates, and resubmission. It uses the user's
existing Azure CLI session and does not require a new Entra app registration.

`power_automate_create_flow` is the canonical native creation path. It validates
the complete workflow definition, trigger/action structure, runAfter graph,
required parameters, connector `connectionName` usage, and exact
connection-reference coverage before any request. Connector-free definitions
may use `{}`. Dry-run is the default and returns the normalized request and
hashes without authenticating. A live call requires explicit mutation approval,
always requests `state=Stopped`, and sends exactly one POST with no automatic
retry. The returned flow ID is read back and verified for display name, state,
definition, trigger shape, and exact connection references. Ambiguous or
mismatched outcomes are reported without enabling or deleting the flow.

Creation does not use Dataverse and has no Dataverse fallback. The compatibility
backend is explicit rather than silently substituted for a supported surface.

For flow-definition writes, prefer `power_automate_apply_guarded_update`. It
requires a fresh definition hash, exact connection-reference keys, and exact
state; validates connector-backed triggers and actions; refuses silent
connection-reference removal; supports dry-run; stops a Started flow when
requested; sends one update; verifies definition, trigger, connection-key, and
state hashes; and restarts only after successful readback. Activation is never
retried automatically. If its response is missing or unsuccessful, the tool
uses one fresh bounded readback: `Started` proves restoration, while `Stopped`
returns the verified definition update, actual final state, failed phase, and
the single safe recovery action without suggesting another definition write.
The raw
`power_automate_update_flow` tool remains available for contract compatibility.

For a narrow change under the workflow definition's `/actions` object, prefer
`power_automate_apply_guarded_patch`. It accepts one to 64 ordered RFC 6902
`add`, `remove`, or `replace` operations, reads the live definition and
connection references itself, applies the patch in memory, and then reuses the
same guarded full-update lifecycle. JSON Pointer `~0` and `~1` escaping and
array indices are supported. Other definition roots and other patch operations
are rejected before mutation. Dry run returns only the changed paths,
validation summary, and before/target hashes; it does not return the derived
complete definition.

`power_automate_turn_off_flow` and `power_automate_turn_on_flow` read current
state, perform at most one state mutation, and verify final state. A no-op is
reported when the target state is already present.

`power_automate_describe_flow_run_support` retrieves the target flow, classifies
its actual trigger, and always reports `executable=false`. Power Automate does
not expose a supported operation for forcing a recurrence schedule to run on
demand. The old `power_automate_run_flow` stub was removed because it labeled
every trigger as Power Apps V2 without inspecting the flow.

Existing bridge writes remain available when read-only mode is disabled. They
are never automatically retried because the upstream operations are not
idempotent, and the adapter does not claim ETag-based concurrency protection.
Resubmission resolves the trigger name with a read-only run lookup, then sends
exactly one POST to the trigger-history resubmit path. It must not probe one
write path and retry through another after an unsuccessful or ambiguous result.

The additive inventory tools use the supported Power Platform API at
`https://api.powerplatform.com` with API version `2024-10-01`. Each inventory
call deliberately returns one upstream response page only. A `404` means the
environment has no Dataverse database and is returned as an explicit
Dataverse-unavailable diagnostic.

These optional alternate inventory tools are hidden unless
`FABRIC_MCP_ENABLE_POWER_PLATFORM_API=true`. Microsoft requires a compatible
tenant-approved client registration with delegated `PowerAutomate.Flows.Read`
(or service-principal RBAC). If tenant consent is unavailable, leave this
backend disabled and use `power_automate_list_flows`,
`power_automate_list_flow_runs`, and the other primary management tools. The
supported inventory API is not required for daily local management.

Flow-run listings and general action diagnostics return status, timing, and
error codes only. They deliberately omit signed content links, raw inputs, raw
outputs, and upstream error messages. The targeted
`power_automate_get_flow_run_action_error` tool returns one sanitized and
truncated error message while excluding headers, payloads, URLs, connection
IDs, and credentials.

`describe_capabilities` identifies the management backend and upstream support
status explicitly. It also reports package version, Git revision and dirty
status when running from a checkout, process start time, and the backend
contract version so a stale runtime can be distinguished from current source.

`power_automate_describe_flow_invocation` is a local classifier. It reports a
trigger shape and always reports `executable=false`; it never attempts an
invocation.

`power_automate_list_connectors`,
`power_automate_search_connector_operations`, and
`power_automate_get_connector_operation` expose read-only authoring metadata
through the environment-scoped Power Platform API. They use the existing Flow
token and environment ID, return bounded normalized metadata, and do not
require Dataverse, enumerate connections, run dynamic resolvers, or invoke a
connector operation. Operation search is an upstream POST but is treated as a
non-retried metadata read. Local filtering and truncation enforce the requested
connector, kind, deprecation, search, and limit contracts even when the
upstream API returns more data; list responses include honest paging metadata.

Optional Dataverse workflow metadata tools require
`FABRIC_MCP_DATAVERSE_WEB_API_URL`. It must be the trusted, canonical HTTPS
Web API URL ending exactly in `/api/data/v9.2`. The tools read category-5
workflow metadata with a fixed `$select`; they do not return `clientdata`, a
flow definition, or any proof of solution membership.

The optional Dataverse path is a capability expansion, not a silent replacement
for non-solution flows.

The native server keeps Power Automate in the same process as Fabric and Power
BI. One runtime owns the shared auth provider, HTTP client, and lifecycle; the
portable stdio path creates no listener, scheduled task, or child server.

References: [Manage flows with code](https://learn.microsoft.com/power-automate/manage-flows-with-code),
[List cloud flows](https://learn.microsoft.com/rest/api/power-platform/powerautomate/cloud-flows/list-cloud-flows),
[Dataverse conditional operations](https://learn.microsoft.com/power-apps/developer/data-platform/webapi/perform-conditional-operations),
and the [Rust MCP SDK](https://github.com/modelcontextprotocol/rust-sdk).
