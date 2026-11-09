# Verification

Checked 2026-10-09 on Windows with Codex CLI 0.162.0-alpha.2 and Claude Code
2.1.280. These are prepublication checks. No installation into the user's
active profile was performed. Publication status is recorded in `tasks.md`.

## Package checks

- Agent Plugins 1.0.0 validator, OpenAI overlay, and canonical catalog mapping:
  passed with zero warnings.
- skill-creator frontmatter validation: passed.
- `claude plugin validate .`: passed for the repository catalog.
- All three catalogs preserve their original entries and root metadata and
  append exactly one `assistant-ui` entry.
- `git diff --check`: passed. Pre-existing README.md and tasks.md changes remain.
- Native regression: `uv run python -m unittest discover -s assistant-ui/tests -v`
  discovered and passed one test, with no skips. A temporary Codex home installs
  from a temporary local marketplace, compares installed bytes, and verifies
  `plugin/read` and `skills/list`: one enabled `assistant-ui:assistant-ui` skill,
  one `assistant-ui` MCP declaration, and no hooks. The test uses no model calls
  or user credentials and cleans up its temporary home.

The separately named plugin-creator skill/validator was not available in this
harness. Portable/overlay validation, current
[OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins),
and actual native ingestion were used. Public-directory ingestion is not tested.

## Live source checks

The declared HTTPS endpoint, `https://www.assistant-ui.com/mcp`, accepted a
Streamable HTTP initialize request without authentication. It returned
`assistant-ui-docs` 1.0.0 with negotiated protocol `2025-03-26`. After the
initialized notification, `tools/list` exposed seven tools:
`list_pages`, `get_navigation`, `search_docs`, `read_page`, `list_templates`,
`read_template`, and `preview_template`.

Actual calls to `search_docs` with `runtime architecture` and `read_page` with
`/docs/runtimes/concepts/architecture` returned nonempty, relevant documentation
without MCP errors. Direct retrieval of `llms.txt` worked, and all 14 `.md`
links in the skill returned HTTP 200 and nonempty, non-HTML content. No template
preview was created. No claim is made about MCP `2026-07-28` conformance.

After making upstream retrieval explicit, resolved `assistant-ui/skills` main
to `139674dc888ee076982b6726e8e6f5d0fe0b5f67` and fetched its README and
`assistant-ui/skills/runtime/SKILL.md`. Both the guide's relative
`./references/state-hooks.md` link and sibling `../thread-list/SKILL.md` link
resolved at the same commit and returned HTTP 200 with nonempty content.
Portable/overlay and skill validation and whitespace checks passed again.
No upstream content was vendored and no updater or installer was added.

## Approved behavior examples

These cases were reviewed against the authored instructions. This is a manual
instruction review, not an independent model execution or an application test.

| Case | Expected outcome | Evidence |
| --- | --- | --- |
| Direct: "Use $assistant-ui to explain runtimes" | Read relevant official pages and cite them | MCP search/read and linked runtime page work; retrieval and citation rules are explicit |
| Indirect: "This @assistant-ui thread stops updating" | Inspect installed versions and relevant source before changing code | Trigger covers package use; context and version checks preserve the existing project |
| Incomplete: "Help with assistant-ui" | Use the overview or resolve the missing goal without choosing a stack | Documentation questions need no project; missing context is requested only when material |
| MCP unavailable | Read llms.txt and linked Markdown; disclose unresolved gaps | Direct paths tested independently of MCP; both-path failure is covered in instructions |
| Nearby non-trigger: "Build a generic chat UI" | Do not select assistant-ui or run an installer just from that request | Discovery boundary and execution scope are explicit |
| Existing older integration | Use matching local types/source; do not upgrade to fit a current example | Version-conflict handling is explicit |
| New task after upstream changes | Refresh the live index and read relevant skill/reference files at one commit where possible | Current commit, guide, relative reference, and sibling skill retrieval verified; cross-task model behavior is not tested |
| GitHub unavailable | Continue with official documentation and disclose missing upstream skill verification | Explicit fallback reviewed; documentation endpoints passed the earlier live checks |
| Private data in a proposed hosted preview | Do not submit it without authorization and approved data | Remote preview side effect is identified separately from documentation reads |

Still unverified: model routing in a fresh user chat, interactive Cursor use,
Claude plugin installation, hosted template creation, and application behavior.
None is represented as a passing package or application runtime check.
