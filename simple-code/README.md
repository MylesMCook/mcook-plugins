# Simple Code

Reduce incidental complexity in code and design. The skill shapes APIs, module
boundaries, refactors, tests, naming, and architecture tradeoffs toward the
simplest design that satisfies the real requirement, preferring concrete, local,
reversible changes over speculative abstraction.

Use it when simplicity and maintainability are the main design pressure:

- "Simplify this module without changing behavior."
- "Is this abstraction earning its keep?"
- "What is the simplest architecture that meets these requirements?"

References cover [API design](skills/simple-code/references/api-design.md),
[architecture](skills/simple-code/references/architecture.md), and
[refactoring](skills/simple-code/references/refactoring.md).
[Provenance](skills/simple-code/references/provenance.md) separates the four
primary influences (Grug, Worse Is Better, A Philosophy of Software Design, and
The Laws of Simplicity) from added heuristics and house defaults. No principle
here outranks correctness, security, accessibility, or explicit requirements.

## Install and invoke

The plugin is skills-only: no server, hook, authentication, or background process.

**Codex:**

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add simple-code@mcook-plugins-local
```

Start a new task and invoke `$simple-code:simple-code`.

**Claude Code:**

```sh
claude plugin marketplace add MylesMCook/mcook-plugins
claude plugin install simple-code@mcook-plugins
```

Start a new session and invoke `/simple-code:simple-code`.

**Factory Droid:**

```sh
droid plugin marketplace add MylesMCook/mcook-plugins
droid plugin install simple-code@mcook-plugins --scope user
```

**Cursor:** install `simple-code` from the team marketplace backed by this
repository.
