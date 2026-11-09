---
name: product-wrangler
description: >-
  Autonomously turns an existing runnable web app that feels unfinished,
  incoherent, prototype-like, or unlike the product it should be into a bounded,
  evidence-backed, substantially better product. Use for broad end-to-end
  requests such as "wrangle this app," "make this feel finished," "turn this
  prototype into a real product," or "fix what this app should actually be."
  Includes product inference, workflow repair, information architecture, visual
  direction, implementation, browser critique, and before/after verification.
  Do not use for greenfield builds, narrow isolated UI fixes, review-only audits,
  design concepts without implementation, or backend-only work.
---

# Product Wrangler

## Objective

Turn an existing runnable web application into the product it should be for its
primary user and job.

Do not merely restyle the current interface. Infer product intent from ranked
evidence, bound the active product surface, repair the most consequential product
and interface defects, and prove improvement by replaying the same user journeys
before and after.

A polished version of the wrong product is a failure. A completed checklist
without observable product improvement is also a failure.

## Authority boundary

This skill changes execution discipline, not authority.

Use only the repository, tools, environments, accounts, and actions already
authorized by the user and host. Never treat this skill as permission to:

- deploy to production
- modify production or personal data
- create accounts or credentials
- change authentication, authorization, billing, or security boundaries
- send email, notifications, messages, webhooks, or publications
- enqueue real jobs or trigger external workflows
- purchase, subscribe, publish, merge, or release
- discard unrelated user changes

Proceed autonomously through reversible repository work and proven-safe local or
sandbox verification. Stop or downgrade to a non-mutating path when safety cannot
be established.

## Trigger boundary

Use this skill when the requested unit is a broad improvement to an existing web
application and the user expects implementation, not just advice.

Typical triggers include:

- "Wrangle this app and make it what it should be."
- "This works, but it feels half-baked. Finish it properly."
- "Make this prototype feel like a real product."
- "Figure out what is wrong with the product and fix it end to end."

Do not activate for:

- a new or greenfield application
- a single component, spacing issue, color change, or isolated bug
- a review, critique, or report where implementation is not requested
- a screenshot-to-code or design-concept-only task
- backend, infrastructure, data, or API work with no product-surface mandate

A broad request remains in scope when the app needs a small local repair before it
can run. Do not convert a genuinely greenfield task into Product Wrangler work.

## 0. Safe-execution preflight

Complete this preflight before opening mutating browser flows or making broad
changes.

### Repository state and rollback

Identify and record:

- repository root
- current branch or worktree
- `git status --short`
- unrelated modified, staged, or untracked files
- the rollback boundary for this task

Do not overwrite, revert, reformat, stage, or absorb unrelated user work. If the
worktree is dirty, separate task-owned files from unrelated files. Continue only
when changes can be isolated safely. If a required file overlaps uncertain user
work, preserve it and report the collision instead of guessing.

### Runtime and service topology

Identify and record:

- local start and validation commands
- runtime mode and loaded environment files
- frontend base URL
- backend, database, storage, auth, analytics, and third-party endpoints
- whether localhost proxies to any shared or production service
- available browser tooling and credentials

Localhost is not proof of a sandbox. Inspect configuration and observed network
traffic before concluding that mutations are safe.

### Data and outbound effects

Classify the data used by the app as one of:

- fixtures or seeded disposable data
- isolated local data
- sandbox or test-service data
- shared development data
- production, personal, customer, or unknown data

Identify every reachable external effect, including:

- email and notifications
- billing and payments
- publishing and social posting
- queues, jobs, and automations
- uploads and permanent storage
- webhooks and integrations
- account, permission, and identity changes
- destructive edits or deletes

### Select the verification mode

Choose and record one mode:

1. **Safe mutation** - Mutating journeys may run only with fixtures, disposable
   accounts, isolated local data, or proven sandbox services.
2. **Read-only browser** - Inspect and navigate, but do not submit mutations or
   trigger outbound effects.
3. **No browser verification** - Browser tooling, credentials, or a runnable app
   are unavailable. Repository work may continue where safe, but product-quality
   completion cannot be claimed.

Exact authorization for one side effect does not authorize adjacent effects.
Missing proof means read-only, not probably safe.

## 1. Bound the active product surface

Define the **primary product surface** before auditing the whole application.

