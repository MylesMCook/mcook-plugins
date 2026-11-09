# Changelog

## 2.0.0 - 2026-11-08

- Remove the bundled personal MCP endpoint. Configure an HTTP server named
  `firecrawl` in your client before upgrading; see the README.
- Keep both skills and their names. Point the Claude research agent at the
  user-configured server and remove machine-specific operator notes.

## 1.2.0 - 2026-10-27

- `firecrawl-research` answers people in plain prose with cited sources. The
  `Answer` / `Confidence` / `Status` block moved to
  `references/answer-format.md` and is used only when a prompt or harness asks
  for it, such as eval runs.
- Sharper skill description naming the built-in WebSearch and WebFetch, so
  ordinary current-information questions load the skill.
- README: a `~/.claude/CLAUDE.md` snippet that makes Claude Code use the skill
  for web questions. In headless Sonnet runs the description alone loaded the
  skill 0/3 times; with the snippet, 3/3.

## 1.1.0 - 2026-10-27

- Added the Claude Code `personal-firecrawl:web-researcher` agent
  (`claude/agents/web-researcher.md`, wired through the Claude marketplace
  entry). Its `tools` allowlist is only the plugin's Firecrawl `search` and
  `fetch`, so Claude Code enforces the limit and it cannot start subagents.
- `firecrawl-research` uses that agent on Claude Code and keeps the
  `web-researcher` brief for other clients. Independent attempts paste the
  puzzle method into the agent's prompt.
- The brief now checks `status`, `error` and `truncated` and retries failed
  fetches through the Wayback Machine, matching the skill.
- Noted that the hosted search route returns at most 10 results.

## 1.0.1 - 2026-10-26

- `firecrawl-research`: Ceramic-aware query rules (plain keywords before
  `"exact phrase"`, `OR` and exact-host `site:`; default 10 results), a
  structured-sources reference for papers, archives and lists, readings for
  vague phrases, a Wayback retry for failed fetches, and independent attempts
  with reconciliation for hard unverified answers.

## 1.0.0 - 2026-10-26

Breaking: seven skills removed and replaced by two.

- Added `firecrawl-research`: all web lookups and research through the MCP
  `search` and `fetch` tools, with question sizing, keyword query rules, a
  multi-clue puzzle method, reading rules, subagent fan-out, and a fixed
  answer format (best answer, confidence, verified or unverified, sources
  actually seen).
- Rebuilt `firecrawl-cli` for on-host bulk work only: map, crawl, download and
  saved files through the local CLI. Kept the endpoint, CLI and security
  references.
- Retired `firecrawl-search`, `firecrawl-scrape`, `firecrawl-map`,
  `firecrawl-crawl`, `firecrawl-download`, `firecrawl-agent` and
  `firecrawl-interact`. Server-side deep research is no longer described; the
  wrapper no longer exposes it.
- Shipped the `web-researcher` subagent as a brief inside `firecrawl-research`
  rather than an agent file, because Agent Plugins agents are client-specific.
- MCP connection unchanged.

## 0.2.0 - 2026-10-21

- Migrated MCP instructions to search, fetch and deep_research for wrapper 3.0.
- Updated inputs, bounded structured results and research ID continuation.
- Routed removed map, crawl, batch, extract, agent and action operations to
  supported on-host CLI/API paths without promising unavailable MCP tools.
- Preserved all eight skill names and the production OAuth connection.

## 0.1.0 - 2026-08-27

- Grouped eight self-hosted Firecrawl skills into one marketplace plugin.
- Added the authenticated production Firecrawl MCP endpoint without credentials.
- Updated the skills for the personal wrapper's scrape actions, structured
  extraction, asynchronous jobs, agent workflow, and deep-research tools.
- Kept local CLI fallbacks for file output and options not exposed by the MCP
  wrapper.
