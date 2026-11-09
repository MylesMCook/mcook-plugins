# Attribution

The `buzz-cli` skill adapts
[`desktop/src-tauri/src/managed_agents/nest_skill.md`](https://github.com/block/buzz/blob/3ed623bb217bf9697b0ce4562529254977e0ea04/desktop/src-tauri/src/managed_agents/nest_skill.md)
from [Block's Buzz project](https://github.com/block/buzz) at upstream commit
[`3ed623bb`](https://github.com/block/buzz/commit/3ed623bb217bf9697b0ce4562529254977e0ea04),
licensed under the Apache License 2.0.

The source text was modified for this plugin by:

- treating `buzz` as an installed runtime dependency rather than a bundled
  executable;
- adding explicit authorization boundaries for external relay and repository
  writes;
- limiting automatic memory-patch conflict retries;
- removing the upstream skill-version field, which Codex skill metadata does
  not support;
- adding Codex and portable Agent Plugin package metadata.

Buzz and the upstream skill are copyright their respective contributors.
