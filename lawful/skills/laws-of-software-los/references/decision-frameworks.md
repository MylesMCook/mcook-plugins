# Decision Frameworks

Use this when the user asks "which technology", "what architecture should we choose", "should we rewrite", "is this worth it", "what metrics should we use", or when stakeholders disagree.

## 1. Decision spine

Every serious technical decision should have this spine:

```markdown
## Decision
We will [choice] for [scope/timeframe].

## Context
[Problem, constraints, users, existing system, decision horizon]

## Forces
- [Force 1: e.g., latency, cost, team autonomy]
- [Force 2]
- [Force 3]

## Options
1. [Option]
2. [Option]
3. [Option]

## Tradeoff
[What the decision sacrifices]

## Consequences
[Expected benefits, risks, follow-up work]

## Validation
[How we will know we were right or wrong]

## Revisit trigger
[Metric/date/event that reopens the decision]
```

If a decision lacks a revisit trigger, it tends to become dogma.

## 2. Reversible vs irreversible

Classify before analysis depth:

| Type | Examples | Decision style |
|---|---|---|
| Reversible | Internal library, feature flag behavior, dashboard tool | Try cheaply, measure, rollback if wrong. |
| Hard but reversible | Database index strategy, queue vendor, service extraction behind stable API | Prototype and plan migration. |
| Mostly irreversible | Public API contract, data model used by many clients, compliance posture, encryption scheme | Require deep review, compatibility plan, staged rollout. |
| Irreversible in practice | Multi-year platform bet, vendor lock-in with stored data, public protocol | Require executive/architecture review and explicit exit cost. |

Use reversibility to avoid both over-analysis and reckless commitment.

## 3. First-principles decomposition

When architecture debate gets ideological, reduce it to primitives:

- What data exists?
- Who creates, reads, updates, deletes it?
- What invariants must hold?
- What latency/availability/security/cost constraints are real?
- What failures are tolerable?
- What coordination must happen between humans?
- What changes often and what changes rarely?
- What can be delayed, approximated, cached, or recomputed?
- What must be correct immediately?

Then rebuild the architecture from those answers.

## 4. Inversion / pre-mortem

Ask:

- How would this architecture fail in production?
- How would it become too expensive?
- How would it become impossible to debug?
- How would users misuse it?
- How would another team accidentally break it?
- How would the migration corrupt data?
- How would the metric be gamed?
- How would the project be "90% done" forever?
- How would one person's departure stall everything?

Turn each answer into a mitigation or an explicit accepted risk.

## 5. Goodhart-resistant metrics

For each metric:

| Question | Example |
|---|---|
| What behavior do we want? | Faster customer checkout. |
| What proxy will we measure? | p95 checkout completion latency and conversion. |
| How can it be gamed? | Hide slow failures, reject slow customers, skip fraud checks. |
| What guardrails prevent gaming? | Error rate, fraud rate, support tickets, revenue, manual review. |
| Who reviews it qualitatively? | Product + engineering + support monthly. |

Prefer metric sets over single metrics.

Common pairs:

- Delivery speed + defect escape rate.
- Uptime + correctness + latency.
- Cost + performance + user impact.
- Test coverage + mutation/failure detection + flaky test rate.
- Team throughput + on-call load + satisfaction.

## 6. Hype/Lindy technology filter

Use for framework, language, database, cloud service, AI tool, or infrastructure choices.

| Lens | Ask |
|---|---|
| Lindy | Has this survived enough real use to deserve trust for ordinary requirements? |
| Hype Cycle | Are we reacting to novelty or to a durable capability shift? |
| Team fit | Can this team operate it at 3 a.m.? |
| Ecosystem | Are docs, libraries, hiring, debugging, and upgrades mature? |
| Exit cost | How do we leave if wrong? |
| Differentiation | Does this technology create product advantage or just engineering novelty? |
| Failure mode | What breaks when the vendor/project changes direction? |

Default: choose boring proven tech for commodity needs; choose novel tech only where it buys a material advantage or removes a material constraint.

## 7. Sunk-cost escape test

When a project feels too invested to stop:

1. Ignore money/time already spent.
2. Estimate remaining cost to reach useful outcome.
3. Estimate future value if completed.
4. Compare against alternatives starting today.
5. Identify the smallest salvageable asset.
6. Define stop/pivot/continue criteria.

Output:

```markdown
## Continue only if
[Evidence threshold]

## Pivot if
[Condition]

## Stop if
[Condition]

## Salvage
[Reusable code, knowledge, contracts, tests, migration learnings]
```

## 8. Architecture tradeoff matrix

Use weighted scoring only as a thinking aid, never as fake precision.

```markdown
| Criterion | Weight | Option A | Option B | Option C | Notes |
|---|---:|---:|---:|---:|---|
| Meets hard requirements | Must | Pass/Fail | Pass/Fail | Pass/Fail |  |
| Simplicity | 3 |  |  |  |  |
| Operability | 3 |  |  |  |  |
| Evolvability | 2 |  |  |  |  |
| Team fit | 3 |  |  |  |  |
| Cost | 2 |  |  |  |  |
| Performance headroom | 2 |  |  |  |  |
| Security/privacy | Must | Pass/Fail | Pass/Fail | Pass/Fail |  |
```

Rules:

- Any "Must" failure disqualifies unless the requirement changes.
- Explain scores in words.
- Run a sensitivity check: if small weight changes flip the result, call the decision close.
- Do not bury qualitative risk inside a number.

## 9. Decision traps and counter-moves

| Trap | Counter-move |
|---|---|
| Confirmation bias | Seek strongest argument against preferred option. |
| Dunning-Kruger | Add expert review and confidence level. |
| Hanlon failure | Fix process/tooling before blaming people. |
| Occam ignored | Test simpler explanation first. |
| Map/territory confusion | Compare docs/diagrams to production/code/telemetry. |
| Hype adoption | Pilot with exit criteria. |
| Sunk cost | Decide from today forward. |
| Local optimization | Optimize whole-system outcome, not team metric. |
| Analysis paralysis | Propose a reversible experiment. |
| Cargo culting | Re-derive from constraints. |

## 10. ADR quality gate

Before accepting an ADR, verify:

- Status is clear: proposed, accepted, superseded, deprecated.
- Decision is a decision, not a research note.
- Context includes constraints and non-goals.
- Options include at least one serious alternative.
- Consequences include downsides.
- Laws/forces are named only when they affect the decision.
- Validation plan says what evidence would prove or disprove the choice.
- Revisit trigger exists.
- Owner exists.

Use `assets/adr-template.md` for new ADRs and `scripts/adr_lint.py` for linting.
