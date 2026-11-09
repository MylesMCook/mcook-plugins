# Architecture Playbook

Use this when the task needs a concrete system design, architecture recommendation, or review beyond the quick workflow in `SKILL.md`.

## 1. Staff-level architecture algorithm

### A. Establish the architectural thesis

Write one sentence:

> We should choose **[architecture]** because **[primary constraint]**, while accepting **[main tradeoff]**, and we will validate it by **[evidence]**.

If you cannot write this sentence, the recommendation is not ready.

### B. Elicit the minimum necessary context

Collect or infer:

- Product goal and user journey.
- Functional requirements and explicit non-goals.
- Workload: traffic, concurrency, data volume, growth, read/write mix, batch/stream needs.
- Quality attributes: latency, availability, consistency, durability, security, privacy, compliance, cost, operability, maintainability, portability.
- Data model: authoritative sources, ownership, lifecycle, retention, migration constraints.
- Environment: cloud/on-prem/edge/mobile/browser, regions, deployment frequency, runtime constraints.
- Team/org: team count, ownership, on-call maturity, release process, skill set, vendor constraints.
- Existing system: dependencies, pain points, incident history, technical debt, integration points.
- Decision horizon: prototype, MVP, 6-month product, multi-year platform.

### C. Separate requirement types

| Requirement type | Examples | How to handle |
|---|---|---|
| Hard constraint | Legal retention, data residency, existing vendor, budget cap | Must satisfy or explicitly reject the project. |
| Target | p95 latency, uptime, cost/user, deploy frequency | Design to meet, measure, and revisit. |
| Preference | Language, framework, team taste | Respect when cheap; do not let it dominate architecture. |
| Guess | "We may need global scale someday" | Convert to trigger/threshold or defer. |

### D. Pick the smallest credible architecture

Default sequence:

1. Single process/script/prototype when validating an idea.
2. Modular monolith when domain boundaries are emerging but operational simplicity matters.
3. Service extraction when a boundary has independent ownership, deploy cadence, scale, compliance, or reliability needs.
4. Event-driven or distributed architecture when workflows are asynchronous, integrations are many, or availability/decoupling demands it.
5. Platform architecture only after repeated product/team needs prove a reusable platform is cheaper than duplication.

### E. Make decisions reversible where possible

- Prefer configuration, schema additions, adapters, branch-by-abstraction, and strangler seams.
- Avoid irreversible data coupling, premature public APIs, unbounded plugin systems, and global shared databases.
- For irreversible choices, require stronger evidence, a migration path, and a kill criterion.

## 2. Architecture option comparison

Use this matrix when presenting alternatives:

| Factor | Option A | Option B | Option C |
|---|---|---|---|
| Fits current requirements |  |  |  |
| Complexity added |  |  |  |
| Operational burden |  |  |  |
| Team fit |  |  |  |
| Scalability path |  |  |  |
| Failure modes |  |  |  |
| Reversibility |  |  |  |
| Cost |  |  |  |
| Recommendation |  |  |  |

A strong comparison includes at least one reason the recommended option could be wrong.

## 3. Modular monolith default

Recommend a modular monolith when:

- One or a few teams own the system.
- Deployment independence is not yet a bottleneck.
- Domain boundaries are still changing.
- The team lacks mature service observability/on-call/contract-testing.
- Most scaling needs can be solved inside one deployable unit.

Make it real:

- Enforce module boundaries in code.
- Own data per module logically even if physically one database.
- Use internal interfaces/events to prevent cross-module spaghetti.
- Keep domain seams extractable.
- Add integration tests around module boundaries.
- Track extraction triggers: traffic, team ownership, deploy cadence, compliance, or isolation.

## 4. Microservices/service extraction gate

Extract a service only when at least one strong driver exists:

- Independent team ownership with clear API contract.
- Independent scaling profile or resource isolation need.
- Independent release cadence causing bottlenecks.
- Compliance/security isolation.
- Reliability isolation, blast-radius control, or fault containment.
- External integration boundary with lifecycle different from core product.

Before recommending extraction, require:

- Service owner and on-call owner.
- API/schema contract and compatibility strategy.
- Timeouts, retries, idempotency, circuit breakers, and backpressure.
- Observability: logs, metrics, traces, dashboards, alerts, SLOs.
- Deployment pipeline, canary/rollback, versioning.
- Data ownership and consistency model.
- Local development/testing story.
- Cost and operational burden estimate.

If those are absent, recommend a modular boundary first.

## 5. Distributed systems checklist

For every remote call, queue, cache, event stream, replicated database, or cross-region dependency, answer:

### Communication

- What is the timeout budget?
- Are retries bounded with jitter/backoff?
- Is the operation idempotent?
- Can messages arrive duplicated, late, out of order, or never?
- Is there backpressure or load shedding?
- Is there a circuit breaker or bulkhead?
- Are failures visible to users, hidden, or retried asynchronously?

### Consistency

- What is the source of truth?
- Which operations require strong consistency?
- Which can be eventual?
- What invariants must never be violated?
- How are conflicts detected and resolved?
- What happens during partition or regional outage?
- Is there a reconciliation process?

### Data and events

- Is schema evolution backward and forward compatible?
- Are events facts, commands, or state snapshots?
- Are event consumers allowed to depend on ordering?
- Is there a dead-letter queue, replay story, and poison-message handling?
- Is the outbox/inbox pattern needed to avoid dual-write loss?
- How are backfills and replays protected from side effects?

### Operations

