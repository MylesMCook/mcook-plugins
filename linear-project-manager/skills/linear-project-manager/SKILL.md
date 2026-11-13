---
name: linear-project-manager
description: >-
  Keep meaningful repository development work aligned with Linear: map a repository,
  reuse or create outcome issues, resume tracked work, and record verification or
  blockers. Use for explicit Linear tracking or feature and bug work in a repository
  with an approved Linear mapping. Questions and trivial edits do not need new issues.
---

# Linear Project Manager

Linear holds project and issue state across machines. Apply this procedure when
invoked or when applicable repository instructions call for Linear tracking.
There are no automatic hooks; a task ending does not guarantee reconciliation.
Use the connected official Linear MCP tools. Discover their current schemas;
do not hard-code tool names or assume server availability from installation.

## Establish the destination and authority

Read applicable `AGENTS.md` and the user's current request. Reuse the repository's
approved Linear mapping: canonical repository URL, Linear team ID, project ID/URL,
and the explicit permission to maintain issues for meaningful work in that repo.
Use repository identity, not a machine-specific checkout path or folder basename.
Do not print or transmit credential-bearing Git URLs; strip credentials and query
parameters before comparing repository identity. Never send source or transcripts.

If the mapping is missing, identify candidate projects with bounded read-only
queries and ask once to confirm the destination and automatic issue-maintenance
scope. Do not guess between similarly named projects. Creating a project requires
explicit authorization. After approval, record a concise mapping in the existing
repo `AGENTS.md` (or create that file if authorized), preserving other instructions.
Do not create another local database, config registry, or mandatory task ledger.
Respect any existing requirement for `tasks.md`; this plugin does not repeal it.

Example mapping shape, filled with verified values after user approval:

- Repository: canonical remote URL
- Linear team: immutable team ID
- Linear project: immutable project ID and URL
- Tracking: user authorizes finding, creating, and maintaining issues and concise
  progress comments for meaningful development in this repository.

Installation and a project URL alone are not write authorization. A mapping cannot
expand authority to other repos, deletions, project administration, messages to
people, deployment, or changes to priority, assignee, milestones, or due dates.
Honor opt-outs and narrower task instructions without repeatedly asking permission.

## Find one outcome issue

Meaningful work changes product behavior, fixes a real defect, or leaves work to
resume across sessions. A quick but real bug fix can deserve an issue; elapsed time
is not the criterion. Questions, exploratory browsing, formatting, and trivial
edits create no issue unless requested. Still update an explicitly linked issue
when such work materially resolves it. Use an existing issue for implementation,
tests, review, and release of the same outcome instead of ticketing each step.

1. Prefer an issue explicitly provided by the user or already linked in task
   context, branch, or PR. Fetch it and verify its team/project and relevance.
   A mismatched destination needs clarification before mutation.
2. Otherwise search the mapped project for the outcome, including recently
   completed matches when recovering from an uncertain write. Reuse an appropriate
   issue; ask if multiple candidates remain plausible. Do not reopen a completed
   issue automatically for a new regression.
3. If no match exists and writes are authorized, create one concise action-first
   issue with the outcome, agreed acceptance criteria, and known constraints.
   Search again immediately before creation. Preserve the returned ID and URL in
   current task context and, where appropriate, the existing branch/PR record.
   Do not introduce a second local ledger.
4. Fetch the team's actual workflow states. Move work that has started to its
   active state; don't invent names such as In Progress or Blocked if absent.
   Preserve human edits and unrelated fields. Never bulk-reclassify the backlog.

Deduplication is best effort, not an atomic lock. Concurrent machines may race.
If duplicates appear, identify them for review; do not delete or merge them on
assumption. Do not take over another person's active issue without clear scope.

## Reconcile before the final response

Update only when the outcome, blocker, acceptance, or evidence materially changed.
Do not post per prompt, per tool call, or for unchanged status. Read the latest
issue and relevant comments first; omit a note already recorded. Patch narrowly,
retaining human-authored requirements and newer work from other sessions.

- **Active:** implementation or required verification remains.
- **Blocked:** record the specific dependency and next action. Use the team's
  blocked state if available; otherwise retain an unfinished state with a blocker
  note. A transient tool failure is not a product blocker.
- **Ready for review:** required human acceptance or merge/release remains. Use an
  appropriate unfinished state. Passing local tests does not imply shipped work.
- **Done:** all agreed acceptance criteria and required review/delivery steps are
  satisfied. Record the actual checks and outcome before marking completed.
  If the evidence note fails to save, leave the issue unfinished.

A concise note contains changed behavior, verification actually performed, a
relevant commit/PR link when available, and remaining work or blocker. No logs,
secrets, raw prompts, transcript dumps, or claims that mocks prove live integration.
Keep partial work unfinished even if the agent stops, crashes, or ends its turn.
If interrupted, reconcile from fresh issue/repo evidence on the next invocation;
there is no guaranteed end-of-session write.

Read back mutations to confirm the saved state. If a write times out or its result
is uncertain, query for that issue/comment before retrying. Do not blindly repeat
create/comment calls. Retry only after confirming absence; if you cannot determine
whether it saved, stop synchronization and report uncertainty.

## Missing connection and reporting

If Linear is unavailable or read-only, continue authorized development. Do not
install software, change auth/configuration, or widen permissions to make it work.
Skip repeated attempts for the rest of the turn unless the user restores access.
At handoff, state the unsynced outcome and next action in the task response, reusing
an existing repo task record only if the repo already requires one. On recovery,
fetch current Linear state before applying missing changes.

Final response: link the issue and describe a material state change briefly.
If nothing changed, avoid an administrative status report. If synchronization
failed, distinguish completed development from unsaved Linear updates.
