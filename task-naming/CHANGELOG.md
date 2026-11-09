# Changelog

## 0.5.2 - 2026-08-24

- Added the portable Agent Plugins 1.0.0 manifest while retaining the Codex
  compatibility overlay.

## 0.5.1 - 2026-07-21

- Keep the bundled contract suite runnable from the versioned installed cache,
  where the marketplace catalog is intentionally external to the plugin.

## 0.5.0 - 2026-07-21

- Replace subject-first titles with action-first `Verb object` titles and an
  optional `— Context` suffix.
- Put the most distinguishing words before sidebar truncation, omit redundant
  project context, and use sentence case.
- Aim for 25–45 characters, keep 60 as a soft ceiling, and rename only when
  the conversation's dominant objective changes.

## 0.4.0 - 2026-07-16

- Remove automatic title maintenance, the `UserPromptSubmit` hook, the App
  Server bridge, the MCP tool, evaluator subprocesses, plugin state, and every
  related runtime artifact.
- Make `$task-naming` explicitly invoked only, with current-task,
  project-folder, and machine-wide scopes.
- Use native Codex task operations when available, verify every change, and
  fall back to `/rename` or a non-mutating mapping when native mutation is not
  available.
- Replace the runtime-coupled test suite with a small skills-only package
  contract.

## 0.3.4 - 2026-07-15

- Replace the unsafe “newest cache” picker with a trusted runtime plugin root
  and a fail-closed fallback that accepts only one complete, non-symlinked,
  manifest-consistent final SemVer release.
- Embed that launcher in the trusted hook definition and force a silent zero
  exit even when Python, the cache, or the selected hook is unavailable.
- Retain a private diagnostic until a healthy evaluation checkpoint completes,
  rather than clearing it on an unrelated ordinary prompt.
- Add exact-command and regression coverage for missing, broken, ambiguous,
  prerelease, symlinked, and healthy cache states.

## 0.3.3 - 2026-07-14

- Replace the version-pinned hook command with a small portable launcher that
  resolves the newest installed Task Naming cache at invocation time.
- Keep an absent or replaced cache as a silent no-op, preventing an active
  task's old cache path from blocking a user message after a plugin upgrade.
- Use the Windows `py -3` override with the same portable launcher instead of
  a path expanded on another machine.

## 0.3.2 - 2026-07-14

- Speak WebSocket JSON-RPC through `codex app-server proxy`, which is a raw
  byte tunnel to the Desktop App Server control socket rather than a JSON-lines
  protocol endpoint.
- Validate the HTTP upgrade and WebSocket proof, mask client frames, and handle
  fragmented messages and heartbeats before issuing title reads or writes.
- Add regression coverage for the actual proxy transport so a protocol mismatch
  cannot silently turn automatic maintenance into an App Server timeout.

## 0.3.1 - 2026-07-14

- Route automatic and manual App Server operations through `codex app-server
  proxy` so a successful rename reaches the running Desktop task service.
- Require a post-write `thread/read` with an exact title match; unverified
  writes are unavailable rather than reported as changed.
- Validate the hook session UUID before touching plugin state, defer every
  first observed prompt even when it contains objective-shift wording, and use
  collision-safe temporary state files.
- Read current task metadata only, rather than full long-thread turns, so
  automatic checkpoints remain bounded as a conversation grows.
- Prefer the hook's active model, allow `TASK_NAMING_MODEL` as an explicit
  override, and let `codex exec` choose its normal default when neither exists.
- Keep UI output silent while retaining a minimal private failure code for
  diagnosis, and add regression coverage for proxy routing, verification,
  malformed IDs, model selection, and failure diagnostics.

## 0.3.0 - 2026-07-13

- Replace model-compliance-based title maintenance with a deterministic
  `UserPromptSubmit` command hook.
- Reassess on the second prompt, explicit objective-shift language, and every
  eighth prompt using an isolated ephemeral Luna decision.
- Read and write only through the documented local App Server, keep first-turn
  naming untouched, and remain silent on routine skips and failures.

## 0.2.5 - 2026-07-13

