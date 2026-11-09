---
name: hono-web-apps
description: >-
  Evaluate, create, modify, test, debug, and verify Hono web applications. Use when Hono is named or
  imported, including routes, middleware, validation, RPC, JSX, adapters, CLI, testing, deployment
  boundaries, UI architecture, or an explicit Hono evaluation. Do not trigger for Vue-only frontends,
  generic Node or browser work, or existing Express, Fastify, Next.js, Nuxt, or other apps unless Hono
  involvement or migration is explicit.
---

# Hono Web Apps

Identify the real requirement and dominant risk. Choose the smallest fitting design, make a local
reversible change, and test observable behavior. Keep necessary complexity behind stable boundaries.
Correctness, security, accessibility, data integrity, and explicit requirements still win.

## Establish repository truth

Before recommending or changing anything:

1. Read the nearest `AGENTS.md` files from the target directory toward the repository root.
2. Inspect status, manifests, workspaces, lockfiles, package-manager metadata, scripts, entry points,
   tests, TypeScript configuration, and deployment configuration.
3. Resolve installed versions and identify the active and pinned runtime, deployment target, platform
   bindings, frameworks, validators, test runner, and canonical commands.
4. Separate research or recommendation from approval to adopt, scaffold, install, migrate, or
   implement.

Preserve the existing framework and conventions unless migration is explicit. Hono may be the wrong
choice. Do not add Hono, `create-hono`, `@hono/cli`, Vue, htmx, Tailwind, validators, adapters, or
build tools merely because this skill is active.

## Choose the smallest fitting design

Apply this ladder only to approved greenfield Hono work:

1. Use Hono for HTTP, APIs, middleware, and server responsibilities.
2. Start small server-driven apps with Hono JSX or HTML, native forms, browser APIs, and plain CSS.
3. Consider htmx when server-returned fragments simplify interaction. Never require it beneath Vue.
4. Add Vue 3 with Vite only for meaningful client state, reusable interactive components, or
   multiple interactive views.
5. Add Tailwind only when the UI and build pipeline benefit.

Do not combine Vue and htmx without a demonstrated requirement and explicit ownership boundary.
Prefer one repository and same-origin deployment when practical. Keep domain and API logic independent
from presentation. For a same-repository TypeScript boundary, consider `hc` and exported `AppType`
before duplicating types or adding code generation; use plain `fetch` when it is clearer.

## Research in version-aware order

Stop when the answer is solid:

1. Installed versions, local source and types, repository instructions, and runtime configuration.
2. An already-configured Hono skill or optional `hono-docs` MCP; do not configure or bundle it.
3. Project-local `hono search`, then `hono docs`, when `@hono/cli` is installed and compatible.
4. Official Hono docs or its `llms.txt`, `llms-full.txt`, and `llms-small.txt` files.
5. Verify important findings against the installed Hono version and target runtime before editing.

`create-hono` and `@hono/cli` are separate tools. Do not use `@hono/mcp`; it builds MCP servers with
Hono and does not assist ordinary Hono application development.

## Create new projects deliberately

Use `create-hono` only after explicit approval:

1. Resolve the parent and target paths. Require a new target path and never scaffold over a repository.
2. Inspect current templates, flags, help, and package metadata.
3. Select the runtime template and package manager explicitly; use it and commit its lockfile.
4. Pin a currently supported Node version using the repository's convention and compatible `engines`.
5. Add the current compatible `@hono/cli` to `devDependencies`; never install it globally.
6. Inspect generated scripts and the runtime adapter before changing the app.

## Use the local CLI safely

In existing repositories, do not add `@hono/cli` just to conform. Before any `hono` command, confirm
the package and binary are local, verify the CLI's Node engine against active and pinned Node versions,
and invoke it through the repository's package manager. Use no-download mode when available. Before
`npx hono`, prove the local binary exists and abort rather than allowing an implicit install.

Use `hono search` and `hono docs` as aids. On failure, report it and fall back to configured tools or
official docs; never turn documentation failure into package installation.

Use `hono request` for representative safe GET and POST probes. First confirm an isolated test
configuration. Probe POST only when database, queue, email, billing, notification, and outbound
dependencies are mocked or safely sandboxed. If unsure, use committed tests. Check status, headers,
body, and content type. Keep secrets and customer data out of arguments and output. This probe uses
`app.request()`; it does not prove bindings, storage, queues, environment, networking, or deployment.

Use `hono serve` only as an ad hoc probe when no canonical development command exists; never replace
established scripts with it. Use `hono optimize` only for an explicit measured bundle-size objective
with regression tests; never add it to the standard build automatically.

## Make the smallest approved change

Preserve existing architecture, naming, validation, error, logging, and testing patterns. Keep
runtime-dependent code at the adapter boundary and handlers thin. Add a dependency only when needed.

Reuse the current validator when sound. Verify validation targets, content types, inferred types, and
error responses. For RPC, preserve chained route inference and compatible TypeScript settings. Export
the relevant `AppType`, but do not force `hc`, broad types, generated clients, or RPC over plain fetch.

## Verify stable boundaries

1. Run a safe project-local `hono request` probe when available.
2. Run committed `app.request()` tests for status, headers, and body; use `testClient` when its typed
   access adds coverage.
3. Run the repository's type checks, linting, builds, and tests.
4. Use runtime-native integration tests for bindings, databases, queues, caches, environment behavior,
   or adapter semantics.
5. Run the canonical runtime path. For meaningful Vue changes, exercise the browser, capture evidence,
   fix observed failures, and repeat.

Report only versions, targets, commands, routes, response properties, bindings, browsers, and operating
systems actually checked. One host does not establish Windows-and-macOS compatibility.