- What dashboards prove health?
- What alerts are actionable?
- What runbook exists for each critical failure mode?
- What is the recovery-time objective and recovery-point objective?
- How is capacity tested?
- How are secrets, certificates, and config rotated?
- How are dependencies degraded or bypassed?

## 6. API design checklist

A production API should specify:

- Resource model or command model.
- AuthN/AuthZ and permission boundaries.
- Input validation and error format.
- Idempotency for create/update commands.
- Pagination, filtering, sorting, rate limits.
- Versioning and deprecation policy.
- Backward compatibility expectations.
- Error semantics and retryability.
- Request/response examples.
- Observability fields: request ID, trace ID, audit ID.
- Contract tests for providers and consumers.
- Abuse cases and privacy constraints.

Default rules:

- Avoid leaking internal persistence models.
- Keep public contracts boring and explicit.
- Never assume undocumented behavior is safe to change if users have observed it.
- Use additive changes when possible.
- Make breaking changes rare, deliberate, and migrated.

## 7. Data architecture checklist

For every entity/table/topic/blob:

- Who owns it?
- What is the authoritative source?
- What are lifecycle states?
- What are invariants?
- What is retention/deletion policy?
- What is the backup/restore plan?
- What is the migration/backfill strategy?
- What is the audit/compliance requirement?
- Who may read/write it?
- What data quality checks exist?
- How is schema changed safely?
- How are caches invalidated or refreshed?

Default guidance:

- Avoid shared write databases across service boundaries.
- Prefer explicit ownership over "everyone can update everything."
- Treat caches as derived and disposable unless explicitly durable.
- Do not add async events without a replay/reconciliation story.
- Treat analytics models and operational models as different maps of reality.

## 8. Reliability and operability

A design is not production-ready until it covers:

- SLOs or service expectations.
- Error budget or risk tolerance.
- Health checks and readiness checks.
- Metrics, logs, traces, and correlation IDs.
- Alerting with owners and thresholds.
- Runbooks for top failure modes.
- Deployment strategy: canary, blue/green, feature flag, or progressive rollout.
- Rollback and data rollback/repair story.
- Capacity plan and load test.
- Disaster recovery plan proportional to business criticality.
- Dependency degradation plan.

Ask: "How would we know this is failing before customers tell us?"

## 9. Performance and scale process

1. Define workload and SLO.
2. Measure baseline with realistic data.
3. Find bottlenecks with profiling/tracing.
4. Estimate theoretical speedup and serial bottlenecks.
5. Optimize the highest-impact path.
6. Validate under load.
7. Simplify the optimized path so future debugging remains possible.
8. Add regression tests or performance budgets.

Do not optimize unknown paths. Do not parallelize before identifying serial constraints. Do not cache before defining invalidation and correctness behavior.

## 10. Migration and rewrite playbook

Prefer incremental replacement.

### Choose a strategy

| Strategy | Use when | Watch for |
|---|---|---|
| Strangler fig | Replacing a legacy system route/use-case at a time | Routing complexity and data sync. |
| Branch by abstraction | Replacing internals behind a stable interface | Abstraction becoming permanent junk. |
| Parallel run | Need confidence before cutover | Cost and divergence. |
| Dual write | Temporary bridge for data migration | Consistency gaps; needs reconciliation. |
| Backfill + shadow read | Migrating large datasets | Idempotency, throttling, and verification. |
| Big-bang cutover | Only when surface is small and rollback is simple | Usually riskier than it looks. |

### Migration minimums

- Inventory dependencies and users.
- Define compatibility period.
- Decide source of truth during transition.
- Build reconciliation checks.
- Add observability before moving traffic.
- Start with low-risk traffic.
- Keep rollback path until verification passes.
- Delete old paths when migration is complete.

## 11. Technical debt handling

Classify debt:

| Type | Example | Treatment |
|---|---|---|
| Deliberate tactical | Shortcut to hit a validated deadline | Record owner, interest, and repayment trigger. |
| Accidental | Design decayed through change | Refactor near touched code; budget recurring cleanup. |
| Architectural | Wrong boundary or dependency direction | Create migration plan and decision record. |
| Operational | Manual deploys, weak observability | Pay down before scale increases. |
| Knowledge debt | Only one person understands it | Pairing, docs, runbooks, rotation. |

A debt item needs: owner, impact, interest cost, trigger, proposed fix, and "do nothing" consequence.

## 12. Security and privacy baseline

For every system:

- Identify trust boundaries.
- Authenticate and authorize every privileged operation.
- Validate inputs at boundaries.
- Avoid logging secrets/PII.
- Encrypt sensitive data in transit and, when required, at rest.
- Design least privilege for services, users, and operators.
- Add audit logs for sensitive operations.
- Include rate limiting and abuse cases.
- Define data retention and deletion.
- Consider supply-chain risk and dependency update process.

Escalate to a security specialist for regulated data, cryptography, auth design, multi-tenant isolation, payments, healthcare, finance, or safety-critical systems.

## 13. Team topology and ownership

Architecture should reduce coordination, not amplify it.

Check:

- Does each module/service have one accountable owner?
- Can a team deliver a user-visible change without waiting on many teams?
- Are interfaces stable enough for independent work?
- Is there a platform team only where product teams actually need a productized platform?
- Are high-risk components covered by more than one person?
- Are decision rights explicit?
- Is on-call aligned with ownership?

When architecture and org conflict, decide which one changes. Ignoring the mismatch creates hidden coordination tax.
