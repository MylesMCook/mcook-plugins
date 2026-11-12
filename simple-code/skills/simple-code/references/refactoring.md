# Refactoring and Code Evolution

Load this when changing existing code, shrinking systems, planning incremental migration, or touching messy legacy areas that still need to keep working.

Extended guidance on changing code safely and incrementally without turning cleanup into a second system project.

## Chesterton’s Fence

Before removing or rewriting something, understand why it exists.

Code that looks ugly or redundant may be handling an edge case, preserving behavior for a dependency quirk, or embodying a requirement that exists nowhere else.

If you do not understand why a piece of code exists, you do not yet have permission to remove it.

## Small Refactors, Always Working

Large refactors fail at a disproportionate rate. They are harder to review, harder to debug, and harder to roll back.

Keep refactors small enough that:

- the system works at every intermediate step
- each step can be reviewed on its own
- the cause of a regression is relatively obvious
- you can stop at any point and still ship

If you have been refactoring for days and the system is not back to green, the step size was too large.

## When to Refactor

Refactor when:

- the next feature is harder to add than it should be
- a stable cut point has become obvious
- duplication has repeated enough times that it is now real shared behavior
- a noisy layer or pass-through abstraction is hiding the real shape of the system

Do not refactor when:

- code is ugly but stable and nobody needs to change it
- the structure is still in flux and the right seam has not emerged
- the cleanup is merely aesthetic and does not unlock real work

Speculative refactoring is still speculation.

## Strategic vs. Tactical Programming

Tactical programming optimizes for finishing the present task quickly. Strategic programming spends a modest amount of effort preserving clarity so the next task is cheaper.

The point is not gold plating. The point is to avoid borrowing speed today at a higher interest rate tomorrow.

## The Tactical Tornado

Watch for the instinct that produces code quickly while leaving behind structural damage.

Speed of writing code is rarely the bottleneck. Speed of understanding it usually is.

## Delete Before You Rearrange

The best refactoring often removes code instead of reorganizing it.

Before extracting, generalizing, or re-platforming, ask:

- can this feature be removed?
- can this option become a sensible default?
- can this layer be inlined?
- can this branch or special case disappear entirely?

Code that does not exist has no bugs, no maintenance cost, and no cognitive load.

## Incremental Evolution Over Revolution

Do not plan a big rewrite unless the current system is truly beyond incremental repair.

Big rewrites fail for predictable reasons:

- feature parity takes longer than expected
- the old system keeps changing while the new one catches up
- edge-case knowledge embedded in the old code gets lost
- teams go a long time without shipping visible progress

Prefer this pattern:

1. identify the worst pain point
2. introduce or clarify a boundary around it
3. replace or simplify behind that boundary
4. repeat

This is the core of incremental replacement patterns such as the Strangler Fig approach.

## Test the Behavior You Intend to Preserve

Before refactoring, make sure you have tests that verify the behavior that must stay true. Favor observable behavior over internal implementation details.

If the right tests do not exist, writing them first is often the safest move.

After each step, run the tests. If failures are hard to interpret, the step was probably too large or the tests are too coupled to internals.

## Manage Legacy Code Locally

Legacy code that is stable and rarely touched is often best left alone. The risk of cleanup can outweigh the benefit.

Focus simplification where the system is actively changing. That is where complexity extracts ongoing cost.

When you must touch legacy code, apply the Boy Scout Rule locally: leave the area you touched a little better than you found it without wandering into unrelated cleanup that makes the change harder to review.