The surface is the smallest complete set of routes, workflows, states, and shared
components required to deliver the primary user job end to end. Include entry,
completion, failure recovery, and the immediately supporting navigation or setup
needed for that job.

Record:

- primary user
- primary user job
- successful observable outcome
- in-scope routes and journeys
- shared components that materially affect those journeys
- explicit non-goals
- lower-priority residual surfaces to report, not absorb

Do not chase every defect in a large application. Finish the named surface
completely, then report residual work separately.

## 2. Infer the product from ranked evidence

Use this hierarchy when sources conflict:

1. Current user brief and explicit acceptance criteria
2. Current product or domain contracts and business invariants
3. Tests, data model, and functioning workflows
4. Representative content and data
5. Existing interface and styling

Higher-ranked evidence wins unless there is concrete evidence that it is stale or
incorrect. Do not silently average contradictory sources. The existing interface
is evidence, but it is the weakest source because it may encode accidental design.

### Build the evidence-linked product thesis

Create a concise working record containing:

- primary user and context
- primary job and successful observable outcome
- supporting jobs
- evidence for each claim, using paths, tests, routes, data fields, or current
  user requirements
- business invariants that must not change
- contradictions between sources
- assumptions and confidence level for each material assumption
- non-goals
- bounded product surface
- visual-direction rationale based on audience, domain, task density, content,
  and credible brand signals

Do not choose a visual direction merely by avoiding gradients, cards, or other
common model habits. Explain why the direction fits this product and its use.

### Try to disprove the thesis

Before implementation:

1. State the strongest plausible alternative product thesis.
2. Identify evidence that contradicts the selected thesis.
3. Explain why the selected thesis still fits the ranked evidence better.
4. Lower confidence or narrow scope when the evidence remains ambiguous.

Do not proceed confidently through a material ambiguity that could produce a
different product. Preserve current behavior and report the ambiguity when the
repository cannot resolve it and the authority boundary does not permit guessing.

## 3. Establish the baseline and workflow ledger

Run available baseline checks before material edits and distinguish pre-existing
failures from regressions.

When safe and available:

- run the application
- capture representative desktop and mobile screenshots
- inspect console errors, runtime warnings, and failed requests
- exercise every primary journey in the bounded surface
- record the starting data and state needed to replay each journey

Create a compact workflow ledger with one row per primary journey:

| Field | Required content |
| --- | --- |
| Primary user outcome | What the user is trying to accomplish |
| Baseline behavior or failure | What observably happens before the change |
| Expected observable result | What must be true afterward |
| Selected change | The smallest coherent product or implementation change |
| Post-fix evidence from the same journey | Browser, state, test, screenshot, or output evidence |
| Remaining uncertainty | Anything still inferred or unverified |

Populate the first four fields before implementation. Populate post-fix evidence
only after replaying the same journey from a comparable starting state.

Every major change must be traceable to:

- the primary or supporting user job it serves
- the ranked evidence supporting it
- the expected observable result
- the risk or invariant it must preserve

Do not invent user research, analytics, conversion gains, or certainty that the
available evidence does not provide.

## 4. Audit and prioritize

Audit only the bounded surface, plus shared behavior that directly affects it.
Prioritize in this order:

1. inability to complete the primary job
2. incorrect state, data, or business behavior
3. misleading hierarchy, navigation, labels, or affordances
4. missing loading, empty, partial, validation, error, recovery, success, or
   destructive-action states
5. inaccessible or unusable interaction
6. responsive failure and information-density mismatch
7. visual incoherence and weak product credibility
8. low-impact decorative polish

Identify dead controls, fake interactions, placeholders, unfinished paths,
meaningless metrics, unrealistic data, generic copy, duplicated concepts, and
ornament that obscures the user job.

Prefer removing confusion over adding interface. Do not redesign for novelty.

## 5. Implement the bounded product pass

Implement the smallest complete set of changes that satisfies the workflow ledger
and product thesis.

Preserve:

- current business invariants
- data integrity
- security and permission boundaries
- external contracts
- functioning repository conventions

Change when evidence supports it:

- information architecture
- route or page responsibilities
- workflow sequence
- navigation
- copy and labels
- component boundaries
- visual system
- responsive behavior
- interaction and feedback patterns

Reuse the repository's framework, styling system, components, tokens, icons,
routing, state, and data-access patterns. Do not introduce a second styling system
or component library. Avoid broad unrelated refactors, speculative abstraction,
and dependencies that do not materially improve the bounded product outcome.

