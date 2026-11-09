# Product Wrangler

Product Wrangler is a small, framework-neutral, skills-only plugin for turning an
existing runnable web app into the product it should be.

It is intended for broad implementation requests such as:

```text
$product-wrangler wrangle this existing app into the product it should actually be

This app works, but it feels half-baked. Figure out what is wrong and fix it end to end.
```

It does not own greenfield application building, isolated UI fixes, review-only
critique, or backend-only work.

## Contract

Product Wrangler requires the agent to:

1. Inspect the dirty worktree, rollback boundary, runtime endpoints, data class,
   test accounts, and outbound effects before mutating browser flows.
2. Bound one primary product surface instead of expanding through the entire app.
3. Infer the product from a ranked evidence hierarchy and attempt to disprove the
   selected thesis.
4. Record contradictions, assumptions, confidence, non-goals, and evidence for
   every major product decision.
5. Create a workflow ledger that ties each primary user outcome to baseline
   behavior, an expected observable result, a selected change, post-fix evidence,
   and remaining uncertainty.
6. Replay the same journeys before and after, run a cold-start pass, revisit the
   thesis, and select COMPLETE, PARTIAL, or BLOCKED honestly.

The plugin does not add tools, hooks, MCP servers, framework dependencies, or
operational authority.

## Safety model

A local frontend may still point at production. Product Wrangler identifies
backend endpoints and external effects before testing. Mutating browser journeys
run only against fixtures, disposable accounts, isolated local data, or proven
sandbox services. Unknown or real-service-backed applications are inspected
read-only unless the exact side effect is authorized.

## Behavioral evaluations

`evals/evals.json` covers broad triggers, nearby non-triggers, conflicting product
evidence, generic redesign, dirty worktrees, real-service-backed apps, missing
browser or credentials, cosmetic-only iteration, scope growth, authority
expansion, and premature completion.

The release gate in `evals/README.md` requires real model runs. Manifest and
contract validation alone are not evidence that the skill makes sound product
judgments.

## Status

Available from the `mcook-plugins-local` marketplace. The initial release gate
included two-family matrix sweeps plus disposable, real-service read-only, and
large-application scope tests. See `evals/results/2026-09-04-v0.2.0.md`.
