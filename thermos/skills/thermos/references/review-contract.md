# Shared review contract

Use this contract for paired Thermos and three-lens adversarial reviews. The
entrypoint selects reviewer count, rubrics, repair policy, and verdict format.

## Resolve one scope

Choose the first applicable mode:

1. Explicit files, plan, commit range, or diff supplied by the user.
2. Explicit pull request, using its base and head.
3. Branch review, using the repository's detected remote-default branch and the
   merge base with `HEAD`. A tracking upstream may identify the reviewed head,
   but it is not the target base unless explicit metadata says so.
4. Uncommitted review, only when the user asks for the worktree or current
   changes. Include staged, unstaged, and untracked files.

Do not assume `main` when Git or pull-request metadata can identify the base.
Do not fetch, switch branches, or mutate the worktree merely to resolve scope.

For branch and pull-request review, exclude dirty worktree changes by default.
Inspect committed content from Git objects when a reviewed path is also dirty.
For worktree review, enumerate untracked files instead of relying on `git diff`
alone.

Record a compact scope contract before delegation:

- user intent and review mode
- repository root, base, head, and merge base when applicable
- included changed files and explicit exclusions
- a scope identity based on `HEAD`, status, and the relevant diff or file hashes
- checks already run and their results

Build the scope identity from only included state:

- committed range, branch, or pull request: immutable base and head commit SHAs
- worktree: `HEAD` plus hashes of the staged diff, unstaged diff, and sorted
  untracked path and content pairs
- explicit files or plans: sorted included path and content hashes
- supplied patch or non-commit diff: a hash of the exact supplied content

Never include excluded paths in the identity.

If ambiguity would materially change what gets reviewed and local context does
not resolve it, ask one concise question.

## Verify and synthesize

Treat reviewer output as candidate findings, not facts.

1. Recheck every candidate against the exact scoped state. Trace the affected
   path and run a narrow check when that is the cheapest reliable proof.
2. Reject stale, out-of-scope, duplicate, speculative, or unsupported claims.
   Reviewer agreement is a clue, not proof.
3. Recompute the scope identity after all required reviews. If reviewed state changed,
   rerun against the new state or state clearly that no current verdict is
   possible.
4. Only after all independent reviews, read existing pull-request discussion
   when a pull request exists and material findings remain. Validate and
   attribute any useful external finding. Do not post anything unless asked.
5. Order the verified findings by priority:
   - `P0`: immediate, broadly blocking failure or critical security impact
   - `P1`: high-impact defect that should block merge or release
   - `P2`: meaningful correctness or maintainability defect to fix normally
   - `P3`: bounded, non-blocking improvement

Every reported finding needs a priority, confidence score from `0` to `1`,
exact file and line range, impact, traced evidence, and concrete fix direction.
