---
name: bug-reporter
description: >-
  Create, improve, format, or safely investigate evidence for fix-ready bug
  reports covering software, hardware, APIs, CLIs, SDKs, apps, services,
  integrations, data pipelines, infrastructure, build and test systems, and
  research tooling. Use when the requested deliverable is a bug report, issue,
  defect handoff, reproduction packet, or private vulnerability report,
  including from failures, regressions, crashes, hangs, incorrect results,
  performance problems, intermittent behavior, usability defects, logs,
  screenshots, reproduction notes, or an existing issue. Do not use when the
  requested outcome is only to implement a fix, troubleshoot interactively, or
  propose a feature without a defect report or handoff.
---

# Bug Reporter

Reduce the maintainer's path from report to confirmed failure to verified fix.
Produce a truthful evidence packet, not a longer retelling of the complaint.

## Choose the working mode

Infer the narrowest mode from the request:

1. **Draft:** Turn supplied facts and artifacts into a finished report. Do not
   start a live investigation unless the user asks.
2. **Investigate and draft:** Collect safe evidence, minimize the failure, and
   then write the report.
3. **Improve:** Preserve every supplied fact while repairing ambiguity,
   structure, and missing-evidence handling. Never fill gaps from plausibility.
4. **Format or submit:** Inspect the target's current contribution guide,
   issue template, component ownership, and security policy. Match its required
   fields and terminology before drafting or submitting.

A request to write a report does not authorize a product patch, public issue,
message, or submission. Take those actions only when separately authorized.

## Route the report safely

- Keep one independently fixable defect per report. Link tightly related
  failures instead of blending them.
- Search the target tracker when submission or duplicate checking is in scope.
  Add new evidence to an exact match; do not force distinct failures into a
  vaguely similar issue.
- Treat suspected vulnerabilities, authorization bypasses, secret exposure,
  privacy leaks, and exploitable data corruption as private reports. Follow
  `SECURITY.md` or the target's private disclosure channel. Never put exploit
  details or sensitive evidence in a public issue.
- Redact credentials, tokens, cookies, signed URLs, personal data, confidential
  payloads, private hostnames, and unrestricted internal links. Use stable
  placeholders so relationships remain clear.

## Establish the actual contract

Inspect the most authoritative evidence available: current local source,
installed versions, live schemas or capability descriptions, issue templates,
tests, specifications, and official documentation. Record only environment
details that could explain or reproduce the failure.

Define expected behavior in observable terms. Anchor it to a specification,
documented contract, test, invariant, previous working version, or an obvious
safety property. If the expectation is a product preference rather than a
contract violation, label it as a usability problem or feature request.

## Build the evidence packet

Capture these universal elements when known:

- a title that names the component, trigger, and symptom rather than a proposed
  solution;
- a one-paragraph summary of the divergence and practical impact;
- exact relevant product, build, revision, dependency, OS, runtime, hardware,
  transport, configuration, and feature-flag values;
- prerequisites and the smallest known starting state;
- numbered, atomic reproduction steps that state exact actions or commands,
  including the working directory when it matters;
- actual and expected behavior, clearly separated;
- a reproduction rate such as `4/5 attempts`, or `Not reproduced` with
  unique forensic evidence;
- first-observed time with timezone and, for regressions, last known good and
  first known bad versions or revisions;
- the smallest useful failing test, input, output, log excerpt, stack trace,
  crash or correlation ID, trace, profile, screenshot, recording, or state
  diff;
- user and system impact, affected scope, data or state impact, and any safe
  workaround;
- acceptance criteria that prove the defect is fixed without breaking a nearby
  valid case.

Keep causal hypotheses and fix ideas out of the title and summary. Put them in
`Analysis`, labeled as inference, so the maintainer sees the observed defect
before the reporter's theory.

Prefer pasteable text, commands, paths, and stable artifact links. A screenshot
or video may support a report but must not be the only description of the
failure. Preserve exact error text inside code fences and include enough
surrounding context to interpret it, not an indiscriminate log dump.

Read [evidence-by-defect.md](references/evidence-by-defect.md) before collecting
or evaluating evidence for a specialized failure such as a crash, performance
regression, intermittent race, data error, accessibility defect, distributed
request, or build failure.

## Reproduce without causing a second incident

- Preserve the user's active task and record the operation that failed.
- Prefer existing artifacts, read-only checks, dry runs, and disposable
  fixtures. Do not reproduce against production or irreplaceable data without
  explicit authorization.
- If a mutation may have been sent, read back state before retrying. Never
  retry a non-idempotent operation merely to improve the report.
- Start from a named clean state. Change one variable at a time and remove
  irrelevant steps without hiding required setup.
- Confirm the failing case and, when safe, one nearby success or control case.
- For intermittent behavior, keep the timing, ordering, load, concurrency,
  seed, and attempt denominator. Do not translate `2/20` into `sometimes`.

