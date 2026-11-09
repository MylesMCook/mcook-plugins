# Current documentation map

Start with [llms.txt](https://docs.rwsdk.com/llms.txt) on each new task involving
framework behavior. Follow its current links if this map drifts. These pointers
were checked on 2026-09-09; they are not a pinned API contract.

| Task | Read and establish |
| --- | --- |
| Fit and new app | [Overview](https://docs.rwsdk.com/core/overview), [quick start](https://docs.rwsdk.com/getting-started/quick-start), [create-rwsdk](https://docs.rwsdk.com/reference/create-rwsdk): supported target, starter, flags, generated scripts |
| Routes and middleware | [Routing](https://docs.rwsdk.com/core/routing), [router reference](https://docs.rwsdk.com/reference/sdk-router), [worker reference](https://docs.rwsdk.com/reference/sdk-worker): order, context, methods, action handling |
| Rendering and mutations | [RSC](https://docs.rwsdk.com/core/react-server-components), [documents](https://docs.rwsdk.com/guides/frontend/documents), [error handling](https://docs.rwsdk.com/guides/frontend/error-handling): server/client boundary, response behavior, hydration |
| Navigation | [Client navigation](https://docs.rwsdk.com/guides/frontend/client-side-nav), [client reference](https://docs.rwsdk.com/reference/sdk-client): stability, initialization, pending UI, redirects/history |
| Authentication | [Core authentication](https://docs.rwsdk.com/core/authentication), [security](https://docs.rwsdk.com/core/security), [experimental authentication](https://docs.rwsdk.com/experimental/authentication): distinguish sessions, identity, authorization, and optional addons |
| Data and configuration | [Environment variables](https://docs.rwsdk.com/core/env-vars), [storage](https://docs.rwsdk.com/core/storage), [Drizzle](https://docs.rwsdk.com/guides/database/drizzle): bindings, secrets, data model, migration commands |
| Optional platform features | [Queues](https://docs.rwsdk.com/core/queues), [cron](https://docs.rwsdk.com/core/cron), [email](https://docs.rwsdk.com/core/email): lifecycle and side effects |
| Experimental features | [Database](https://docs.rwsdk.com/experimental/database), [realtime](https://docs.rwsdk.com/experimental/realtime): current stability and migration cost; do not mix with [legacy realtime](https://docs.rwsdk.com/legacy/realtime) |
| Tests and release | [Vitest](https://docs.rwsdk.com/guides/vitest), [debugging](https://docs.rwsdk.com/guides/debugging), [troubleshooting](https://docs.rwsdk.com/guides/troubleshooting), [hosting](https://docs.rwsdk.com/core/hosting): compatible setup, local/runtime/deployed evidence |
| Upgrades | [Migration guide](https://docs.rwsdk.com/migrating), [releases](https://github.com/redwoodjs/sdk/releases), [source](https://github.com/redwoodjs/sdk): installed-to-target changes and peer requirements |

The official [AI guide](https://docs.rwsdk.com/guides/build-with-ai) describes
[llms-full.txt](https://docs.rwsdk.com/llms-full.txt). Prefer focused pages over
loading the full manual on routine edits. When a link fails, rediscover it from
the index or official repository rather than guessing a path.

If a guide conflicts with code, inspect the installed package's exports,
declarations, and relevant implementation; then check the corresponding release
tag. `main`, `latest`, a search snippet, and a migration guide are not proof of
the installed API. Record the discrepancy and use a narrow compile/runtime probe
where behavior is uncertain.

Consult [Cloudflare Workers docs](https://developers.cloudflare.com/workers/)
for runtime/binding behavior and [React docs](https://react.dev/reference/rsc/server-components)
for React boundaries. Use official StyleX documentation and the actual compiler
package for styling integration. Do not add a documentation MCP or download an
upstream agent skill merely to read these pages.
