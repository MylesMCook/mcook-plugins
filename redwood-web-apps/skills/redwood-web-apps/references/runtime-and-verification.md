# Runtime, data, and verification

Read the relevant current docs from [the docs map](docs-map.md). Choose services
for a demonstrated requirement, not because they appear in an upstream example.

## Workers and bindings

Inspect the generated Vite and Wrangler configuration before changing it.
Establish the Worker entrypoint, compatibility date/flags, environment selector,
binding names, and generated types. Verify Node API and package compatibility
with workerd; a dependency working under the local Node executable is insufficient.

Keep secret values in the project's existing local/remote secret mechanism;
inspect key names without printing values. Do not move server secrets into
`VITE_` variables, client imports, or serialized props. Regenerate binding types
with the repository's supported command after configuration changes.

Local runtime emulation is not always isolated: inspect remote bindings, service
bindings, database URLs, and outbound API clients before starting the app, tests,
or migrations. Check environment overlays, `remote: true`, `--remote`, and startup
initialization/migration code as well as the release script. Prove the resource
target before running a startup path that can migrate or seed it; use an isolated
local configuration when the existing one reaches remote state.
Use local/test resources and fixtures; prevent email, billing, queue, or webhook
side effects unless those targets and effects are explicitly authorized.

## Persistence and authentication

Preserve an existing database, ORM, and authentication provider. Select D1, R2,
Durable Objects, or an external database according to query, consistency,
concurrency, and access needs. Keep binding access server-side. Verify read/write
and persistence through the same runtime used by the app.

Core session primitives and experimental auth/passkey addons are different
choices. Inspect addon version compatibility and generated files before applying
one. Existing user/session storage is not disposable scaffolding. Do not replace
D1/Prisma or an auth provider merely because a newer starter uses Durable Objects.

For a schema or storage migration, identify the exact environment and resource,
existing data, migration order, backup/restore route, and application rollback
compatibility. Test against isolated data before an authorized remote migration.
Cloudflare resource migrations and SQL schema migrations are separate concerns.

## Tests and debugging

Use the repository's test setup first. The RedwoodSDK Vitest guide covers
testing against the built Worker so RSC transforms are present. Verify a matching
Workers Pool configuration instead of copying a frozen Vite test snippet.
If using the guide's `/_test` bridge, keep its action dispatch and test utilities
exclusive to the isolated test environment. Verify the production artifact does
not expose the bridge; do not ship it as a public endpoint. A bridge test does
not replace testing the real action's authentication and protocol path.

Use pure unit tests for domain logic, Workers-runtime integration tests for
bindings and request behavior, and browser tests for hydration/actions/navigation.
A mocked binding proves the mock contract, not deployed persistence or permissions.

For queue/cron work, pass required data explicitly: HTTP request context is not
available in these handlers. Test retries/idempotency and the platform event
separately; a local web request does not prove a deployed scheduled trigger.

For runtime bugs, reproduce through the canonical dev/preview command, inspect
browser and Worker errors, and narrow the failing boundary. A production build
check should catch bundling and server/client import problems; a browser check
must still prove interaction and resulting state. Do not bypass SSR or disable
security controls simply to suppress an unexplained error.

## Release

Read `release`, deploy, generation, and migration scripts before running them.
Confirm account, Worker name, environment, routes/domain exposure, secrets by
name, and binding targets. Select the environment using the installed tooling's
documented mechanism; do not assume Vite mode selects the Wrangler environment.

Prepare the build and rollback before requesting any missing remote authority.
Do not provision resources, migrate remote data, deploy publicly, or alter DNS
as a side effect of a local build request. Respect authorization already given.

After an authorized release, check the deployed URL and affected authenticated
workflow, writes/readback if in scope, resource bindings, and immediate logs.
Report unavailable verification explicitly. Do not equate upload success with
application health or a code rollback with reversal of a data migration.
