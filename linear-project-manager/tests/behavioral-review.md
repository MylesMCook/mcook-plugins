# Behavioral review, 2026-09-22

These are local scenario walkthroughs against the completed skill, not live
agent activations or authenticated Linear tests. The user approved the v1
behavior table before implementation.

| Input and state | Reviewed decision |
| --- | --- |
| Explicitly invoke the skill to map a repo with no mapping | Read-only candidate lookup, one destination/authority question, persist verified IDs only after approval. |
| Indirect feature request in a mapped repo; no matching issue | Search in project, recheck before create, create one outcome issue, use actual active workflow state. |
| Resume the same fix on another machine with an issue link | Fetch and verify linked issue; reuse it, no machine-path identity or new ticket. |
| Feature request in an unmapped repo | Ask for destination/scope once; no guessed project or unauthorized write. |
| Explain a function, browse documentation, or adjust formatting | No new issue or mapping ceremony unless explicit tracking requested. |
| Fix a real defect in five minutes | Duration does not exclude tracking; one outcome issue. |
| Local tests pass but required review or deployment remains | Keep unfinished; no Done or shipped claim. |
| All agreed acceptance and delivery pass | Save concise evidence first, then completed state; read back. |
| Evidence comment fails while implementation is finished | Leave issue unfinished, disclose unsaved synchronization. |
| External dependency prevents completion; no Blocked state exists | Keep unfinished and record dependency/next action; do not invent a state. |
| Linear is disconnected or read-only | Continue development, report unsynced outcome, no automatic auth changes or repeated retries. |
| Create/comment times out after possible success | Read current state before retry; stop sync if outcome remains uncertain. |
| Another machine already posted identical evidence | Read recent comments, omit duplicate note. |
| Similar issue belongs to another project or multiple matches exist | Clarify before mutation; do not guess or take over. |
| Concurrent machines both create an issue | Best-effort search cannot guarantee uniqueness; identify duplicates for review, do not delete or merge. |
| Mapping grants tracking, user says do not update Linear this task | Respect the narrower request; mapping is not blanket authority. |
| Stop/crash before reconciliation | No Stop continuation; next invocation reconciles fresh evidence. |

Review result: each case has a corresponding decision in the skill. No runtime
policy engine is claimed: issue selection, authority checks, and completion remain
agent decisions. Live acceptance still requires an authenticated disposable Linear
project plus a fresh installed task.

## Historical 0.1.0 native verification

- Codex CLI 0.153.4 and desktop 0.155.0-alpha.9.2: all seven tests pass.
- Fresh-home installation preserves package bytes and exposes one enabled skill,
  the Linear MCP declaration, and both context hooks in the native app-server API.
- Both hooks report `untrusted` before user review, with no load warnings/errors.
- The native-resolved commands execute successfully from the installed cache.
  This subprocess test does not change trust or prove a model followed the context.
- A read-only lookup through the existing connected Linear tools succeeded, with
  no matching repo project. This is connector evidence, not bundled-server OAuth
  or write-cycle acceptance. No test tickets or comments were created.

The original portable build failed the same native regression (zero hooks).
Version-matched upstream `core-plugins/src/loader.rs` explicitly omits hooks for
AgentPlugin-format packages. The user approved the Codex-native exception.
Windows execution and a live authenticated create/update/readback cycle were
unverified. User installation, OAuth where needed, and hook trust were still required.

## 0.1.1 hook removal

The 0.1.0 hook findings above are historical. Version 0.1.1 removes both hooks.
The fresh-home native installation test now requires one enabled skill, the Linear
MCP declaration, and zero plugin hooks. No authenticated Linear write cycle is
claimed by that test.

## 0.1.2 portable packaging

Accepted outcome: installation exposes one enabled skill and the official Linear
MCP declaration, with zero hooks, both with OpenAI compatibility files and with
only the Agent Plugins core. Portable and native manifests retain the same
identity and version, and both MCP declarations use the same HTTPS endpoint with
their format's Streamable HTTP transport spelling.

Before migration, the existing native installation check passed while the new
portable-only check failed because root `plugin.json` was absent. After migration,
all three package/discovery checks pass on Codex CLI 0.162.1 in disposable homes.
The portable-only check removes `.codex-plugin/` and `.mcp.json` before installation,
so native fallback cannot satisfy it. No model call, OAuth flow, Linear operation,
desktop client check, or other-client runtime check is claimed. The old hook-based
native-only exception is retired.
