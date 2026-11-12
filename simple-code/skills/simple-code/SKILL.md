---
name: simple-code
description: Reduce incidental complexity in code and design. Use when shaping APIs, module boundaries, refactors, tests, naming, and architecture tradeoffs with a bias toward concrete, local, reversible solutions.
---

# Simple Code

Use this skill when simplicity and maintainability are the main design pressure.

## Workflow

1. Identify the real requirement, dominant risks, and which concern should lead the decision.
2. Recommend the simplest design that satisfies the requirement now.
3. Prefer local, concrete, reversible changes over speculative abstractions.
4. Pull unavoidable complexity behind the simplest stable boundary you can.
5. Test at stable boundaries rather than mirroring internals.

## References

- `references/api-design.md`
- `references/architecture.md`
- `references/refactoring.md`
- `references/provenance.md`

## Guardrails

- Do not simplify away correctness, security, accessibility, or explicit product requirements.
- Treat added abstraction as a cost that must justify itself.
