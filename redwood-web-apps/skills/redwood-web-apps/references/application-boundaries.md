# Application boundaries

Read the current routing, RSC, client, and error docs linked in
[the docs map](docs-map.md) before applying version-dependent names below.

## Routes and rendering

Keep route order intentional: global middleware, prefixes, interrupters, render
wrappers, and error handlers have different scopes. Verify early-return behavior
and method handling. Do not assume HEAD automatically uses GET; inspect support
for OPTIONS, 405, and the required Allow header for affected routes.

Preserve the document shell, asset imports, and client initialization from the
working starter. Verify direct loads as well as client transitions. Avoid manual
HTML rendering helpers for interactive routes: the RSC docs distinguish their
output from the protocol negotiation used by the normal router render path.

Client navigation is an optional enhancement. Check the installed initialization
contract, hydration callbacks, history, redirects, pending UI, and prefetch
semantics before enabling it. Do not add another router or a global query cache
just to reproduce server-rendered data already available in the page.

## Server operations

For each read or mutation, identify its input, session identity, authorization,
data boundary, response, and UI update. Use runtime validation, not TypeScript
casts, for FormData, URL parameters, and serialized action arguments. Never use
a client-supplied user ID as proof of ownership.

Check the installed behavior of ordinary server functions versus `serverQuery`
and `serverAction` before choosing a wrapper. Data-only results, whole-tree
updates, redirects, and headers are distinct contracts. Do not manually forge
internal RSC headers/protocol calls to save a small helper.

Handle pending submissions, errors, and successful completion visibly. Verify
duplicate-submit behavior where it matters. Test progressive enhancement when
required; React-looking form syntax alone does not prove no-JavaScript support.
For a stale view after saving, distinguish persisted data from refreshed RSC
output and client-owned state before changing the action or adding a cache.

Place authorization at the operation, even when route interrupters also protect
the page. Test a direct call without a session and with another user's resource
ID. Avoid mutable global request context and shared caches containing private
user data. A function running on the server is not automatically safe to expose.

## Errors and headers

Check the installed `except`/error response contract and handler scope. Preserve
intentional HTTP status codes and redirects; do not turn every error into a 200
HTML page or every validation failure into 500. Verify page, API, and action
failures separately, including failures during streaming when relevant.

Return a useful public message and keep internal error details in appropriate
server logs. Inspect cookie/header merging and CSP nonce propagation through
normal responses, denied requests, redirects, and action responses. Do not copy
old context-header accessors from an incompatible release.
