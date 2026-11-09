---
name: adversarial-review
description: >-
  Run an independent Skeptic, Architect, and Minimalist review of a patch,
  branch, plan, plugin, or bounded file set when the user explicitly requests
  adversarial or three-reviewer review. Do not trigger for ordinary review,
  paired Thermos review, implementation, or a repository security scan.
---

# Adversarial review

This is Thermos's three-lens mode. Start exactly three independent native
review-only children and return one verified verdict. An explicit invocation
authorizes the review, not implementation, deployment, or external messages.

## Establish the shared contract

Read [the shared review contract](../thermos/references/review-contract.md) and
[the child contract](../thermos/references/subagent-contract.md). Apply their
scope, evidence, no-write, independence, and synthesis rules to three children.
Use only the three rubrics below; do not also launch the paired workflow.

Infer the intended target from the request and current context. Plans and
explicit files use content hashes; patches and branches use the corresponding
shared-contract identity. Preserve unrelated dirty work. With no identifiable
target, return CONTESTED with NO_REVIEWABLE_TARGET.

## Three independent lenses

Give every child the same bounded scope and checks already run, plus only its
assigned rubric:

- **Skeptic:** trace assumptions against reachable behavior. Investigate failure
  inputs, authorization, races, invalid state, data loss, and unsupported safety
  claims. Report a reproducible failure or a concrete missing requirement.
- **Architect:** inspect ownership, coupling, compatibility, rollout, and
  recovery. Identify where the proposed change breaks an existing boundary or
  leaves a necessary migration step undefined. Tie concerns to the actual system.
- **Minimalist:** identify unnecessary state, branching, abstraction, or scope.
  Show a smaller solution that still meets the requirements. Do not propose
  deletion that loses behavior, observability, safety, or verification.

Use fresh unreserved task names for each invocation. Inspect supported spawn
options instead of assuming a particular API, model, or profile. When supported,
use `fork_turns: "none"` and send a self-contained scope packet. Launch all three
in one wave; never simulate missing reviewers or substitute a sequential pass.
Reviewers may run useful non-destructive checks but must not edit, post, deploy,
delegate further, or read each other's findings.

Bound the review to the task. Inspect progress around three minutes and stop
stalled work by five minutes unless the user requested deeper coverage. Missing
or incomplete reviewers must be disclosed; elapsed time does not establish PASS.

## Verify and report

Wait for the required handoffs and apply the shared contract's verification and
scope-drift check. For each retained finding, include priority, location, impact,
evidence, originating lens, and the parent's acceptance rationale. Explain
rejected claims only when a material disagreement affects the verdict.

Report scope, findings, checks, coverage, and the smallest next action:

- **REJECT:** at least one verified P0 or P1 finding blocks the change.
- **CONTESTED:** a required reviewer failed, scope drifted, or material evidence
  is unresolved. Name SUBAGENT_UNAVAILABLE, SUBAGENT_FAILED, TIMEOUT,
  MALFORMED_OUTPUT, INCOMPLETE_COVERAGE, or NO_REVIEWABLE_TARGET as applicable.
- **PASS:** all three lenses completed and no blocking finding survives.
  Explicitly list any remaining P2/P3 work; PASS does not mean issue-free.

This mode is review-only. If fixes are requested, the parent may implement only
verified in-scope changes and then run a fresh review of the changed state.
