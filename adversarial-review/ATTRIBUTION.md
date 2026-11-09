# Provenance

This package descends from a locally authored skill that was formerly kept at:

```text
~/.agents/skills/adversarial-review
```

That standalone copy was retired after the marketplace migration. This plugin
is now the canonical source. Version 0.2.0 replaces the original orchestration
contract with native Codex Subagent V2-only routing, supervision, and
verification. Version 0.3.0 makes invocation momentum-first and lets reviewers
use inherited tools and approval handling for stronger diagnostic evidence.

No third-party code, connector, model, or visual asset is bundled. The original
local source did not include a license file, so this package intentionally does
not assert a license. Add one only after its owner selects the intended terms.
