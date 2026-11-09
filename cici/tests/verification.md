# Verification: 2026-10-15 Windows launch repair (0.1.1 candidate)

- Windows PowerShell, Node 24.12.0, Claude Code 2.1.280. Before the fix, helper
  setup selected the extensionless npm launcher, returned ENOENT for version
  and auth, and incorrectly reported loggedIn=false.
- `node --test cici/tests/claude-code.test.mjs`: 9 passed. New resolver tests
  failed against the original implementation before the repair. Coverage includes
  native/npm Windows layouts, unsupported shims, PATH ordering, spaces, exact
  prompt/argument preservation, missing binaries and synchronous launch failures.
- Real source helper setup: ok=true, version=2.1.280, loggedIn=true, auth exit=0.
  Account identifiers were not retained.
- Real source helper review in an empty temporary directory with
  `--no-git-context`: returned CICI_WINDOWS_OK, exit=0. Existing plan permissions,
  empty tools, deny list and disabled session persistence were preserved.
  Claude warned about the inherited unknown MultiEdit deny entry and a cancelled
  local SessionEnd hook; neither prevented the response or successful exit.
- Portable validator with marketplace mapping and OpenAI overlay: zero warnings.
  All three skill validators and `git diff --check` pass.
- Windows executed the real native process. Unix resolver behavior is covered
  synthetically here; actual Unix process regression awaits the existing CI matrix.
  Fresh-home ingestion, installed-cache execution and interactive skill activation
  were not rerun. The separate OpenAI validator is still absent from the installed
  plugin-creator. No publication, installation or authentication changes were made.

## Historical migration baseline: 2026-10-12

The following evidence and source-sha256.json describe the original 0.1.0 transfer,
not byte identity of the repaired helper or skills.

- All seven original files (three skills, helper, contract, tests, icon) match
  the user-designated Claude Code 0.1.0 installed package by SHA-256.
- Existing Node tests: 3 passed. Ask/review/rescue dry runs return the intended
  prompts; review and rescue explicitly omit Git context when requested.
- Fresh temporary Codex home: install succeeds, all package bytes match,
  plugin/read reports three skills and no MCP servers or hooks; skills/list
  exposes all three enabled cici-prefixed names at installed paths.
- Portable package and marketplace validation: zero warnings. All three skill
  validators pass. Separate OpenAI validate_plugin.py is unavailable in the
  installed plugin-creator; actual native ingestion is checked instead.
- Existing Claude CLI 2.1.293 setup sees login in the normal keychain context;
  sandbox setup reports logged out as documented by the preserved contract.

Routing review (static, not model-evaluated): direct Claude asks select the base
skill; second-pass reviews select review; investigation/fix-plan requests select
rescue. Missing task context requires inspecting the target repo first; ordinary
Codex-only edits need no Claude call. Secrets, unapproved Git context, remote
side effects, and broad refactors retain the original guards.

Native Windows execution and fresh interactive chat activation are not tested.

Live provider smoke: the unchanged helper returned exactly `CICI_OK` with a
synthetic prompt and no repository context. Claude 2.1.293 warns that the inherited
`MultiEdit` deny entry names no known tool; the effective `--tools ""` and plan
permissions remain in place. This migration deliberately preserves the helper.
