# Publication readiness

Objective: maintain a clean public plugin marketplace snapshot.

State: the reviewed source snapshot excludes the original repository's private
Git history, pull requests, Actions logs, internal notes and local-only skills.
The original history is preserved in a separate private repository.

Decisions:
- Preserve marketplace and plugin IDs.
- Configure Firecrawl endpoints in the user's own client.
- Use Microsoft's released Canvas Apps plugins rather than a local copy.
- Preserve per-component licenses; no blanket license is granted.

Verification: affected package/skill validators, isolated Firecrawl discovery,
13 builder tests and 8 Goalie tests passed before publication. Fabric dependency
notices cover all 231 checksum-verified locked registry archives.

Known detail: the unchanged Fabric executable retains compiler/Cargo paths with
its Windows build username. No personal-document paths or credentials were found
in those observed strings.
