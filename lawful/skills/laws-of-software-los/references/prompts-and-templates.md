# Prompts and Templates

Use these when the final answer needs a polished structure. Adapt rather than blindly filling every section.

## 1. Architecture recommendation template

```markdown
# Architecture recommendation: [topic]

## Recommendation
Choose [option] because [dominant constraint]. Confidence: [High/Medium/Low].

## Context I am assuming
- [Assumption]
- [Assumption]

## Options considered

| Option | Best when | Pros | Cons | Reversibility | Verdict |
|---|---|---|---|---|---|
| [A] |  |  |  |  |  |
| [B] |  |  |  |  |  |
| [C] |  |  |  |  |  |

## Why this is the right default
- [Reason tied to requirements]
- [Reason tied to laws/tradeoffs]

## Design sketch
- Components:
- Data ownership:
- APIs/events:
- Deployment:
- Security boundaries:
- Observability:

## Risks and mitigations

| Risk | Impact | Mitigation | Validation |
|---|---|---|---|
|  |  |  |  |

## Rollout plan
1. [Smallest safe step]
2. [Validation checkpoint]
3. [Expand]
4. [Cleanup/delete old path]

## What would change my mind
- [Evidence]
```

## 2. Design review template

```markdown
# Design review: [document/system]

## Summary
[2-4 lines with overall judgment]

## Blockers
- **[Issue]** — [impact]. Fix: [action].

## High-priority improvements
1. **[Issue]**
   - Evidence:
   - Why it matters:
   - Laws:
   - Fix:
   - Validation:

## Medium/low-priority improvements
- [Finding]

## What is strong
- [Preserve good choices]

## Recommended path
1. [Now]
2. [Next]
3. [Later]

## Open questions
- [Only material questions]
```

## 3. Microservices vs monolith answer template

```markdown
## Recommendation
Start with / stay with / move toward [modular monolith | selective service extraction | microservices] because [reason].

## Decision drivers
- Team ownership:
- Deploy cadence:
- Scaling profile:
- Data consistency:
- Operational maturity:
- Compliance/security:
- Product volatility:

## Extraction gate
Extract a service only when it has:
- Clear owner/on-call
- Stable boundary and API
- Independent reason to deploy/scale/isolate
- Observability and contract tests
- Data ownership and consistency model

## Path
1. Enforce module boundaries now.
2. Track extraction triggers.
3. Extract the first service only when a trigger fires.
```

## 4. Rewrite decision template

```markdown
## Recommendation
[Do not rewrite yet | Incrementally replace | Rewrite narrowly] because [reason].

## Keep
- [Parts worth preserving]

## Replace
- [Parts that create disproportionate drag]

## Strategy
Use [strangler | branch by abstraction | parallel run | targeted rewrite].

## Migration plan
1. Add observability and characterization tests.
2. Create seam.
3. Move one low-risk path.
4. Run old/new in parallel where feasible.
5. Reconcile data.
6. Shift traffic gradually.
7. Delete old code.

## Kill criteria
Stop or pivot if [condition].
```

## 5. Performance answer template

```markdown
## Recommendation
Do not optimize [area] yet / optimize [specific bottleneck] because [evidence].

## Baseline needed
- Workload:
- SLO:
- Current p50/p95/p99:
- Cost:
- Data size:
- Bottleneck evidence:

## Plan
1. Instrument.
2. Profile under realistic load.
3. Optimize the dominant bottleneck.
4. Validate speedup and correctness.
5. Add regression guard.
```

## 6. Planning/estimate template

```markdown
## Estimate
Range: [low]-[high], confidence [level].

## Assumptions
- [Assumption]

## Milestones
1. [Milestone] — proves [risk]
2. [Milestone] — proves [risk]

## Risks
| Risk | Probability | Impact | Mitigation | Trigger |
|---|---|---|---|---|

## Scope cuts
- [Cut] saves [time/risk] while preserving [value].

## Not included unless stated
- Production hardening
- Data migration
- Runbooks
- Documentation
- Support/on-call
- Security review
```

## 7. Incident architecture analysis template

```markdown
## What failed architecturally
[System/process/design weakness, not blame]

## Why detection lagged
[Telemetry, alerting, ownership, or mental model gap]

## Why containment lagged
[Blast radius, coupling, rollback, dependency, or access gap]

## Permanent fixes
1. [Prevention]
2. [Detection]
3. [Containment]
4. [Recovery]

## Validation
- [Game day/test/alert/runbook]
```

## 8. Questions that unlock better architecture

Use no more than 5 unless the user explicitly wants discovery.

- What is the most important constraint: speed to market, reliability, cost, scale, compliance, or team autonomy?
- What is the current and expected workload?
- What data must be strongly consistent?
- Who owns and operates this after launch?
- What happens if this dependency is slow, down, duplicated, or wrong?
- What is the rollback path?
- What is the simplest version that would teach us enough?
- Which users or integrations rely on current behavior?
- What would make this decision obviously wrong in three months?
- What can we measure before committing?

## 9. Compact law callout format

Use this when you want to show rigor without overwhelming the user:

```markdown
The laws that matter most here are:
- **Gall + KISS:** start with the smallest working architecture.
- **Hyrum:** protect existing clients from behavior changes.
- **Distributed Fallacies + CAP:** do not split services until failure and consistency semantics are explicit.
- **Goodhart:** define guardrail metrics so the target does not distort behavior.
```

## 10. Tone rules

- Be clear and direct.
- Prefer "I recommend X" over "it depends" after explaining the key dependency.
- Name tradeoffs without apologizing for them.
- Do not invoke every law; use only the few that change the decision.
- When uncertain, say what evidence would resolve the uncertainty.
