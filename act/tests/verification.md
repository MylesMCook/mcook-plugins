# Act 0.1.0 verification

Initial implementation checked on mac-mini, macOS arm64, 2026-10-10, in the
primary checkout at base `1a58879`. Release status is recorded in `tasks.md`.
Local detailed evidence:
`/private/tmp/mcook-act-plugin.grz7yls9/`.

## Package and discovery

- Current Myles Plugin Builder portable-package validation: zero warnings.
- Current builder marketplace-entry validation: zero warnings, metadata only.
- Installed skill-creator quick validation: passed. Requirements live in the body
  because that installed validator does not accept `compatibility` frontmatter.
- Native regression installs only into a disposable Codex home, compares package
  bytes, and verifies one enabled `act:act` skill and no hooks/MCP servers through
  app-server APIs. No model, auth, or active-home installation is involved.
- Both catalog arrays retain all previous entries in order, with only `act`
  appended. Prior task-record content is preserved. Unrelated baseline files are
  byte-identical, local Markdown links resolve, and diff whitespace checks pass.

Metadata was generated with skill-creator's dependency-free `--name` route.
Validators used existing cached jsonschema/PyYAML installations without downloads.
Automatic approval review rejected a proposed PyYAML download because a new
dependency required approval; no dependency was acquired. The separately named
OpenAI `validate_plugin.py` is absent from the installed plugin-creator skill and
was not run. Native ingestion is separate evidence, not a claim that it ran.

## Workflow execution

The referenced setup task changed Docker/act limits during development. Its
restart and recovery completed before this plugin's separate smoke. This test
discovered the current configuration rather than relying on the earlier snapshot.
The plugin task made no runtime allocation or persistent configuration changes.

The disposable synthetic workflow was copied into a new scratch Git repository
and given a unique run name. It listed, previewed, and executed successfully with
installed act 0.2.89 against the existing local Docker endpoint. Assertions proved:

- Copied local files and Linux amd64 execution on the mapped runner.
- The current 4 GiB job memory cap and two-CPU limit.
- No mounted Docker socket and an empty workflow GitHub token.
- Output propagation between steps and successful job completion.

All 21 existing containers, including 20 running containers, retained their IDs,
start timestamps, restart counts, status, and health status across this test.
No run container or scratch repository remained. Installed act configuration
retained its hash. Evidence: `smoke-{list,preview,run}.log`, `smoke-result.json`,
and `containers-{before,after}.json` in the evidence folder.

The scratch harness used an independent process deadline and run-specific cleanup.
It isolated the platform config directory, whose original actrc was absent, and
used the existing home defaults. Approved empty input files and an explicitly
empty token prevented implicit credential loading. This repository's publishing
workflow was not executed.

## Coverage limits

Release preflight in a clean checkout of remote `main` also passed all 13 builder
regressions, portable and skill validation, isolated Codex native discovery, and
Claude marketplace validation with no errors or warnings. All three existing
catalogs append only Act and retain previous entries and metadata. This does not
establish a live Claude model invocation.

Independent source-based review covered the cases in [evals.md](evals.md). Its
consumer-repository wording finding was corrected. A separate forward evaluation
made the correct decisions on four synthetic requests covering an unsafe
dependency chain, an excluded matrix with gh-act, sandbox denial, and generic
tests. It exposed an ambiguity about help/version creating a config directory;
the discovery guide now specifies an isolated child-process scratch config home
when the original platform config is absent. Those observations were simulated.
Windows/Linux configuration
instructions were checked against upstream source; those OS runtimes were not
executed. Automatic model activation, gh-act execution, private integrations,
native macOS/Windows runners, actual project CI, and reboot persistence remain
unverified. Local smoke success does not establish hosted-CI parity.
