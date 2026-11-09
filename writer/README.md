# Writer

One skill for drafting, rewriting, reviewing, and cleaning up prose.

```text
$writer Rewrite this email so the ask is clear without changing the facts.
$writer Remove generic AI-writing patterns while preserving my voice.
```

The main workflow protects facts, uncertainty, audience, and intent. Cleanup
references load only when relevant. Examples are not sources of facts to add
to a draft, and the skill does not claim to detect authorship or evade detectors.

Version 0.2.0 consolidates `writing-clearly-and-concisely` and `human-writing`
under `writer`. Their useful references remain in the package; use `$writer`
for future explicit invocations. Document layout and routine assistant replies
do not automatically select this workflow.

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add writer@mcook-plugins-local
```

Start a fresh task after updating. No tools, hooks, MCP server, or background
state is added. Existing source notices are retained with the references.
