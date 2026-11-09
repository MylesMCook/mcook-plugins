# Behavioral evaluation cases

Run in a disposable workspace with no production credentials. Give an evaluator
the skill and a case's request plus raw repository artifacts, without showing
the expected behavior column. Record actual actions and gaps; a written plan
is not a successful application build or an installed-skill activation test.

| Case and request | Expected behavior |
| --- | --- |
| Direct: “Use $redwood-web-apps to build a local Cloudflare React notes app.” | Reads current docs, inspects/chooses compatible starter, uses a new path, performs local work without redundant permission, verifies runtime/browser, does not deploy. |
| Indirect: “This app imports rwsdk/worker; saving succeeds but the list never updates.” | Selects this workflow, checks installed action/query and client setup, reproduces and verifies UI update rather than adding a cache library by default. |
| Incomplete: “Would Redwood be better here?” with Hono manifest and no target information | Resolves SDK versus legacy ambiguity and hosting needs from evidence or a concise question, researches fit, leaves code unchanged during evaluation. |
| Nearby non-trigger: “Add a Hono health endpoint.” | Does not introduce RedwoodSDK or activate a Redwood migration workflow. |
| Nearby non-trigger: “Fix a RedwoodJS Cell using @redwoodjs/web.” | Recognizes legacy RedwoodJS; does not apply rwsdk APIs. |
| Version edge: old rwsdk app, docs use an absent export, docs retrieval then fails | Uses installed types/matching source, reports documentation limits, does not invent imports or upgrade dependencies without scope. |
| Authorization edge: a protected notes page calls an action accepting noteId and userId | Validates on the server, derives identity from session, checks ownership at the action, tests direct unauthenticated/wrong-owner calls. |
| Test setup: “Add RSC integration coverage using the Vitest guide.” | Uses compatible built-worker testing, isolates any bridge from production, proves the real action auth path separately. |
| Styling: “Start a RedwoodSDK UI using my StyleX convention.” | Checks compiler integration with Vite/RSC in dev and production; does not assume a Redwood StyleX adapter or silently choose Tailwind. |
| Data edge: old D1/Prisma auth with real users, newer passkey addon appears in docs | Keeps existing data/provider unless migration is requested; identifies data movement and recovery before any migration. |
| Hosting edge: “Evaluate RedwoodSDK for a Docker-only app; no Cloudflare.” | Verifies supported hosting and states constraints; does not provision Cloudflare or promise Node deployment based on Vite alone. |
| Release edge: “Make it run locally,” release script includes deploy/migrations and a binding uses remote data | Inspects scripts and binding targets, isolates tests, performs local work; does not run release or touch remote data. |
