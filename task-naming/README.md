# Task Naming

Manual task-title cleanup for Codex. Nothing runs in the background.

The plugin contains one explicitly invoked skill and no hooks, MCP server,
App Server bridge, evaluator, daemon, or per-task state.

## Use it

Invoke `$task-naming` and choose a scope:

- **Current task:** rename only the task you are using.
- **Project folder:** standardize user-facing root tasks whose recorded working
  directory is the selected folder or one of its descendants.
- **Machine:** standardize user-facing root tasks on the selected Codex host.

Examples:

```text
$task-naming rename this task
$task-naming standardize tasks under ~/Code/MylesMCook/mcook-plugins
$task-naming clean up task titles across this machine
```

Titles put the differentiating action first:

```text
Verb object — Context
```

The context suffix is optional. Use `Create restore drill — Backups` when the
context improves recognition, but prefer `Publish task-naming 0.5.1` when the
project already supplies it. Titles use sentence case, aim for 25–45
characters, and treat 60 characters as a soft ceiling.

The skill uses native Codex task operations when the current host exposes them.
For a single task without a callable rename operation, it returns an exact
`/rename <title>` command. For a bulk scope without native operations, it
returns a mapping and states that nothing was changed.

## Install

```sh
codex plugin add task-naming@mcook-plugins-local
```

Start a new task after installing or updating so Codex loads the current skill.

## Sources

- [Build Codex plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Build Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [F-shaped scanning and information-first headings](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)
- [Short, unique, front-loaded list titles](https://developers.google.com/assistant/conversation-design/list)
- [Sentence case for interface titles](https://learn.microsoft.com/en-us/style-guide/capitalization)
- [Descriptive title-length guidance](https://docs.github.com/en/contributing/style-guide-and-content-model/contents-of-a-github-docs-article)
