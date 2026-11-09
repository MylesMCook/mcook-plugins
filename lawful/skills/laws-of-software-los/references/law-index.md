# Law Index for Laws of Software (LOS)

This file is an original architecture-review checklist inspired by the public law list at `https://lawsofsoftwareengineering.com/`. It is not a copy of the source site's explanations. Consult the source site for canonical descriptions, citations, and updates.

Use this file when you need comprehensive coverage. Do not dump every law into the final answer. Pick the 3-8 laws that materially change the recommendation.

## How to use the laws

1. Identify the decision type: architecture, teams, planning, quality, scale, design, or decision-making.
2. Scan the relevant group below.
3. Convert each triggered law into a concrete question:
   - "What hidden dependency will break?"
   - "Where does complexity go?"
   - "What are we measuring, and how can that measure be gamed?"
4. Turn the answer into a fix, guardrail, experiment, or explicit tradeoff.

## Architecture laws

| Law | Agent move | Red flags |
|---|---|---|
| Conway's Law | Align architecture boundaries with team communication and ownership. Recommend an Inverse Conway Maneuver when the desired architecture and org shape conflict. | Services split by technical layer only; many teams must coordinate for one feature; unclear owners. |
| Hyrum's Law | Treat observable behavior as part of the contract. Add compatibility tests, versioning, migration notes, and deprecation windows. | "It's undocumented so nobody relies on it"; changing error text/status/ordering without notice. |
| Gall's Law | Prefer evolving a small working system into a larger one. Demand a walking skeleton before grand architecture. | Big-bang platform; no simple end-to-end path; design starts at peak complexity. |
| Law of Leaky Abstractions | Identify what the abstraction hides poorly and document escape hatches. | ORM hiding bad queries; queues hiding delivery semantics; cloud service hiding quotas. |
| Tesler's Law | Place irreducible complexity where it is cheapest and safest to manage. | Complexity shoved to users, operators, or every caller; "we eliminated complexity" with no accounting. |
| CAP Theorem | For partition-prone distributed data, state the consistency/availability behavior per operation. | Global consistency promised with always-on availability; no behavior for network partitions. |
| Second-System Effect | Challenge ambitious rewrites and v2 expansions. Keep the replacement's scope smaller than the ego wants. | "While we're rewriting, let's add..."; generalized plugin frameworks before product fit. |
| Fallacies of Distributed Computing | Design every remote interaction for latency, failure, security, bandwidth, topology change, and heterogeneity. | Chatty service mesh; no timeouts/retries/idempotency; assuming same LAN/cloud/region forever. |
| Law of Unintended Consequences | Add blast-radius controls: canary, feature flags, rollback, observability, and post-change review. | "This is a small change" in a coupled system; no production telemetry. |
| Zawinski's Law | Resist scope gravity. Keep products and platforms from absorbing every adjacent function. | Roadmap adds mail/calendar/chat/reporting just because integration is possible. |

## Team and organization laws

| Law | Agent move | Red flags |
|---|---|---|
| Brooks's Law | For late projects, reduce scope, improve sequencing, or remove blockers before adding people. | "Add five engineers and keep the same date"; onboarding not counted. |
| Dunbar's Number | Keep coordination structures human-scale. Split groups by bounded context and mission when relationship load dominates. | Everyone must know everyone; huge meetings; no clear tribe/program boundaries. |
| Ringelmann Effect | Make ownership visible and individual contributions accountable without creating hero culture. | Large undifferentiated teams; unclear decision rights; social loafing. |
| Price's Law | Find where critical work concentrates and reduce fragility around it. | One or two people do the architecture, releases, and incident response. |
| Putt's Law | Translate between technical reality and management incentives. Require technical review for technical decisions. | Decisions made by people furthest from the implementation; engineers excluded from planning. |
| Peter Principle | Separate management progression from technical mastery. Recommend staff/principal tracks and training. | Strong IC promoted into management without support; architecture done by title alone. |
| Bus Factor | Identify knowledge bottlenecks and add pairing, docs, runbooks, rotation, and ownership redundancy. | Only one person can deploy, debug, approve, or explain a component. |
| Dilbert Principle | Do not assume titles imply competence. Evaluate decisions by evidence, not hierarchy. | "VP wants it" replaces rationale; weak technical decisions become mandates. |

