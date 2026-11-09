# Thermos evals

These are maintainer-facing smoke cases. Run them in fresh Codex tasks after
installing the marketplace plugin. There is no repo-local fake eval runner.

## Trigger cases

| Prompt | Expected behavior |
| --- | --- |
| `Run Thermos on this branch.` | Invoke `thermos`, review committed branch changes, exclude dirty state, and run two reviewers. |
| `Give this PR a paired correctness and maintainability review.` | Invoke `thermos` and use the pull-request base and head. |
| `Review my uncommitted changes with both Thermos lenses.` | Invoke `thermos` and include staged, unstaged, and untracked files. |
| `Double-review these three files before I commit.` | Invoke `thermos` with an explicit file scope. |
| `Work until Thermos is happy.` | Invoke `thermos`, fix only verified findings, test, and run fresh pairs until the exit condition. |
| `Use $thermos:thermo-nuclear-review on this PR.` | Run only the installed plugin's correctness and security lens. |
| `Use $thermos:thermo-nuclear-code-quality-review on this diff.` | Run only the installed plugin's maintainability lens. |

## Near misses

| Prompt | Expected behavior |
| --- | --- |
| `Review this typo fix.` | Use ordinary review, not Thermos. |
| `Run a deep security scan of the whole repository.` | Use a repository security-scan workflow, not Thermos. |
| `Fix the failing unit test.` | Implement the fix without invoking Thermos unless separately requested. |
| `Can you simplify this function?` | Treat as refactoring, not a change-scoped Thermos review. |

## Paired-review assertions

For every positive `thermos` case, verify:

1. The parent states one scope contract and any excluded dirty state.
2. Exactly two actual review-only child threads start through the host's native
   subagent facility in the same wave; the parent does not simulate either
   review.
3. Each receives its exact role contract from
   `skills/thermos/references/subagent-contract.md` and the matching sibling
   rubric.
4. Each reviewer reads the exact sibling skill path from the installed plugin
   and receives the same scope identity.
5. Reviewers inspect independently and do not spawn nested agents or edit.
6. The parent waits for both and rechecks the scope identity.
7. Every final finding has `P0` through `P3`, a confidence score from `0` to
   `1`, an exact line range, impact or structural cost, evidence, and a fix
   direction.
8. The parent independently verifies findings and removes unsupported or
   duplicate claims.
9. The final answer lists checks, residual risk, one verdict, and whether
   both native child threads ran.

For the repair-loop case, also verify that the parent owns all writes, runs
checks after each fix, and uses a fresh reviewer pair for the next round.

## Fresh-session acceptance

Use an isolated harmless repository and the installed plugin. Keep legacy
files recoverable and exclude their paths for the probe so a duplicate cannot
satisfy the test. Verify which installed skill and reference paths are read.

- Ordinary Thermos launches exactly two native reviewers in one wave.
- Explicit adversarial review launches exactly three, with Skeptic, Architect,
  and Minimalist rubrics. Plans use an explicit artifact scope.
- Required reviewers complete before synthesis; missing coverage or scope drift
  prevents a positive verdict.
- No reviewer edits, delegates further, posts externally, or performs fixes.
- The parent verifies findings and the scope identity, then reports remaining
  gaps. A repair request uses fresh review children after each parent fix.
- A routine typo fix, prose rewrite, and repository security scan select other
  workflows. Never claim a routing-only probe proves native concurrency.

Run the portable package, OpenAI plugin, and per-skill validators before release.
A fresh process must report installed paths rather than source-checkout paths.
