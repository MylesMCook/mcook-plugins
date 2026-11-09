# Review Rubrics

Use this file when reviewing an architecture, RFC, ADR, migration plan, codebase structure, or incident. Produce concrete findings, not generic advice.

## Finding format

```markdown
### [Severity] [Short title]

**Evidence:** [What in the doc/code/request triggered this]
**Why it matters:** [Impact in user terms]
**Laws triggered:** [3 or fewer]
**Fix:** [Specific change]
**Validation:** [How to prove the fix worked]
```

Severity levels:

- **Blocker**: likely correctness, security, data loss, outage, irreversible architecture, or unbounded cost risk.
- **High**: significant maintainability, reliability, scalability, compatibility, or delivery risk.
- **Medium**: meaningful risk or omission that can be scheduled.
- **Low**: polish, clarity, or local improvement.

Do not invent evidence. If evidence is absent, say "not specified" and explain why that absence is a risk.

## Architecture review rubric

| Area | Pass signal | Fail signal | Laws |
|---|---|---|---|
| Problem framing | Goals, non-goals, constraints, success metrics are clear | Solution chosen before problem is defined | First Principles, Map/Territory, Goodhart |
| Simplicity | Smallest credible architecture is considered | Starts with peak complexity | KISS, YAGNI, Gall, Second-System |
| Boundaries | Components own clear responsibilities and data | Shared mutable data, unclear APIs, circular dependencies | Conway, Demeter, DRY |
| Evolution | Migration/versioning/backward compatibility exists | Big-bang change, no deprecation path | Hyrum, Lehman, Unintended Consequences |
| Reliability | Failure modes, observability, rollout, rollback exist | Happy-path-only design | Murphy, Distributed Fallacies |
| Data | Source of truth, consistency, lifecycle, backup are defined | No ownership, hidden dual writes, undefined consistency | CAP, Tesler |
| Operations | Owners, runbooks, alerts, deploy path exist | No on-call or recovery story | Bus Factor, Broken Windows |
| Security/privacy | Trust boundaries and access rules are explicit | Sensitive data/auth left vague | Murphy, Least Astonishment |
| Team fit | Ownership and communication paths match architecture | Many-team coordination for routine changes | Conway, Brooks, Dunbar |
| Validation | Tests, metrics, experiments, and kill criteria exist | Claims with no evidence plan | Gilb, Confirmation Bias |

## System design review questions

Ask these in order:

1. What problem is being solved, for whom, and by when?
2. What constraints are real versus speculative?
3. What is the simplest option that could work?
4. What does this design make easy?
5. What does this design make hard?
6. Where can it fail, and how will we detect it?
7. What data can be lost, corrupted, duplicated, delayed, or exposed?
8. What user-visible behavior changes?
9. What existing clients or workflows might depend on current behavior?
10. What has to be true for the recommendation to be wrong?
11. What can be tested before full commitment?
12. What is the rollback or exit strategy?

## API review rubric

| Check | Pass | Fail |
|---|---|---|
| Contract clarity | Inputs, outputs, errors, auth, retryability documented | Consumers must infer behavior |
| Compatibility | Additive changes, versioning, deprecation, contract tests | Breaking changes hidden as refactors |
| Idempotency | Commands safe to retry or explicitly not retryable | Retry can duplicate money/orders/emails |
| Pagination/rate limits | Large result sets bounded | Unbounded list endpoints |
| Error design | Stable error codes and actionable messages | Free-form errors relied on by clients |
| Security | AuthZ checked at resource/action boundary | Auth assumed by caller or gateway only |
| Observability | Request IDs, traces, audit logs | Debugging depends on screenshots |
| Least astonishment | Names and behaviors follow ecosystem norms | Surprising side effects or inconsistent semantics |

## Distributed system review rubric

Blocker if any critical distributed workflow lacks:

- Timeout budget.
- Retry policy with bounded attempts and jitter.
- Idempotency/deduplication strategy.
- Backpressure/load-shedding behavior.
- Consistency model.
- Observability for cross-service flow.
- Replay/dead-letter/reconciliation story for async messaging.
- Security at the boundary.

