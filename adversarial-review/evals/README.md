# Adversarial Review evals

These are optional behavioral evals for deliberate live testing. They are not
the normal release gate: a positive case launches three full reviewer runs and
can take several minutes. There is no repo-local fake subagent runner.

## Fast release gate

Use static plugin validation, `tests/test_contract.py`, installed-version
inspection, and a byte-for-byte source/cache comparison for routine publishing.
Those checks prove the package and installed contract without spending three
model runs. Run the live cases below only when the user explicitly requests a
behavioral trio test.

## Test isolation

For an explicitly requested live eval, refresh and install the marketplace
bundle, then start a fresh task and invoke `@adversarial-review`. The retired
same-named standalone source must remain absent so the selected plugin identity
is unambiguous.

## Trigger cases

| Prompt | Expected behavior |
| --- | --- |
| `Use $adversarial-review on my current diff.` | Invoke the skill, resolve the worktree scope, and run three independent reviewers. |
| `Use $adversarial-review to challenge this implementation plan.` | Review the plan with all three lenses without editing it. |
| `Use $adversarial-review on commit <sha>.` | Review only that exact commit. |
| `Use $adversarial-review to review this branch against main.` | Resolve the branch range and preserve unrelated dirty state as excluded. |
| `Use $adversarial-review on the last turn only.` | Review only the last-turn boundary if the host can expose it; otherwise report the boundary gap rather than widening scope. |

## Near misses

| Prompt | Expected behavior |
| --- | --- |
| `Review this typo fix.` | Use an ordinary review, not the three-subagent workflow. |
| `Run a deep security scan of the whole repository.` | Use a repository security-scan workflow, not Adversarial Review. |
| `Fix the failing unit test.` | Implement the requested fix without invoking this review-only skill. |

## Assertions

For every positive case, verify that:

1. The parent records one intent and an explicit review scope.
2. Exactly three fresh native Subagent V2 children start in the same wave with
   one automatically allocated run number, such as `skeptic_r2`,
   `architect_r2`, and `minimalist_r2`. A repeated invocation in the same parent
   advances the run number for the full trio and never asks the user to start a
   new task.
3. Each reviewer avoids implementation and nested delegation, receives the same
   scope contract, uses targeted diagnostics when helpful, and returns either
   structured findings or `No material findings.`
4. The parent waits until all three settle or the adaptive deadline expires,
   then compares the pre/post source fingerprint and worktree state when Git is
   involved.
5. The final result names all three coverage statuses, evidence-backs retained
   findings, and returns exactly one `PASS`, `CONTESTED`, or `REJECT` verdict.
6. The current permission and approval mode does not block launch. Reviewers
   use inherited tools and automatic approval handling when available, without
   asking the user to configure reviewer mechanics.
7. The workflow prefers V2 `default` on `gpt-5.6-terra` with high reasoning
   when exposed, otherwise uses host defaults without asking.
8. The standard child wave gets three minutes, continues recent meaningful
   progress up to five total minutes, and interrupts stalled or over-budget
   children with reduced coverage.

## Static acceptance

Run from the repository root:

```sh
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py adversarial-review
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
if rg --hidden -n '[[:blank:]]$' adversarial-review; then exit 1; fi
git diff --check -- adversarial-review .agents/plugins/marketplace.json
if rg -n 'claude|run_in_background|subagent_type|codex[_-](skeptic|architect|minimalist)|/add-plugin|\.cursor-plugin' adversarial-review/skills adversarial-review/.codex-plugin adversarial-review/README.md adversarial-review/DESIGN.md; then exit 1; fi
python3 -m unittest adversarial-review/tests/test_contract.py
git status --short -- adversarial-review .agents/plugins/marketplace.json
```

The validators, JSON parse, diff check, and contract tests must pass. The two
no-match checks must produce no output. Status must contain only intended
Adversarial Review or marketplace changes; unrelated work remains excluded.
