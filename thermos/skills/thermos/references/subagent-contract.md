# Thermos native subagent contract

Read this before starting a Thermos child thread. It is the canonical
contract for the ordinary native subagents available to this plugin.

## Roles and rubrics

| Review lens | Rubric |
| --- | --- |
| Correctness and security | Exact supplied correctness/security rubric path |
| Maintainability | Exact supplied maintainability rubric path |

For paired review, start one child for each lens above in the same wave.
For adversarial review, the sibling entrypoint supplies three inline rubrics;
send each child its exact rubric text instead of a rubric file. All remaining
scope, independence, evidence, and no-write requirements apply unchanged.
Task names are labels;
specialization comes from the assigned rubric and role statement below. The
parent must use the host's native subagent-spawn tool; a prompt-only simulated
review is not a Thermos child thread.

## Shared child input

Give every child:

- the review mode and user intent;
- repository root, base, head, merge base, and scope identity when applicable;
- included paths and explicit exclusions;
- checks already run and their result;
- one exact absolute path to its assigned rubric, or the complete inline rubric.

When the runtime exposes `fork_turns`, set it to `"none"` and send this compact
input instead of the parent transcript.

Every child must:

1. Read its assigned rubric at the exact path or in the supplied packet before reviewing.
2. Inspect only the supplied scope, independently of its sibling.
3. Operate as a review-only child: do not edit, stage, commit, post comments,
   run destructive commands, or create external side effects.
4. Avoid nested delegation and do not read the other reviewer's result.
5. Return only candidate findings, checks inspected, and residual risk.
6. Never synthesize the parent verdict or propose work outside the scope.

## Correctness and security child

> Perform only the assigned Thermos correctness and security review. Trace
> reachable behavior, security, data integrity, availability, compatibility,
> and test coverage risks introduced or worsened by the supplied scope. Return
> evidence-backed candidate findings using the assigned rubric's format. Do not
> edit, delegate, or declare a final patch verdict.

## Maintainability child

> Perform only the assigned Thermos maintainability review. Look for structural
> complexity, wrong ownership, branching growth, type ambiguity, file sprawl,
> and weakened testability introduced or worsened by the supplied scope. Return
> evidence-backed candidate findings using the assigned rubric's format. Do not
> edit, delegate, or declare a final patch verdict.
