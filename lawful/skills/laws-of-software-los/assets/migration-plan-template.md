# Migration Plan: [Migration]

## Objective

[What moves from where to where, and why.]

## Current state

- Source system:
- Target system:
- Users/clients:
- Data:
- Integrations:

## Strategy

[Strangler | branch by abstraction | parallel run | dual write | backfill | big-bang with justification]

## Compatibility

- Existing behavior to preserve:
- Public contracts affected:
- Deprecation plan:

## Data plan

- Source of truth during migration:
- Backfill:
- Dual write/sync:
- Reconciliation:
- Repair:
- Retention/deletion:

## Rollout plan

1. Instrument current system.
2. Add compatibility seam.
3. Move low-risk slice.
4. Shadow/parallel run.
5. Reconcile.
6. Shift traffic gradually.
7. Freeze old writes.
8. Complete cutover.
9. Delete old path.

## Rollback

- Technical rollback:
- Data rollback/repair:
- Communication plan:

## Validation

| Check | Method | Pass criteria |
|---|---|---|
| Correctness |  |  |
| Performance |  |  |
| Reliability |  |  |
| User impact |  |  |

## Risks

| Risk | Mitigation | Owner |
|---|---|---|
|  |  |  |
