# Evaluation Guide

Use this guide to test whether the `laws-of-software-los` skill improves agent output quality.

## Evaluation principles

- Compare outputs with the skill against outputs without the skill or against a previous version.
- Use realistic prompts that include ambiguity, constraints, and messy context.
- Grade pass/fail assertions where possible.
- Use blind human comparison for subjective quality.
- Track deltas: better tradeoffs, fewer omissions, more actionable recommendations, less overengineering.

## What good output looks like

A good answer:

- Recommends a specific path.
- States assumptions and confidence.
- Identifies the simplest credible option.
- Compares alternatives fairly.
- Names tradeoffs and failure modes.
- Handles data consistency, compatibility, security/privacy, reliability, observability, rollout, rollback, and ownership when relevant.
- Connects laws to decisions without dumping all laws.
- Provides validation and next steps.
- Avoids fake precision and cargo-cult best practices.

## Core eval prompts

Use or adapt the prompts below.

### Eval 1: Microservices pressure

Prompt:

> We have a Rails monolith with 12 engineers. Deploys are weekly and painful. Product wants us to split into microservices so we can scale. Should we do it?

Expected output:

- Does not blindly recommend microservices.
- Asks or assumes current bottlenecks.
- Recommends modular monolith hardening or selective extraction unless strong drivers exist.
- Covers Conway, Distributed Fallacies, CAP/data ownership, observability, contract testing, team ownership.
- Provides extraction gate and incremental path.

Pass assertions:

- Mentions operational prerequisites for services.
- Includes a simpler option.
- Includes validation/metrics.
- Includes risks of service extraction.

### Eval 2: Public API behavior change

Prompt:

> Our API docs say list results are unordered, but today they come back sorted by creation time. I want to change the query to improve performance. Safe?

Expected output:

- Invokes Hyrum's Law concept without necessarily naming it.
- Treats observed behavior as compatibility risk.
- Recommends telemetry, versioning or explicit sort parameter, deprecation/migration, contract tests, and release notes.
- Provides safe rollout.

Pass assertions:

- Does not say "docs allow it, so safe."
- Includes backward compatibility plan.
- Includes monitoring/rollback.

### Eval 3: Rewrite temptation

Prompt:

> The legacy billing system is ugly and slow to change. I want a clean rewrite in Go with event sourcing and microservices.

Expected output:

- Challenges second-system risk and sunk cost.
- Recommends evidence gathering and incremental migration.
- Identifies billing correctness/data risk.
- Suggests characterization tests, seams, strangler, parallel run, reconciliation.
- Defines when a rewrite is justified.

Pass assertions:

- Includes migration/rollback.
- Includes data reconciliation.
- Avoids technology-first decision.

### Eval 4: Performance folklore

Prompt:

> Our checkout feels slow. Should we add Redis everywhere and move the expensive work to Kafka?

Expected output:

- Requires workload, SLO, profiling/tracing.
- Warns against premature optimization.
- Provides measurement-first plan.
- Notes cache invalidation and async correctness.
- Identifies user-visible consistency and failure modes.

Pass assertions:

- Does not recommend Redis/Kafka as first step.
- Includes profiling and success metrics.
- Includes correctness risks.

### Eval 5: Estimation

Prompt:

> Leadership wants a date for migrating all customers from our old database to the new one. Engineering says 4 weeks. What should I include in the plan?

Expected output:

- Gives range/uncertainty and assumptions.
- Includes inventory, backfill, dual read/write or sync strategy, verification, rollback, observability, support, freeze windows.
- Mentions Ninety-Ninety/Hofstadter/Brooks-style concerns.
- Adds risk register and scope cuts.

Pass assertions:

- Includes data migration validation.
- Includes rollback or repair.
- Includes operational work beyond code.

### Eval 6: Incident/postmortem

Prompt:

> Yesterday an email retry job sent duplicate receipts to 80k users. How should we fix the system?

Expected output:

- Avoids blame.
- Identifies idempotency, dedupe keys, retry semantics, observability, backfill/repair, rate limiting, test coverage.
- Suggests runbook and verification.
- Applies distributed-systems failure thinking.

Pass assertions:

- Includes idempotency.
- Includes detection/alerting.
- Includes prevention and recovery.

## Scoring rubric

Grade each output 0/1 for each assertion:

| Dimension | Pass criteria |
|---|---|
| Recommendation | Clear recommended path, not only pros/cons |
| Simplicity | Considers simplest credible option |
| Tradeoffs | Names what the recommendation sacrifices |
| Law coverage | Uses relevant laws, not law dumping |
| Failure modes | Covers realistic failure paths |
| Operability | Includes observability, rollout, rollback, ownership when relevant |
| Data/API safety | Covers consistency, migration, compatibility when relevant |
| Validation | Includes tests, metrics, experiments, or acceptance criteria |
| Actionability | Gives concrete next steps |
| Calibration | States assumptions/confidence and avoids overclaiming |

Compare total pass count with and without the skill, but also perform a blind preference review for overall usefulness.

## Trigger eval queries

Should trigger:

- "Review this architecture diagram and tell me what will break."
- "Should we split our monolith into services?"
- "Write an ADR for choosing Postgres vs DynamoDB."
- "Plan a safe migration from one billing provider to another."
- "How do we make this API versioning strategy less risky?"
- "This system is slow; recommend a performance plan."
- "Act like a staff engineer and review this RFC."
- "What team structure should own these services?"

Should not trigger:

- "Fix this TypeScript syntax error."
- "Write a regex for email validation."
- "Explain what a for loop is."
- "Convert this JSON to YAML."
- "Summarize this unrelated legal document."
- "Make this CSS button blue."

## Iteration loop

1. Run at least 6 eval prompts without the skill.
2. Run the same prompts with the skill.
3. Grade pass/fail assertions.
4. Blind-compare overall usefulness.
5. Inspect misses:
   - Wrong trigger: improve `description`.
   - Missing analysis: add a gotcha or checklist.
   - Too verbose: move detail to references.
   - Repeated manual reasoning: add a script/template.
6. Revise and rerun.
