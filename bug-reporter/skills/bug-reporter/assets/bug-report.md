# [Component: trigger causes specific symptom]

## Summary

[In one paragraph: under what condition, which component does what, what it
should do instead, and why the difference matters.]

## Environment

- Product or component: [exact name]
- Version, build, or revision: [exact identifier]
- OS, runtime, hardware, or transport: [only relevant values]
- Relevant configuration or feature flags: [sanitized values]
- First observed: [timestamp with timezone or version]
- Regression window: [last known good -> first known bad, if known]

## Preconditions

[Smallest required starting state, fixture, account role, data shape, or setup.]

## Steps to reproduce

1. [Exact action or pasteable command; include the working directory when needed.]
2. [One action per step.]
3. [The action that exposes the defect.]

**Reproduction rate:** [for example, `4/5 attempts` under the environment above]

## Expected behavior

[Observable result, with the contract, test, specification, invariant, or last
working version that establishes it.]

## Actual behavior

[Observable result and the exact point of divergence. Preserve concise error
text verbatim.]

## Impact and scope

- User or workflow impact: [blocked task or degraded behavior]
- Affected scope: [known users, data, platforms, or configurations]
- Data or state impact: [none observed, changed, lost, corrupted, or unknown]

## Evidence

- Failing test, command, or minimal input: [pasteable text or stable link]
- Error, stack, trace, profile, screenshot, or recording: [smallest useful artifact]
- Request, crash, or correlation ID: [sanitized ID]
- Timestamp and timezone: [exact occurrence]
- State before and after: [sanitized diff or readback]
- Nearby success or control case: [what still works]

## Analysis

**Observed:** [Facts directly supported by the evidence above.]

**Inferred:** [Optional narrow hypothesis, confidence, and discriminating test.]

**Suspected component or fix direction:** [Optional and evidence-supported.]

## Workaround

[Safe temporary path and its limitations, or `None known`.]

## Acceptance criteria

- [The failing case produces the expected result.]
- [A nearby valid or control case still works.]
- [Relevant state, security, performance, and compatibility guarantees hold.]
- [A regression test fails before the fix and passes afterward, when practical.]

## Missing evidence

- [Material unknowns that affect reproduction, routing, or repair.]

**Next probe:** [The single safest, highest-information action that could close
the most important gap.]

<!-- Delete every unused heading, instruction, and placeholder before handoff. -->
