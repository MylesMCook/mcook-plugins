# Code Comments

Add or improve comments so humans can understand and review code written by
LLMs. Explain the approach, unfamiliar domain concepts, important assumptions,
and decisions that are easy to miss. Also audit stale or misleading prose and
document public contracts. One shared skill works across languages and harnesses.

Use it whenever the task is about source comments or API documentation:

- “Improve the comments in this package without changing executable code.”
- “Add comments so I can understand and review this generated code.”
- “Add useful documentation to this API.”
- “Audit these comments against the implementation.”

The skill inspects implementation, callers, tests, and task requirements before
describing behavior. It gives a human reviewer a mental model, explains useful
constraints and rationale, permits no edit when the code is
already clear, and preserves directives and unresolved TODOs. An audit stays
read-only unless fixes are requested. A requested policy is proposed; applying
it to `AGENTS.md` requires that instruction.

The [research review](skills/code-comments/references/research.md) distinguishes
empirical findings and their limitations from editorial judgment, including the
limits of applying comment research to human review of generated code. The
[language guide](skills/code-comments/references/language-conventions.md) covers
Go, Python, JavaScript/TypeScript, Rust, Java, C#, and adapting the workflow to
other languages. [Examples](skills/code-comments/references/examples.md) show
what earns a comment. Comments have no count or density target.

The [readability guide](skills/code-comments/references/readable-comments.md)
adapts Writer's workflow and relevant references for source comments: put the
fact first, name the mechanism, cut filler and repeated setup, and preserve
technical qualifiers. Writer need not be installed to use this skill.

## Install and invoke

Requires a harness that supports Agent Skills and access to this repository.
The plugin has no runtime dependency, server, hook, authentication requirement,
or background process. It uses the target project's existing tools.

**Codex:** in the connected Git marketplace:

If this source is not configured on the machine, register it first:

```sh
codex plugin marketplace add https://github.com/MylesMCook/mcook-plugins.git --ref main
```

Refresh the configured source and install:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add code-comments@mcook-plugins-local
```

Start a new task and invoke `$code-comments:code-comments`, or ask to add,
improve, or audit comments. Normal skill discovery remains enabled.

**Claude Code:** in the repository's Claude marketplace:

```sh
claude plugin marketplace add MylesMCook/mcook-plugins
claude plugin install code-comments@mcook-plugins
```

Start a new session and invoke `/code-comments:code-comments`.

**Cursor:** install `code-comments` from the team marketplace backed by this
repository. Invoke `/code-comments` or ask for comment improvements. The root
portable manifest and the repository's Cursor catalog supply the same skill.

**Other Agent Skills hosts:** use
[`skills/code-comments/`](skills/code-comments/) through the host's supported
skill installation mechanism. Installation and invocation syntax are host-owned.

One `SKILL.md` is canonical. Root `plugin.json` supplies Agent Plugins metadata;
`.codex-plugin/plugin.json` supplies OpenAI compatibility; the repository's
Claude catalog supplies Claude metadata and default `skills/` discovery. This
follows the existing repository convention, so no per-plugin Claude or Cursor
manifest is needed. See [portability evidence](tests/verification.md) for what
was actually checked and any remaining limits.

This is a general commenting companion derived from the owner's Gommenter Go
workflow. It does not remove or replace that installed skill. The research is
summarized in original prose; paper PDFs and third-party text are not bundled.

Primary packaging references checked 2026-10-02:
[Agent Plugins](https://agent-plugins.org/specification),
[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins),
[Claude manifest and discovery](https://code.claude.com/docs/en/plugins-reference),
and [Cursor plugin formats](https://cursor.com/docs/reference/plugins).