Visual decisions must follow the recorded audience, domain, task density, content,
and brand evidence. A generic modern redesign that could belong to any product
does not satisfy this skill.

Use the browser throughout implementation when the selected verification mode
permits it. Never use real external side effects merely to demonstrate that a
control works.

## 6. Prove the result through journey replay

Verification is outcome-based, not activity-based.

### Replay the same journeys

For every workflow-ledger row:

1. Restore a comparable starting state and data set.
2. Replay the same journey used for the baseline.
3. Record the actual post-fix result.
4. Compare it with the expected observable result.
5. Update remaining uncertainty honestly.

Screenshots prove appearance, not completion. Pair them with observed navigation,
state changes, validation, persistence, recovery, or test results relevant to the
journey.

### Browser critique

When browser verification is available and safe, inspect the bounded surface at
approximately:

- 1440x900
- 1024x768
- 390x844

Check:

- first-use comprehension and primary-action discoverability
- navigation and back, cancel, close, and escape behavior
- forms, validation, filters, search, sorting, dialogs, and drawers
- loading, empty, partial, error, recovery, success, disabled, and destructive
  states
- keyboard navigation, focus order, accessible names, semantics, and contrast
- overflow, truncation, density, mobile collapse, and touch usability
- console output, failed requests, runtime warnings, and unintended effects

Critique the rendered result against the product thesis and workflow ledger, not
against the agent's preference for a particular visual style.

A repair cycle that changes only cosmetics while the primary journey outcome
remains unchanged does not count as product improvement.

### Cold-start pass

Run a final cold-start pass in a fresh browser context when browser tooling is
available:

- start from the app's real entry point
- clear task-created local session state unless persistence is itself under test
- use a disposable or sandbox account when authentication is required
- verify first load, first-use comprehension, empty or initial states, and the
  primary journey without relying on implementation knowledge

Do not use a production or personal account to satisfy the cold-start gate.

### Revisit the thesis

After implementation, reread the evidence-linked product thesis and ask:

- Did new evidence contradict the original thesis?
- Does every major change serve the primary user job?
- Were any changes justified only by visual taste or implementation convenience?
- Did the bounded surface remain bounded?
- Is the result a better product, or only a more polished interface?

Revise or revert unsupported changes instead of defending the initial plan.

## 7. Engineering validation

Run all relevant available checks, starting narrow and ending with the repository's
required validation:

- typecheck
- lint
- unit tests
- integration tests
- end-to-end tests
- production build

Do not claim a check passed unless it was executed and its result was observed.
Record pre-existing failures separately.

## Completion states

Use exactly one completion state:

### COMPLETE

Use only when all applicable conditions are true:

- the safe-execution preflight is recorded
- the primary product surface is explicit and complete
- the product thesis is evidence-linked, contradiction-aware, and revisited
- every primary journey has before and after evidence in the workflow ledger
- the expected observable results were met
- the same journeys were replayed from comparable starting states
- the cold-start pass succeeded when browser verification was available
- no unauthorized mutation or external effect occurred
- relevant engineering checks passed, or pre-existing failures are isolated and
  do not invalidate the result
- no known critical or high-severity product defect remains in the bounded surface
- residual work is outside the bounded surface or genuinely lower priority

### PARTIAL

Use when useful implementation is complete but one or more proof gates are absent,
including missing browser tooling, credentials, safe test data, comparable
baseline state, or a required external dependency.

State exactly what was implemented and what prevents product-quality completion.
Do not relabel partial verification as production readiness.

### BLOCKED

Use when the task cannot proceed safely or coherently without expanding authority,
overwriting unrelated work, guessing through a material product ambiguity, or
triggering an unauthorized external effect.

## Final report

Report concisely:

- completion state: COMPLETE, PARTIAL, or BLOCKED
- bounded product surface and explicit non-goals
- evidence-linked product thesis and confidence
- contradictions and material assumptions
- safe-execution mode, data class, and external-effect boundary
- primary workflow ledger with before and after evidence
- major changes and the evidence supporting each
- routes, workflows, and viewport sizes exercised
- cold-start result
- files changed
- commands and checks actually run
- pre-existing failures
- residual work outside the bounded surface
- remaining uncertainty and anything not verified

Never claim that the application is production-ready unless production readiness
was explicitly in scope and independently supported by the required evidence.
