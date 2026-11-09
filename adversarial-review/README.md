# Adversarial Review

> Retired from the marketplace on 2026-09-09. Use the adversarial-review skill in Thermos 0.3.0 or later. This source remains only for rollback and historical reference.

Adversarial Review is a momentum-first, skills-only Codex plugin for an
explicit high-scrutiny review. Invoke it and Codex infers the active target,
then immediately runs exactly three fresh reviewers through native Subagent V2:

- Skeptic: correctness, security, edge cases, and broken assumptions
- Architect: boundaries, coupling, rollout, and migration risks
- Minimalist: scope creep and unnecessary complexity

You do not need to switch permission modes, choose models, describe agent
mechanics, or separate unrelated worktree state. Reviewers can use inherited
tools and approval handling to run targeted tests, builds, linters, and
diagnostics. They investigate; they do not turn the review into an unsolicited
repair pass. The parent returns one evidence-backed `PASS`, `CONTESTED`, or
`REJECT` verdict.

The standard child wave gets three minutes before interruption is considered.
Reviewers still making visible progress can continue for up to five total
minutes. Stalled reviewers are interrupted, while a deeper wait happens only
when you explicitly ask for it.

You can invoke the skill repeatedly in one Codex task. Each review automatically
uses the next free shared run number for its three internal child names, so
completed or partial earlier runs cannot collide. The verdict still shows only
the useful Skeptic, Architect, and Minimalist labels.

## Why this is a plugin

The source format remains a normal `SKILL.md` with progressive-disclosure
references. The plugin is its installable distribution unit for the marketplace
and the ChatGPT desktop app; it does not need an app mapping, MCP server, hook,
or dedicated agent-profile configuration.

Implicit invocation is intentionally disabled because this workflow consumes
three independent V2 child runs. Use `$adversarial-review` or select the
installed plugin; that invocation is enough to start the workflow.

## Supported scopes

Name a target when you care about an exact boundary:

- a patch, plan, tight file list, or commit range
- staged or unstaged changes
- a named commit
- a branch or pull request against a base
- the last assistant turn

Otherwise the skill infers the narrowest relevant target from the active
request, tracked changes, branch diff, or current artifact. It excludes
unrelated state without asking you to manage the boundary.

## Install and use

After this catalog change is released, refresh the configured marketplace and
install the package:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add adversarial-review@mcook-plugins-local
codex plugin list | rg 'adversarial-review@mcook-plugins-local'
```

Then start a new Codex task. In the ChatGPT desktop app, open **Plugins** from
Work or Codex, choose the marketplace, install **Adversarial Review**, and
start a new task before using the bundled skill.

## Acceptance

The marketplace bundle is the canonical discoverable copy. After refresh and
installation, use the fast release gate below. Do not run a full three-reviewer
task merely to prove installation; it consumes three model runs and is
intentionally expensive.

## Fast release gate

```sh
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py adversarial-review
python3 -m unittest adversarial-review/tests/test_contract.py
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
if rg --hidden -n '[[:blank:]]$' adversarial-review; then exit 1; fi
git diff --check -- adversarial-review .agents/plugins/marketplace.json
codex plugin list | rg 'adversarial-review@mcook-plugins-local.*0\.3\.3'
diff -qr --exclude=__pycache__ \
  adversarial-review \
  ~/.codex/.tmp/marketplaces/mcook-plugins-local/adversarial-review
```

The deterministic contract tests and byte-for-byte installed-tree comparison
are the normal publish acceptance. See [`evals/README.md`](evals/README.md) for
optional behavioral cases when the user explicitly wants to spend the time and
tokens on a live trio.
