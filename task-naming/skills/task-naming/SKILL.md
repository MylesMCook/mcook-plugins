---
name: task-naming
description: >-
  Manually name, rename, audit, or standardize Codex task titles when the user
  explicitly invokes $task-naming. Support one current task, all user-facing
  root tasks under a project folder, or all user-facing root tasks on one
  machine. Do not invoke implicitly or use for filenames, variables, branches,
  commits, tickets, or ordinary conversation.
---

# Task Naming

Rename Codex tasks only when explicitly invoked. Use native task operations;
do not run background maintenance.

## Select the scope

Choose exactly one scope from the user's request:

- **Current task:** target only the calling root task.
- **Project folder:** target user-facing root tasks whose recorded working
  directory is the requested folder or a descendant of it.
- **Machine:** target user-facing root tasks on the requested Codex host. Use
  the current host when the user does not name another one.

Exclude subagents, guardians, maintenance workers, ephemeral side
conversations, and empty-title records. Include archived tasks only when the
user explicitly asks for archived history. Never let a machine-wide request
spill onto another connected host.

If the host cannot prove the inventory is exhaustive, label the observed scope
as partial instead of claiming all tasks were covered.

## Inspect with native operations

1. Discover the native task-management operations available on the host.
2. Use the current-task operation for current-task scope.
3. For project or machine scope, list candidate tasks and read enough context
   to identify each dominant objective.
4. Preserve the recorded host, project path, root-task status, and archive
   state while filtering.

Do not inspect or edit Codex databases, session files, rollout logs, plugin
state, or App Server sockets. Do not start scripts, hooks, subprocesses, MCP
servers, or model evaluators for title maintenance.

## Build each title

Put the differentiating action first:

```text
Verb object — Context
```

- Start with a concrete verb and its object. Prefer verbs such as `Explore`,
  `Plan`, `Draft`, `Build`, `Review`, `Validate`, `Release`, `Document`,
  `Standardize`, `Clean up`, `Repair`, and `Remove`.
- Append ` — Context` only when a stable product, workstream, or domain label
  makes the title easier to distinguish outside its project. Omit context that
  the Codex project or host already shows.
- When using context, use one em dash with one space on both sides.
- Use sentence case and preserve exact capitalization for proper names,
  product names, versions, and technical identifiers.
- Aim for 25–45 characters. Treat 60 as a soft ceiling and never exceed 80.
- Describe the current dominant objective, not the opening prompt. Rename when
  that objective changes; ignore quick detours and incidental questions.
- Exclude dates, machine names, paths, URLs, ticket IDs, raw prompt text,
  status labels, and numbered suffixes.
- Remove conversational framing such as `Help me`, `Can you`, `Please`,
  `Continue`, and `I want`.
- Keep an accurate existing title instead of renaming for its own sake.
- Mark an unclear task `needs context` rather than inventing a title.

Resolve collisions with the smallest truthful object distinction, then add a
context suffix only if needed. Do not append numbers, dates, or machine labels.

## Apply and verify

Treat a direct rename request as authorization; do not ask for a second
confirmation. If the user asks only for an audit or proposal, return a mapping
without changing anything.

1. Record the eligible count and proposed old-to-new mapping.
2. Apply only changed titles through native task operations.
3. Re-read every changed task and compare the stored title exactly.
4. Preserve archive state. If an explicitly included archived task requires an
   unarchive/rename/rearchive sequence, use it only when all three operations
   are native and verify the final state.
5. Report `eligible`, `changed`, `unchanged`, `deferred`, and `failed` counts.

When no native rename operation is callable:

- For current-task scope, return the title and `/rename <title>`.
- For project or machine scope, return the mapping and say that no titles were
  changed.

Never claim completion from a write response alone.
