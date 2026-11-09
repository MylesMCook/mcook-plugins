---
name: laws-of-software-los
description: >-
  Evaluate substantive software architecture tradeoffs, system boundaries,
  ADRs, migration strategies, and architectural incident lessons. Use when
  alternatives, ownership, compatibility, or recovery need an explicit design
  decision. Do not activate for ordinary implementation, routine bug fixes,
  generic code review, or formatting without an architectural decision.
---

# Laws of Software (LOS)

Apply this skill when software work needs principal-level judgment, explicit tradeoffs, and a credible validation path.

This skill is original synthesis inspired by the public law list at `https://lawsofsoftwareengineering.com/`. Use the source site for canonical law descriptions and updates.

## Use when

- choosing or reviewing architecture, system design, APIs, service boundaries, or infrastructure direction
- reviewing an RFC, ADR, migration plan, incident, codebase structure, or technical strategy
- deciding substantive distributed-system, data-ownership, compatibility, or recovery tradeoffs

Do not use for:

- tiny syntax fixes or rote formatting
- ordinary code changes and debugging that do not require an architecture decision
- purely mechanical conversions or summaries
- non-software domain work

## Operating contract

For code-producing tasks:

1. Prefer the smallest reversible design. Do not add speculative frameworks or abstractions.
2. Preserve compatibility by default. Treat observed behavior as part of the contract unless you have a migration plan.
3. Assume failure in remote or distributed paths. Add timeouts, retry bounds, idempotency, backpressure, and observability where they matter.
4. Treat data changes as dangerous. Define source of truth, invariants, migration safety, reconciliation, and rollback.
5. Keep security baseline intact. No secret leaks, auth bypasses, unsafe dynamic execution, or injection patterns.
6. Add focused tests when behavior changes, or say what narrower validation substitute ran and why.
7. Ship operability with production paths: logs, metrics, traces, alerts, owners, and rollback criteria when relevant.
8. Name the tradeoffs. Do not present code or designs as production-ready while hiding risk.

## Workflow

1. Frame the real problem.
   State the goal, actors, constraints, non-goals, success metrics, and time horizon. If a missing fact would not change the answer, make a minimal assumption and proceed.
2. Map the current system before changing it.
   Inspect the existing code, boundaries, data ownership, dependencies, trust boundaries, runtime environment, and failure domains.
3. Generate the smallest credible path.
   For architecture work, compare 2-4 viable options and always include the simplest one. For code work, prefer the smallest safe patch.
4. Stress-test with law lenses.
   Use `references/law-index.md` for the full checklist. Pick only the few laws that materially change the recommendation.
5. Decide, implement, and document.
   Make rationale, rollout, rollback, and validation explicit. Use templates from `assets/` when they save time.
6. Verify before finalizing.
   Run relevant scripts from `scripts/` when files are available, then run the repo checks that matter for the change.
7. Close with evidence.
   State what changed or what you recommend, what was validated, and the remaining material risk.

## Law groups

Use `references/law-index.md` when you need the full 56-law pass. Common groups:

- architecture and distributed systems
- teams and ownership
- planning and estimation
- quality, testing, and evolution
- scale and performance
- local design and code clarity
- decision quality and bias

Do not law-dump. Use the 3-8 laws that change the answer.

## Scripts

Run these from the skill root when they fit the artifact in front of you:

```bash
python3 scripts/arch_law_check.py --input path/to/design.md
python3 scripts/arch_law_check.py --input path/to/design.md --json
python3 scripts/adr_lint.py --input path/to/adr.md
```

The checkers flag omissions; they do not prove correctness.

## Templates and references

Load only what the task needs:

- `references/architecture-playbook.md` for concrete system-design guidance
- `references/review-rubrics.md` for architecture, API, migration, planning, or code-structure reviews
- `references/decision-frameworks.md` for technology choices, metrics, and cognitive traps
- `references/prompts-and-templates.md` for polished answer structures
- `references/evaluation-guide.md` for trigger and output evaluation

Useful templates in `assets/`:

- `assets/adr-template.md`
- `assets/architecture-review-template.md`
- `assets/incident-architecture-review-template.md`
- `assets/migration-plan-template.md`
- `assets/risk-register-template.md`
- `assets/system-design-brief-template.md`

## Hard gotchas

- Microservices are not the default. Prefer a modular monolith or narrower extraction until ownership, deploy cadence, scale, compliance, or isolation forces the split.
- Rewrites are guilty until proven necessary. Favor strangler, branch-by-abstraction, or targeted replacement.
- Performance claims without workload, SLO, profile, benchmark, or cost model are guesses.
- "Future-proofing" needs a near-term scenario. Otherwise keep it as a simple extension point or defer it.
- Metrics need guardrails or they get gamed.
- Distributed flows need timeouts, retries, idempotency, backpressure, consistency decisions, and observability.
- A design with no owner, runbook, migration plan, or rollback is not production-ready.
- A code change with no tests or explicit validation is not production-ready.