## Planning laws

| Law | Agent move | Red flags |
|---|---|---|
| Premature Optimization | Require measurement before complexity-heavy optimization unless constraints are already proven hard. | Optimizing cold paths; exotic data structures without workload; performance folklore. |
| Parkinson's Law | Timebox exploration, define done, and protect scope. | Work expands because no finish line exists; discovery never converges. |
| Ninety-Ninety Rule | Add integration, polish, edge cases, and operationalization to estimates. | "Almost done" before testing, migration, docs, and production hardening. |
| Hofstadter's Law | Treat estimates as uncertain distributions. Add buffers and milestone evidence. | Single deterministic date for novel work; no contingency. |
| Goodhart's Law | Pair target metrics with guardrails and audits. Ask how the metric can be gamed. | Velocity as productivity; uptime hiding correctness; ticket count as value. |
| Gilb's Law | Measure important qualities imperfectly rather than not at all. Define proxy metrics and validation. | "Maintainability can't be measured"; no baseline for reliability, latency, cost, or debt. |

## Quality and evolution laws

| Law | Agent move | Red flags |
|---|---|---|
| Murphy's Law / Sod's Law | Assume failure and design detection, mitigation, fallback, and recovery. | No error budgets; no disaster path; no failure injection or rehearsal. |
| Postel's Law | Emit a clear contract; accept only deliberate, documented input variants and monitor them. Reject ambiguity at security and data-integrity boundaries. [RFC 9413](https://www.rfc-editor.org/rfc/rfc9413.html) explains how broad tolerance can entrench noncompliance. | Brittle consumers; accepting garbage silently; schema drift with no validation. |
| Broken Windows Theory | Fix visible decay quickly so it does not normalize. | Dead code, flaky tests, TODO graveyards, inconsistent patterns. |
| Technical Debt | Track debt as a drag on change, not as moral failure. Assign owner, interest, payoff trigger, and expiry. | Debt accepted with no repayment plan; rewrite used as debt theater. |
| Linus's Law | Increase review diversity and observability for defect discovery. | Critical code reviewed by one person; no logs/traces/repro cases. |
| Kernighan's Law | Keep code simpler than the maximum cleverness the team can debug. | Clever concurrency, macros, reflection, or generics without strong tests. |
| Testing Pyramid | Bias toward many fast deterministic tests, with fewer integration and end-to-end tests. | Mostly slow UI tests; no unit/contract coverage; brittle release gates. |
| Pesticide Paradox | Refresh tests as the system and bug patterns evolve. | Test suite never catches new regressions; coverage exists but confidence is low. |
| Lehman's Laws of Software Evolution | Expect software tied to real-world domains to change continuously. Design for safe evolution. | Frozen architecture for moving business rules; no refactoring budget. |
| Sturgeon's Law | Expect mediocre artifacts; review ruthlessly and preserve only what earns its keep. | Copy-pasted patterns, unused abstractions, ceremony without value. |
| Boy Scout Rule | Improve nearby code in small safe increments while preserving scope. | "Not my mess"; drive-by changes too large to review. |

## Scale laws

| Law | Agent move | Red flags |
|---|---|---|
| Amdahl's Law | Find the serial bottleneck before parallelizing. Model expected speedup. | Throwing workers at single-threaded bottlenecks; no profiling. |
| Gustafson's Law | When workload size grows, redesign around scalable decomposition and acceptable approximation. | Assuming fixed workload; ignoring batch/window size and data growth. |
| Metcalfe's Law | For network products/platforms, model value and risk as connections grow. | Integration surface grows without governance; network effects assumed but not seeded. |

## Design laws

