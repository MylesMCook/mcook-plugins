---
name: trace-power-automate-submission
description: Trace one exact submission or correlation key across Power Automate runs, authoritative business records, and delivery artifacts. Use when someone asks whether a specific workflow submission completed, is still processing, failed before writing, or needs reconciliation. This workflow is read-only and does not perform recovery or resubmission.
---

# Trace a Power Automate Submission

Use the bundled `microsoft_fabric` MCP server for Power Automate and Microsoft
365 metadata. Load the target system's nearest `AGENTS.md` or runbook first;
that local documentation owns lane names, asset IDs, authoritative records,
commit rules, evidence paths, and processing windows.

Require two inputs before making a tenant call:

- the exact deployment lane or system context;
- the exact submission or correlation key.

Do not infer a lane from an environment ID, display name, timestamp, or nearby
successful run.

## Keep the trace read-only

- Never run, resubmit, retry, update, enable, disable, or patch a flow.
- Match the exact key. Temporal proximity is not correlation evidence.
- Separate flow execution, the authoritative business commit, and delivery
  artifacts such as PDFs or emails. None proves the other by itself.
- Treat Graph file metadata as existence evidence only. Do not claim file
  contents were validated unless an approved content-reading surface did so.
- If a required store, permission, or evidence source is unavailable, report
  it as unknown. Never turn missing evidence into permission to retry.

## Trace the key

1. Call `check_local_setup`, then `describe_capabilities`. Stop on a missing
   prerequisite or permission.
2. Resolve the exact environment, flows, and Microsoft 365 resources from the
   system's maintained asset map. Use bounded lists and exact IDs; do not
   rediscover a known deployment by guessing from names.
3. Inspect a bounded set of relevant flow runs and sanitized action results.
   Tie a run to the key through explicit key-bearing input, output, or
   deterministic retained evidence. A green run alone is not enough.
4. Resolve deterministic key-specific files or markers and record their
   existence, type, size, and timestamps when useful. Validate contents only
   through an approved reader.
5. Verify the authoritative business record through that system's approved
   read surface. For an Excel ledger, use the connected live workbook session,
   confirm the exact workbook, and read only the key-specific log row and rows.
   Do not use standalone file tooling to inspect a live authoritative workbook.
6. Compare the observed evidence with the system's documented commit and
   completion invariants, then return one fail-closed result.

## Results

- **Complete:** the exact authoritative commit satisfies every documented
  invariant, with matching completion evidence when the system requires it.
- **Processing:** exact key-bearing processing evidence is active within the
  documented window and no evidence conflicts with it.
- **Rejected before write:** an exact run conclusively rejected the request,
  the authoritative store has zero matching writes, and completion evidence is
  absent.
- **Reconciliation required:** the write is partial or mismatched, evidence
  conflicts, a marker is stale, or a post-write outcome is ambiguous.
- **Not found:** both the deployed path and authoritative store were checked
  successfully and contain no exact evidence for the key.
- **Unknown:** required evidence could not be read or the target deployment
  could not be resolved safely.

## Report

Return a short operator result unless the user asks for detail:

```text
Context / key:
Result:
Authoritative record:
Workflow evidence:
Delivery artifacts:
Safe next action:
Unknowns:
```

For **Complete**, the safe next action is no resubmission. For **Processing**,
wait and recheck the same key. For every other result, preserve the evidence
and stop; any recovery, reconciliation, or replay requires a separate explicit
approval for that exact key and action.
