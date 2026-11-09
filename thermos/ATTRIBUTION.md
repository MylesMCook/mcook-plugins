# Attribution

Thermos is a curated Codex-native adaptation of the MIT-licensed Thermos plugin
from Cursor's public plugin repository.

- Source revision: `dc415439eebed0cd8fddb11e896dee43bce9d8b0`
- Source tree: https://github.com/cursor/plugins/tree/dc415439eebed0cd8fddb11e896dee43bce9d8b0/thermos

The three-skill boundary, paired-review idea, and parts of the review rubrics
were adapted. The implementation was rewritten around Codex skills, progressive
disclosure, normal parallel subagents, explicit diff scope, parent-side finding
verification, and an opt-in repair loop. No upstream logo or other binary asset
is included.

The upstream and local copyright notices are preserved in `LICENSE`.

Version 0.3.0 adds a locally authored three-lens entrypoint based on the user's
Adversarial Review workflow. Its concise rubrics and shared contract are newly
written here; no third-party adversarial-review source or assets are vendored.