| Law | Agent move | Red flags |
|---|---|---|
| YAGNI | Defer unneeded features and abstractions. Keep extension points narrow and justified. | "We might need it someday"; configuration for imaginary users. |
| DRY | Remove duplicated knowledge, not necessarily duplicated text. Centralize facts that must change together. | Copy-pasted business rules; over-abstracted code that hides simple differences. |
| KISS | Prefer clear, boring, and direct designs. Explain why any complexity is necessary. | Architecture requires a diagram just to explain the happy path. |
| SOLID Principles | Use as local object/module design heuristics, not religion. Optimize maintainability and substitutability. | Giant classes, hidden dependencies, brittle inheritance, impossible tests. |
| Law of Demeter | Reduce coupling by limiting knowledge of distant collaborators. | Chains like `a.b().c().d`; feature code navigating internals of other modules. |
| Principle of Least Astonishment | Match user/developer expectations and ecosystem conventions. | Surprising defaults, inconsistent naming, hidden side effects, nonstandard APIs without reason. |

## Decision laws

| Law | Agent move | Red flags |
|---|---|---|
| Dunning-Kruger Effect | Calibrate confidence. Seek expert review in unfamiliar domains. | Confident claims without evidence; no humility around hard distributed/security/data problems. |
| Hanlon's Razor | Diagnose systems and incentives before blaming people. | Incident reviews focus on individuals; no process/tooling fixes. |
| Occam's Razor | Prefer simpler explanations until evidence requires complexity. | Root cause theories with many assumptions; solving the wrong problem. |
| Sunk Cost Fallacy | Reassess based on future value and switching cost, not past investment. | "We've already spent six months"; no kill criteria. |
| The Map Is Not the Territory | Validate diagrams, docs, models, and metrics against reality. | Architecture docs disagree with production; no telemetry or code inspection. |
| Confirmation Bias | Actively seek disconfirming evidence and alternative explanations. | Only benchmark happy path; only ask supporters; ignored incident data. |
| Hype Cycle & Amara's Law | Separate short-term overhype from long-term structural impact. Pilot before standardizing. | Adopting tech because it is hot; rejecting tech because early hype disappointed. |
| Lindy Effect | Give proven, boring technology extra weight when requirements are ordinary. | Novel stack for commodity needs; dismissing battle-tested tools. |
| First Principles Thinking | Rebuild the argument from constraints, physics, economics, and user needs. | Cargo-cult architecture; framework chosen before problem defined. |
| Inversion | Ask how the system would fail, disappoint users, or become unmaintainable, then design against that. | No pre-mortem; no abuse cases; no rollback. |
| Pareto Principle | Find the small set of causes producing most impact. Focus effort there first. | Equal attention to low-impact edge cases; no prioritization by impact. |
| Cunningham's Law | Use deliberately proposed drafts to elicit correction, but label them as drafts. | Waiting for perfect clarity; debates with no concrete proposal. |

## Combined law patterns

### When the user asks for microservices

Apply Conway, Distributed Fallacies, CAP, Hyrum, Leaky Abstractions, Bus Factor, Testing Pyramid, Goodhart, and Cost/operability checks. Default answer: modular monolith or service extraction only when team ownership, independent deployability, scaling, compliance, or release cadence demands it.

### When the user asks for a rewrite

Apply Second-System, Sunk Cost, Gall, Lehman, Technical Debt, Broken Windows, Unintended Consequences, and Inversion. Default answer: incremental strangler path unless the current system cannot be safely changed, cannot meet existential requirements, or the migration surface is smaller than continued patching.

### When the user asks for performance

Apply Premature Optimization, Amdahl, Gustafson, Pareto, Gilb, Goodhart, and Kernighan. Default answer: define SLO/workload, measure, identify bottleneck, optimize algorithm/data path, validate under load, then simplify.

### When the user asks for estimates

Apply Hofstadter, Ninety-Ninety, Parkinson, Brooks, Goodhart, Price, Bus Factor. Default answer: range estimate with milestones, risk register, scope cuts, integration/operationalization work, and explicit assumptions.

### When the user asks for quality/code review

Apply Boy Scout, Broken Windows, Technical Debt, Testing Pyramid, Pesticide Paradox, Kernighan, DRY, KISS, SOLID, Demeter, Least Astonishment. Default answer: prioritized findings with small safe patches, not a vague best-practices essay.
