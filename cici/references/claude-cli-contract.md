# Claude CLI Contract

Codex controls the repo. Claude reviews, answers, or proposes.

Use `claude -p --permission-mode plan --tools "" --disallowedTools "Edit MultiEdit Write NotebookEdit Bash"`.

Do not use dangerous permission bypass flags or `--bare`; it skips OAuth/keychain auth.

Check that Claude launched before interpreting authentication. A missing executable
or launch error is not a logged-out account. Only when Claude reports logged out,
investigate sandbox OAuth/keychain access using the harness's permitted workflow.

Use `--dry-run` before sending context. Use `--no-git-context` until diff sharing is approved.
