---
name: pstack
description: >-
  Route non-trivial Codex work through rigorous engineering principles, compact playbooks, and concrete verification.
---

# Pstack

Use for non-trivial engineering work when speed should come from depth, not from spraying code. Start with the principle that changes earn their place.

## Principles Index

Read the relevant principle before acting:

- Subtract before you add: delete scope, wrappers, or options that are not earning their place.
- Boundary discipline: put guards at edges, keep internal flows typed and direct.
- Type-system discipline: make invalid states hard to express.
- Outcome-oriented execution: optimize for the result the user needs, not process residue.
- Prove it works: verify against the real surface.
- Fix root causes: reproduce, trace, and remove the cause.
- Guard context: delegate bulk exploration or summarize aggressively.
- Never block on the human for reversible local work.
- Encode lessons in structure when a correction repeats.

## Playbook Routing

- Investigation: read-only question or design confidence check.
- Bug fix: reproduce, root-cause, fix, verify.
- Feature: name the data shape, implement the smallest coherent behavior, verify user path.
- Refactor: prove behavior equivalence while deleting complexity.
- Performance: capture baseline, change one thing, compare treatment.
- Runtime forensics: diagnose from logs, traces, profiles, or heap data before editing.
- Prototype: build disposable options to make a decision cheaply.
- Visual parity: compare screenshots and fix until the visible target matches.
- Skill authoring: write compact triggers, progressive disclosure, and validation steps.
- Autonomous run: keep a decision trail and concrete stop condition.

## Reply Rule

Name the principle that changed a decision. If no principle changed a decision, do not cite one. Tiny bit brutal, but useful.
