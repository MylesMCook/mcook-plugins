# Verification evidence

Checked 2026-10-02 on macOS. The intended outcome is useful comments for a human
reviewing code they did not write, especially code created by an LLM. Checks
below verify package behavior and concrete comment decisions; they do not
measure a human reader's comprehension of this particular skill's output.

## Package and discovery

- Portable Agent Plugins 1.0.0 validator: passed, zero warnings, including the
  OpenAI overlay and repository marketplace mapping.
- Skill frontmatter validator: passed.
- `claude plugin validate .`: passed for the repository Claude catalog.
- `uv run python -m unittest discover -s code-comments/tests -v`: two native
  ingestion tests passed using Codex CLI 0.156.1 and Claude Code 2.1.287.
- Codex: a temporary local marketplace and config home installed the package;
  all source files matched installed bytes. Supported `plugin/read` and
  `skills/list` APIs discovered one enabled `code-comments:code-comments` skill,
  with no MCP server or hook. No model request or credentials were needed.
- Claude Code: a temporary catalog/config/plugin home installed the package
  without a per-plugin Claude manifest. Native component inventory reported
  `Skills (1) code-comments`. No model request or live-account installation.
- Catalog comparison: each catalog preserves all earlier entries and root
  metadata and appends exactly one `code-comments` entry. Portable, OpenAI,
  and Claude identity/version metadata agree; OpenAI interfaces agree.
- The installed plugin-creator skill has no `scripts/validate_plugin.py`.
  That standalone check was unavailable. The actual supported Codex ingestion
  APIs, portable validator, and skill validator supply the observed evidence;
  no missing script was downloaded or claimed to have passed.
- Cursor: root portable manifest and its catalog entry were checked against
  current official format documentation and the portable schema. Interactive
  Cursor installation, activation, and model behavior were not exercised.

## Independent synthetic forward test

A separate agent used the skill on raw Go/Python fixtures, tests, and a short
task specification in an isolated scratch directory. It could not edit the
plugin checkout or install tools.

- Audit request: source byte comparison passed. Findings distinguished a stale
  retry claim, a missing documented error, and a redundant comment.
- Edit request: the retry predicate's comment now describes HTTP 429/503, the
  supplied 1-based attempt convention, and the boundary at attempt three.
  Python documentation now states the blank-input error and retains its
  working example. Redundant statement narration was removed.
- Executable Go source and Python AST excluding the intentionally changed
  docstring stayed identical. Build directive, encoding declaration, SPDX
  notice, and unresolved TODO survived. Tests, task specification, and policy
  retained their hashes.
- After editing: Go's five existing table cases, `go vet`, `gofmt`, two Python
  unit tests, and one doctest passed. No Python formatter was installed for
  the fixture; no unrun formatter or linter is claimed.
- Manual routing assessment covered direct/indirect comment requests,
  incomplete input, a policy proposal, and two nearby non-trigger tasks.
  This was a description/workflow assessment, not runtime auto-selection.

- Human-review request: a fresh LLM-generated invoice discount allocator gained
  a short explanation of largest-remainder rounding, caller assumptions,
  denominator safety, exact arithmetic, and invoice-order ties. Comments were
  checked against a raw specification and code, without inventing author intent.
  Seven tests passed before and after, covering 1,664 valid bounded inputs;
  one added doctest passed. Executable ASTs matched after excluding intentional
  docstrings; outputs and exception types/messages matched in 1,668 comparisons.
  The example supports a concrete editorial assessment, not a comprehension
  benchmark or proof about arbitrary generated code.

- Writer-informed readability request: a separate verbose generated draft lost
  filler and vague assurances while preserving integer minor units, caller
  responsibilities, unchecked runtime types, errors, caps, zero boundaries,
  exact totals, mutation limits, and deterministic ties. Seven tests (including
  1,664 bounded valid cases), one doctest, executable AST comparison, and 1,668
  before/after outcome comparisons passed. Readability was assessed through
  editorial and requirement-by-requirement review, not a human study.

## Publication

Implementation commit `2ab80fc` was pushed to remote main. A fresh Git-backed
marketplace in an isolated Codex home fetched the live repository and exposed
`code-comments@mcook-plugins-local` 0.1.0 as available and uninstalled. All 13
tracked package files matched the published source byte-for-byte; all three
published catalogs contained exactly one matching entry.

The active CLI currently has no configured Git source for `mcook-plugins-local`;
its normal marketplace upgrade could not run. Global configuration was left
unchanged. Verification used the live Git source in the isolated home, and no
plugin was installed in the user's active configuration. JSON listing used
`--available` because CLI 0.156.1 omits uninstalled entries without that flag.
The README includes first-time source registration as well as installation.

Scratch evidence is kept locally under
`~/Documents/Codex/2026-10-02-code-comments/evaluation/`; fixture source, model
transcripts, caches, and third-party PDFs are not shipped in this package.

## Research integrity

The annotated review contains 16 primary studies: 12 about source-comment
maintenance/quality and four about human interaction with generated code.
Full texts were inspected except Fluri et al., for which the primary abstract
was available. Each card records method, narrow result, limitations, and a
practical inference. Official language/package conventions are identified
separately. Synthetic examples are labeled as examples, not research findings.
