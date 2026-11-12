# Architecture Decisions

Load this when the task is mainly about layering, deployment boundaries, service splits, eventing, concurrency, dependencies, state, or high-level tradeoffs.

Extended guidance on structuring systems without spending complexity before the problem has earned it.

## The Complexity Budget

Every system has an implicit complexity budget. Each architectural choice spends from it or earns some back. When the budget is exhausted, every change becomes harder, bugs take longer to localize, and onboarding slows down.

Before adding a service, framework, layer, workflow engine, cache, or new build step, ask: what concrete problem does this solve now, and what complexity does it add forever?

## Monolith First

Default to a monolith or the coarsest deployable boundary that fits the known problem. Fewer network boundaries usually means fewer operational failure modes, simpler local development, and faster debugging.

A monolith is a deployment choice, not an excuse for bad internal structure. Keep module boundaries clear so later extraction remains possible if the need becomes real.

Split only when there is a proven operational, organizational, isolation, scaling, or regulatory reason.

## Events Are Not Free Decoupling

Event-driven designs add ordering questions, replay concerns, idempotency work, delivery semantics, and debugging cost.

Use events when they buy something real:

- independent consumers
- fan-out to multiple downstream reactions
- temporal decoupling that matters
- durable asynchronous workflows that should survive retries and restarts

Do not introduce events mainly to avoid a direct call inside one product flow. That usually trades visible coupling for harder-to-debug coupling.

## Different Layers, Different Abstractions

Each layer should operate at a different level of abstraction. If two adjacent layers have nearly the same interface, one of them is probably not earning its existence.

Good layering example:

- **HTTP layer:** request, validation, response
- **Domain layer:** business rules and workflows
- **Data layer:** persistence and storage concerns

Bad layering: a service layer that only forwards calls between controller and repository.

## Pass-Through Variables Signal Boundary Problems

When a value must be threaded through several layers because only a deep layer needs it, the intermediate layers pay cognitive cost without gaining responsibility.

Good first fixes:

- move the responsibility closer to where the value matters
- use a request or execution context object when several pieces of metadata genuinely travel together
- use ambient or thread-local state only with explicit awareness of the tradeoffs

Repeated pass-through variables usually mean the boundaries are wrong.

## Choosing Between Approaches

Once correctness, security, data integrity, and regulatory constraints are satisfied, compare options in this order:

1. **Implementation simplicity:** easier to build, deploy, debug, and change
2. **Common-case fitness:** better fit for the scenarios that actually matter
3. **Consistency with the existing system:** less conceptual friction for the team
4. **Completeness:** support for the full theoretical case space

For internal design work, completeness usually comes last because it is expensive to guess and often easy to add later.

## Concurrency and Distribution Are Complexity Multipliers

Shared mutable state creates races. Network boundaries create partial failure, retries, timeouts, and consistency problems.

Default to the simplest model that works:

- stateless request handlers where possible
- simple job queues with independent workers
- optimistic concurrency when the domain tolerates it
- sequential processing when throughput still meets the need

Avoid threads sharing mutable state unless there is a clear reason. Avoid distributed transactions unless the constraints genuinely demand them.

## Framework and Dependency Selection

Every dependency is a liability. It can break, change direction, become unmaintained, or impose security and upgrade work you do not control.

Before adding one, ask:

- can the standard library or existing stack solve this well enough?
- how much of the dependency will we really use?
- is it understandable and maintained enough to trust?
- if it goes bad, can we replace it without surgery across the codebase?

For frameworks especially: a framework is a decision to structure part of your application around somebody else’s opinions. Prefer libraries over frameworks when the problem does not require global structure.

## State Management

System difficulty is often proportional to the amount of mutable state and how widely it is shared.

Prefer:

- computed values over stored values when recomputation is cheap
- immutable data when it makes reasoning easier
- one clear source of truth over duplicated state
- durable storage as source of truth over caches unless measurements justify the cache

Caches, derived state, and synchronization code all multiply complexity.

## When the System Grows

As systems grow, the same rules matter more, not less.

- **Deep modules** keep local understanding possible.
- **Consistent conventions** compress cognitive load.
- **Aggressive deletion** prevents dead options and stale code from accumulating.
- **Resistance to the second system** prevents over-general rebuilding that outgrows the real problem.

## Documentation as Architecture

Comments and design notes matter when they capture things code alone cannot express:

- why a decision was made
- what alternatives were rejected
- what constraints are non-obvious

Write these notes at module or boundary level. A short note about responsibility and tradeoffs is usually more valuable than many comments paraphrasing syntax.

## Organize by Knowledge, Not by Time

Avoid decomposing modules purely by execution order.

Bad: one module for step 1, one for step 2, one for step 3.

Better: one module for file-format knowledge, one for domain rules, one for persistence.

Group by owned knowledge, not by temporal sequence.

## Design for Reversibility

Significant changes should be reversible or at least recoverable. Rollbacks, staged migrations, feature flags, deprecations, and backward-compatible API changes all lower the cost of mistakes.

Lower-cost mistakes make it easier to ship simpler solutions and refine them incrementally.

## Keep the Feedback Loop Fast

Fast feedback encourages small changes, experimentation, and correction. Slow feedback encourages batching, fear, and speculation.

Invest disproportionate effort in keeping these fast:

- local development setup
- the common test suite
- build times
- deployment pipelines

Fast feedback is a simplicity tool, not just a productivity tool.