Do not discard a non-reproducible crash, corruption event, or intermittent
failure when it has unique diagnostic evidence. State what was attempted, how
many times, and what evidence remains available.

## Separate evidence from diagnosis

Use three explicit claim levels:

- **Observed:** Directly supported by a command, artifact, state readback, or
  cited contract.
- **Inferred:** A narrow explanation consistent with the observations. State
  confidence and the discriminating test.
- **Unknown:** Missing evidence that materially affects reproduction, routing,
  or repair.

Correlation, a nearby code change, or a workaround is not automatically root
cause. Include suspected component ownership, fix direction, or code locations
only when evidence makes them useful. Do not prescribe an implementation that
the report has not justified.

## Handle missing information honestly

Never invent versions, commands, reproduction rates, expected behavior,
severity, impact, root cause, or results. When a missing fact blocks a useful
report, ask no more than three high-information questions. Otherwise produce
the best complete draft and put the gap under `Missing evidence` with the next
safe probe.

Name material gaps briefly, then choose one `Next probe` with the highest
information gain. If the minimal failure has not been captured, do not invent a
specific test harness or fix-dependent acceptance test; use an observable
criterion and make the regression test conditional on a reproducible case.

Do not punish the reader with empty boilerplate. Omit irrelevant sections and
fields. Use `Not captured` only when the absence itself matters.

## Control report length

- Let the evidence determine the length. There is no minimum section count or
  word count.
- Start with the summary. Do not add a preamble, methodology recital, generic
  conclusion, or restatement of the user's request.
- State each fact once in the section where it is most useful. Do not repeat the
  title in the summary, the summary in impact, or the same error in several
  sections.
- Use short prose for meaning, numbered steps for sequence, and bullets for
  compact facts. Add a table only when it makes repeated fields easier to
  compare.
- Excerpt artifacts to the smallest useful span and link the full sanitized
  source when maintainers may need it.
- Preserve exact technical terms, error text, commands, citations, caveats, and
  uncertainty. Concision does not outrank correctness.

## Save and offer the report

Follow the target tracker template when one exists. Otherwise adapt
[bug-report.md](assets/bug-report.md). Remove every unused heading,
instruction, and placeholder from the finished report.

Lead with the defect and impact. Put diagnostic depth after the reproduction
contract. Keep implementation notes optional and evidence-labeled.

Always write the finished report to a Markdown file. Do not print or duplicate
the report body in chat, even when the user did not explicitly ask for a file.
The request for a bug report authorizes creation or update of this report
artifact only; it does not authorize a product patch, submission, or message.

Choose the destination in this order:

1. Use the explicit output file or directory supplied by the user.
2. When improving a report loaded from an existing local `.md` file, update
   that file unless the user supplied a different output destination.
3. Otherwise use
   `<workspace-root>/bug-reports/YYYY-MM-DD-<title-slug>.md`. If the host does
   not identify a workspace root, use the current working directory as the
   workspace root.

Treat an explicit path ending in `.md` as a file. Treat every other explicit
destination as a directory and place the generated filename inside it. Use the
host's local date. Build `<title-slug>` from the report title by lowercasing it,
replacing each run of characters outside `a-z` and `0-9` with one hyphen,
trimming leading and trailing hyphens, and truncating it to 64 characters after
trimming. Use `bug-report` if nothing remains.

Create the parent directory when permitted. Never overwrite an unrelated
file. Updating the source report in improve mode is intentional; for every
other existing destination, append the lowest available numeric suffix before
`.md`, starting with `-2`.

Before handoff, read the saved file back and verify that it:

- exists at an absolute path with a `.md` extension;
- contains the complete final report;
- contains no unused headings, instructions, or placeholders; and
- contains no secret or private data that should have been redacted.

Return one compact link in this exact shape:

```text
Saved: [filename.md](/absolute/path/to/filename.md)
```

Add only an essential security, submission, or temporary-storage warning after
the link. Do not repeat the report, summarize it, or add a generic completion
recap. If no safe writable destination is available, ask for one and stop; do
not fall back to putting the report body in chat.

## Quality gate

Before handoff, verify that a person or agent can answer:

- What single behavior is wrong, and why does it matter?
- Which exact component and tested version are involved?
- What starting state and smallest steps expose it?
- What happened, what should happen, and what proves each claim?
- How often does it occur, and is there a regression window?
- Which artifacts, commands, paths, IDs, and timestamps support diagnosis?
- What is observed, inferred, and still unknown?
- How can a fix be verified, including a nearby non-regression case?
- Is the report safe to share through the chosen channel?
- Can any sentence, heading, field, or artifact disappear without reducing the
  maintainer's ability to act?

If any unavailable answer prevents action, name the missing evidence and the
single best next probe instead of decorating the gap with confidence.
