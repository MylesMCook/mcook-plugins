# Research basis

Checked 2026-09-09 through three independent Luna research passes: architecture
and request handling; runtime, persistence, authentication, and deployment;
framework fit, upstream metadata, and the existing Hono Web Apps workflow.
The author cross-checked consequential findings against official pages.

These are design inputs for the plugin, not a version promise. One research
result reported an older release; direct inspection of the official
[v1.7.3 release](https://github.com/redwoodjs/sdk/releases/tag/v1.7.3) showed it
marked latest, dated September 3. Agents must still check the project's actual
version and current docs on future tasks.

## Findings that change the workflow

| Evidence | Plugin decision |
| --- | --- |
| The [overview](https://docs.rwsdk.com/core/overview) and [hosting guide](https://docs.rwsdk.com/core/hosting) center React, Vite, and Cloudflare Workers. | Prefer this workflow for Cloudflare React applications; retain Hono as an independent HTTP/API option and evaluate other hosting targets explicitly. |
| The [AI guide](https://docs.rwsdk.com/guides/build-with-ai) provides an index and full documentation file. | Read the live index and task-specific pages; use the full file selectively. Bundle no frozen starter or API manual. |
| [Routing](https://docs.rwsdk.com/core/routing) uses explicit composition and Web APIs. | Preserve route/middleware order and starter wiring; do not assume Next.js filesystem conventions or RedwoodJS generators. |
| [RSC docs](https://docs.rwsdk.com/core/react-server-components) separate server components, client components, data queries, mutations, and manual rendering. | Keep client boundaries small, verify mutation updates, and use the interactive router path for interactive pages. |
| The [migration guide](https://docs.rwsdk.com/migrating) changes peers, middleware action handling, and headers. Its auth migration discussion warns about moving live data from D1/Prisma to Durable Objects. | Check installed types; do not perform incidental upgrades or treat an auth storage change as a starter refresh. |
| The [security page](https://docs.rwsdk.com/core/security) shows an entrypoint example different from the `defineApp` pattern in the [worker reference](https://docs.rwsdk.com/reference/sdk-worker). | Live docs are essential but not infallible; verify exports and probe discrepancies before copying code. |
| [Core authentication](https://docs.rwsdk.com/core/authentication) and [experimental authentication](https://docs.rwsdk.com/experimental/authentication) are separate documentation tracks. | Distinguish session infrastructure, identity, and application authorization; do not silently adopt an experimental addon. |
| [Experimental database](https://docs.rwsdk.com/experimental/database) and [realtime](https://docs.rwsdk.com/experimental/realtime) have their own APIs and lifecycle. | Make stability, data recovery, and migration cost explicit before adoption; preserve existing storage. |
| The [Vitest guide](https://docs.rwsdk.com/guides/vitest) tests a built Worker and demonstrates an HTTP bridge to server actions. | Verify RSC in the runtime; keep the test bridge absent from production and separately test the real action boundary. |
| The frontend pages in the [docs index](https://docs.rwsdk.com/llms.txt) include Tailwind and component-library guides but no dedicated StyleX integration was found. | Preserve the user's StyleX preference and require a dev/production compiler probe rather than claiming an official adapter exists. |

The ownership, input-validation, test-bridge isolation, deployment authorization,
and rollback gates are this plugin's engineering recommendations. Do not read
them as claims that RedwoodSDK automatically supplies these guarantees.

## Upstream provenance

The authoritative implementation is [redwoodjs/sdk](https://github.com/redwoodjs/sdk).
The [tagged license](https://github.com/redwoodjs/sdk/blob/v1.7.3/LICENSE.md)
is MIT. This plugin's prose is an
original synthesis with source links; it does not vendor upstream code, images,
starter files, or documentation. Its own license is MIT, copyright Myles Cook.

## Behavioral review

Three Luna follow-up passes read the finished skill and references without the
evaluation answer table. They exercised decision paths for stale UI on an old
SDK, RedwoodJS Cells, RSC tests with a deploy-containing release script, Docker
fit, local StyleX work, Hono-only work, remote bindings during local startup,
and live auth storage. No blocking packaging or workflow defect was found.

The reviews prompted explicit SDK/RedwoodJS disambiguation, separation of
persisted data from refreshed UI state, and inspection of startup migrations
before using remote-capable bindings. These were read-only behavioral reviews,
not application execution or fresh installed-skill activation tests. No demo app
was built and no Cloudflare resource was created during plugin validation.
