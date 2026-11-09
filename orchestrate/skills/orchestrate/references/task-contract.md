# Task and handoff contract

Use these compact shapes. Add fields only when the task needs them.

## Parent task graph

```text
Objective:
Done criteria:
Constraints:
Approval boundary:
Source identity:

Host capability context:
- native_subagent_tools:
- spawn surface:
- concurrency limit source:
- routing metadata source:

Slices:
- id:
  depends_on:
  owner:
  read_scope:
  write_scope:
  requested_route:
  expected_output:
  verification:
```

Record parent-visible routing evidence separately after launch:

```text
Routing evidence:
- id:
  requested_agent_type:
  requested_model:
  requested_reasoning_effort:
  requested_history_mode:
  configuration_precedence:
  observed_agent_type:
  observed_model:
  observed_reasoning_effort:
  observed_history_mode:
  verification_status: runtime-verified | configuration-derived | unverified | mismatch
  metadata_source:
  fallback_reason:
```

Always record requested routing. Populate observed fields only from
parent-visible spawn or session metadata. `configuration-derived` means the
expected route follows documented configuration precedence; it is not proof of
the effective role, model, reasoning effort, or history mode. Do not treat a
child's self-report as proof.

## Child task packet

```text
Objective:
Scope:
Known facts:
Relevant paths or sources:
Constraints:
Edits allowed:
Write ownership:
Done criteria:
Return contract:
```

Do not paste the full parent transcript when a short packet is sufficient. Give
the child exact paths, refs, errors, or source URLs it needs to work without
guessing.

## Child handoff

```text
Status: complete | partial | blocked
Scope handled:
Findings or changes:
Evidence:
Verification:
Files changed:
Risks or open questions:
Recommended next action:
```

A handoff is incomplete when it omits material verification or does not state
which files it changed. The parent must inspect evidence before integration.
