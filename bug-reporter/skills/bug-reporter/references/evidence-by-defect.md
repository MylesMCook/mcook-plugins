# Evidence by defect type

Read only the relevant section. Add fields when they help reproduce, diagnose,
or verify the specific failure; do not turn this reference into a mandatory
questionnaire.

## Crash, panic, or hang

- Capture the crash signature or ID, symbolized stack trace, thread dump, core
  or minidump reference, and the last successful operation.
- Record whether the process exited, restarted, deadlocked, or remained
  responsive, plus signal, exception, or exit status.
- For hangs, include duration, wait state, resource use, and thread or process
  samples taken while hung.
- State whether recovery preserved data and whether the same input crashes a
  clean process.

## Performance, resource use, or leak

- Name the metric and unit. Compare a measured bad case with a measured
  baseline under the same workload and environment.
- Record dataset or workload size, concurrency, warm-up, duration, sample
  count, distribution or percentile, and variance when relevant.
- Attach the smallest useful profile, trace, query plan, heap snapshot, or
  resource-over-time series.
- Separate absolute slowness from a regression; include last known good and
  first known bad revisions when available.

## Intermittent, timing, or concurrency failure

- Report successes and failures as a fraction over a defined attempt window.
- Preserve seed, ordering, timing, timeout, load, worker count, clock source,
  and concurrency level.
- Include per-attempt timestamps and correlation IDs when distributed systems
  are involved.
- Identify the smallest condition that changes the rate; do not claim a race
  without evidence.

## Regression

- Record the exact last known good and first known bad versions, builds, or
  commits tested under equivalent conditions.
- State other variables that changed at the same time.
- Include a bisect result only if each tested revision used a credible control
  and clean build. Otherwise provide the narrowed window without guessing the
  culprit.

## Build, install, dependency, or test failure

- Include the exact command, working directory, exit code, toolchain and
  package-manager versions, lockfile or resolved dependency state, and relevant
  environment variables with secrets removed.
- Say whether the failure occurs in a clean checkout, clean cache, incremental
  build, local machine, and CI image.
- Provide the first causal error, not only the final cascade or generic job
  failure.
- For test failures, include test name, seed, shard, retry behavior, and the
  smallest focused command that reproduces it.

## Incorrect result, data, or state transition

- Supply the smallest sanitized input, actual output, expected output, and the
  rule, schema, invariant, oracle, or independent calculation behind the
  expectation.
- Record locale, timezone, encoding, units, precision, ordering, and schema
  version when they can affect the result.
- Show state before and after. Distinguish display errors from persisted data
  errors and confirm whether readback agrees with the write response.
- Do not rerun destructive transformations merely to obtain cleaner evidence.

## UI, interaction, or accessibility defect

- Record route or screen, viewport, density, zoom, theme, locale, input method,
  browser or app build, and device when relevant.
- Describe the exact pointer, keyboard, touch, voice, or assistive-technology
  interaction and the intended task.
- For accessibility, include assistive technology and version plus relevant
  accessible role, name, state, focus order, announcement, contrast, or target
  size evidence.
- Add a screenshot or short recording when useful, but describe the defect in
  text and avoid exposing personal content.

## API, CLI, integration, or distributed service

- Capture the operation, endpoint or tool name, transport, sanitized request
  shape, response status and code, retry count, timeout, and exact client and
  server versions.
- Include timestamps with timezone and request, trace, job, or correlation IDs
  that let maintainers locate server-side evidence.
- Trace validation, dispatch, upstream acceptance, mutation, independent
  readback, rollback, and state restoration only as far as the declared
  contract requires.
- Distinguish caller input, local configuration, authentication, transport,
  wrapper behavior, upstream rejection, and service behavior. Surface the
  narrowest proven failing boundary.

## Hardware, operating system, or infrastructure

- Record model or topology, architecture, firmware, driver, kernel or OS,
  hypervisor or container runtime, storage or network path, and relevant health
  state.
- Include exact system errors and the smallest diagnostic logs around the
  event. Note taint, unsupported modules, overclocking, or vendor patches when
  relevant.
- State whether the failure follows the workload, machine, device, region, or
  software version.
- Treat data corruption, hardware damage, broad outage, and recovery failure as
  high-impact evidence requiring extra care before reproduction.

## Security or privacy vulnerability

- Stop public drafting or submission and find the target's private disclosure
  channel.
- Privately record affected versions and assets, prerequisites, attack surface,
  realistic impact, minimal proof, and whether exploitation or exposure was
  observed.
- Minimize access to real user data and do not broaden testing beyond the
  reporter's authorization.
- Keep public summaries non-exploitable until maintainers coordinate
  disclosure.

## Documentation or usability defect

- Quote only the smallest confusing or incorrect fragment and identify its
  exact version or URL.
- Describe the user's task, the reasonable interpretation, the resulting wrong
  action or dead end, and the verified behavior.
- Distinguish incorrect documentation, missing prerequisites, ambiguous errors,
  and excessive workflow friction.
- Suggest replacement wording or workflow only after establishing the actual
  contract.