Typical findings:

- **High:** No source-of-truth decision for duplicated state.
- **High:** Event consumers depend on ordering without partition/key guarantees.
- **High:** Dual writes without outbox/reconciliation.
- **Medium:** No documented retryability for API errors.
- **Medium:** Queue has DLQ but no owner/process to drain it.
- **Low:** Trace IDs not shown in examples.

## Migration/rewrite review rubric

A migration plan should include:

- Inventory of users, clients, data, integrations, and jobs.
- Compatibility strategy.
- Cutover strategy.
- Backfill plan.
- Verification/reconciliation checks.
- Rollback/repair plan.
- Telemetry before migration.
- Ownership and timeline.
- Explicit deletion plan for old paths.

High-risk signs:

- "Rewrite from scratch" without strangler analysis.
- No source-of-truth during transition.
- No dark launch/shadow traffic/parallel run where feasible.
- No rollback for schema or data changes.
- Success defined as "new system is live" rather than correctness, cost, reliability, and user impact.

## Planning review rubric

| Check | Strong plan | Weak plan |
|---|---|---|
| Scope | Must/should/could and non-goals | All desires treated as required |
| Estimate | Range with assumptions and confidence | Single date with no uncertainty |
| Sequence | Milestones de-risk hardest unknowns early | Hardest integration saved for the end |
| Staffing | Onboarding and coordination cost included | People added linearly to speed up |
| Metrics | Outcome metrics plus guardrails | Velocity/output metrics only |
| Risk | Risk register and triggers | Risks mentioned but unmanaged |
| Done | Includes tests, docs, rollout, observability, support | "Code complete" equals done |

## Quality/code review rubric

Use when reviewing code structure or refactor plans.

| Area | Strong | Weak | Laws |
|---|---|---|---|
| Clarity | Names and control flow explain intent | Cleverness required to understand | Kernighan, KISS |
| Duplication | Knowledge has one owner | Business rules copied in many places | DRY |
| Coupling | Modules know only necessary collaborators | Deep chains and hidden global state | Demeter |
| Tests | Fast tests cover logic; integration tests cover boundaries | Slow brittle e2e suite only | Testing Pyramid |
| Evolution | Small refactors tied to touched code | Massive cleanup unrelated to goal | Boy Scout, Broken Windows |
| Debt | Tradeoff and repayment trigger recorded | TODOs with no owner | Technical Debt |
| Surprise | APIs behave as expected | Hidden side effects | Least Astonishment |

## Incident/postmortem architecture review

Focus on systems, not blame.

Output:

```markdown
## Architectural contributing factors
- [Boundary, dependency, data, process, or observability weakness]

## Detection gap
- [Why the issue was not caught earlier]

## Containment gap
- [Why blast radius was larger than necessary]

## Recovery gap
- [Why restore/repair was slow or risky]

## Design changes
1. [Change] — prevents/detects/contains/recovers from [failure mode]

## Follow-up validation
- [Test, alert, game day, dashboard, runbook]
```

Apply Hanlon's Razor, Murphy's Law, Broken Windows, Bus Factor, Distributed Fallacies, and Map/Territory.

## Decision review rubric

A strong decision has:

- Problem statement.
- Context and constraints.
- Options considered.
- Recommendation.
- Tradeoffs.
- Consequences.
- Reversibility.
- Validation plan.
- Review date or trigger.
- Owner.

Reject or revise decisions that:

- Use popularity as proof.
- Hide costs.
- Lack alternatives.
- Ignore team ability to operate the choice.
- Have no trigger for reevaluation.
- Are justified by sunk cost.

## Final review self-check

Before final answer, verify:

- Did I answer the user's actual question?
- Did I recommend one path, not just list possibilities?
- Did I preserve good existing choices?
- Did I include tradeoffs and failure modes?
- Did I avoid speculative complexity?
- Did I identify missing facts without stalling unnecessarily?
- Did I propose validation and next steps?
- Did I map to laws only where they changed the analysis?
