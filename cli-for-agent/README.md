# CLI for Agents

`cli-for-agent` is a skills-only Codex plugin for designing and reviewing command-line tools that coding agents can run without babysitting. It is an adaptation of Cursor's MIT-licensed [CLI for Agent plugin](https://github.com/cursor/plugins/tree/0dda29e839d15464a137af9935665a5a47ee09b8/cli-for-agent), packaged for Codex's documented plugin and marketplace structure.

## What it covers

- Non-interactive commands with explicit inputs and confirmation bypasses where appropriate.
- Scoped `--help` with valid examples, stable command grammar, stdin, files, pipelines, pagination, and ordering.
- Machine-useful stdout, structured-output modes, stderr diagnostics, and clear exit behavior.
- Fast, actionable errors that explain the next valid command without leaking secrets.
- Idempotent retries, `--dry-run`, and proportionate safeguards for consequential mutations.
- Bounded remote jobs, retries, cancellation, and durable operation IDs for asynchronous work.

It does not add a runtime, hook, MCP server, or new command framework. The skill applies the smallest compatible improvement to the CLI already in scope.

## Use in Codex

Invoke it directly:

```text
$cli-for-agent:cli-for-agents Review this CLI for coding-agent usability.
```

Or ask Codex to build, refactor, document, or review a command-line interface. The skill can be selected implicitly for that work.

## Package layout

```text
cli-for-agent/
├── .codex-plugin/plugin.json
└── skills/cli-for-agents/
    ├── SKILL.md
    └── agents/openai.yaml
```

The manifest and skill location follow OpenAI's [Codex plugin structure](https://learn.chatgpt.com/docs/build-plugins#plugin-structure). This bundle needs no optional integration components.

## Install or refresh on a machine

This repository's Git-backed marketplace is `mcook-plugins-local`. Close any active tasks that are using the plugin, then run:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add cli-for-agent@mcook-plugins-local
codex plugin list | rg 'cli-for-agent@mcook-plugins-local'
```

Start a new Codex task after reinstalling so it loads the refreshed skill. There is no bulk plugin-update command; repeat the `codex plugin add` step for each updated plugin.

## Attribution and license

See [ATTRIBUTION.md](ATTRIBUTION.md) and [LICENSE](LICENSE).
