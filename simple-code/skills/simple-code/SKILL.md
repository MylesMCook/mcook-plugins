---
name: simple-code
description: Reduce incidental complexity in code and design. Use when shaping APIs, module boundaries, refactors, tests, naming, logging, and architecture tradeoffs, or when asked to simplify code or judge whether an abstraction, dependency, layer, or service earns its cost. Biases toward concrete, local, reversible solutions. Not for pure bug hunts, formatting, or style-only edits.
---

# Simple Code

Use this skill when simplicity and maintainability are the main design pressure.

## Workflow

1. Identify the real requirement, dominant risks, and which concern should lead the decision. Read the existing code, callers, and tests before proposing changes.
2. Recommend the simplest design that satisfies the requirement now. Name one option; mention an alternative only when it is a close call.
3. Prefer local, concrete, reversible changes over speculative abstractions. Delete before you rearrange.
4. Pull unavoidable complexity behind the simplest stable boundary you can.
5. Test at stable boundaries rather than mirroring internals.
6. State what complexity the recommendation adds or removes, and what would justify revisiting it.

## Load a reference when

- Functions, classes, public APIs, parameters, or module boundaries: `references/api-design.md`.
- Layering, service splits, events, concurrency, dependencies, or state: `references/architecture.md`.
- Changing existing code, incremental migration, or legacy areas: `references/refactoring.md`.
- Deciding how strongly to apply a principle: `references/provenance.md`.

## Core defaults

- **Locality of behavior.** Keep the behavior of a unit visible where the unit is defined. Prefer a little duplication or an inline helper over indirection that sends a reader across files to understand one flow.
- **Names.** A name should say what something is or does in domain terms. If it needs a comment to explain the basics, rename it or reshape it.
- **Tests.** Assert observable behavior through public boundaries. Avoid mocks of internals and tests that break on every refactor. Write the missing behavior test before a risky change.
- **Logging.** Log at boundaries and decision points, not every line. Use structured fields and a request or correlation ID so one flow can be traced across components. Never log secrets or personal data.
- **Types.** Use types to make misuse hard. Treat advanced type machinery in ordinary application code as a cost that must justify itself.

## Guardrails

- Do not simplify away correctness, security, privacy, accessibility, data integrity, or explicit product requirements.
- Treat added abstraction, dependencies, layers, and services as costs that must justify themselves.
- Do not remove code until you understand why it exists.
- Do not widen a change into unrelated cleanup.