- Load the exact bundled title tool once when Codex defers MCP tools in a
  non-interactive resume.
- Keep broad tool discovery prohibited and preserve the single rename-call
  boundary.

## 0.2.4 - 2026-07-13

- Route non-interactive `bypassPermissions` resumes directly to the bundled
  title bridge before any unsupported Desktop dynamic call.
- Keep normal Desktop modes on the native task-service path for immediate
  sidebar refreshes.

## 0.2.3 - 2026-07-13

- Fall back once to the bundled title bridge when a non-interactive CLI host
  rejects the outer Desktop-tool call before its code can run.
- Preserve native-first Desktop routing and the existing no-retry boundary
  after a native call actually executes.

## 0.2.2 - 2026-07-13

- Prefer the current Codex Desktop task operations so successful renames update
  the running app's sidebar immediately.
- Keep the bounded App Server bridge only as a portability fallback when native
  task operations are absent or fail.
- Add regression coverage for native-first routing and stale-sidebar avoidance.

## 0.2.1 - 2026-07-13

- Recover from App Server cold-start timeouts with one fresh, bounded,
  idempotent internal attempt.
- Return quiet structured timeout diagnostics and permit exactly one native
  title-operation fallback when the bridge remains unavailable.
- Allow a fresh attempt after resume or compaction instead of making one
  transient bridge failure permanent for the task.

## 0.2.0 - 2026-07-13

- Adopt a clean semantic version for the finished automatic task-naming
  release.

## 0.1.0+codex.20260713194401 - 2026-07-13

- Remove successful MCP result prose while retaining structured status for
  hosts that inspect it.
- Keep the bundled contract suite green both in the source repository and in
  Codex's isolated installed-plugin cache.

## 0.1.0+codex.20260713192852 - 2026-07-13

- Pin automatic code-mode maintenance to the loaded
  `mcp__task_naming__maintain_task_title` namespace.
- Require the MCP tool's exact camel-case `threadId` argument and reject the
  ineffective `session_id` and `thread_id` near misses in contract coverage.

## 0.1.0+codex.20260713191522 - 2026-07-13

- Add one approved `maintain_task_title` MCP tool for hosts without native
  current-task title operations.
- Route atomic read, root-task guard, exact comparison, and conditional rename
  through the documented local Codex App Server.
- Keep the fallback dependency-free and short-lived: no daemon, timer,
  transcript parsing, network service, or direct task-storage access.
- Preserve the first-turn delay and objective-drift hysteresis while reducing
  later maintenance to at most one tool call.
- Add contract coverage for exact App Server methods, no-op behavior, title
  validation, and child-task protection.

## 0.1.0+codex.20260713181828 - 2026-07-13

- Add a lightweight `SessionStart` hook for automatic current-task naming.
- Keep titles aligned with the dominant objective as long conversations evolve.
- Reassess on resume and compaction without per-prompt or Stop-hook churn.
- Preserve silent no-op behavior when a host exposes no native title operation.
- Limit automatic maintenance to one title read and, only when needed, one
  rename. Do not retry or re-read after a successful native write.
- Remove the routine hook status message and add an installed multi-turn
  acceptance scenario.
- Defer automatic writes until the second user turn to avoid Codex's task-title
  creation race.
- Defer all title-tool activity during the first user turn, including discovery
  and reads, so new tasks show no pointless maintenance row.
- Keep automatic maintenance silent so the standard Codex tool activity is the
  only visible UI.
- In code-mode hosts, perform the read, comparison, and optional write inside
  one orchestrator call without a separate tool-discovery pass.
- Pin the current Codex code-mode argument shapes so automatic reads and writes
  use `threadId` instead of silently ineffective near-miss parameters.
- Treat app-created delegated tasks as user-owned roots unless the host
  explicitly marks them as subagent or maintenance records.

## 0.1.0 - 2026-07-13

- Add the `Subject — Outcome` task-title convention.
- Add current-task, project-audit, and authorized batch-apply workflows.
- Use native task tools when available and `/rename` as the honest CLI
  fallback.
- Keep v1 skills-only with no hook, app-server client, or private-state access.
