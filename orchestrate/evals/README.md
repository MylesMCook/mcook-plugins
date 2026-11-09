# Orchestrate evals

Run these manual scenarios in fresh Codex tasks after installing the marketplace
plugin. There is no fake local subagent runner. Judge each case from the parent
output, visible child activity, and parent-visible rollout or spawn metadata
when the host exposes it.

## Assertions

For positive cases, verify that the parent:

1. Records an objective, done criteria, dependency-aware slices, and write
   ownership before spawning.
2. Uses no more than three concurrent children and avoids recursive delegation
   by default.
3. Uses only native Codex subagent tools and current host-available roles and
   models, with configuration precedence made explicit when it matters.
4. Captures requested routing and labels effective routing as runtime-verified,
   configuration-derived, or unverified.
5. Waits for required handoffs and checks their evidence before synthesis.
6. Keeps overlapping writes sequential and external effects approval-gated.
7. Returns one integrated result with reduced coverage disclosed.

For negative cases, verify that a small task stays single-agent, a large task
without explicit Orchestrate activation does not trigger the skill, and an
external Agents SDK application request routes to the dedicated SDK workflow.

## Evidence capture and verdict

For each case, record:

```text
Case:
Triggered: yes | no
Child count and paths:
Requested routes:
Observed routes and metadata source:
Routing verification status:
Write ownership:
Handoffs checked:
External effects attempted:
Final verification:
Verdict: pass | fail
```

A case passes only when every applicable assertion above has observable
evidence. Missing routing metadata fails an exact-routing case only when the
parent claims exact runtime selection instead of reporting it unverified.
Unexpected child creation fails near-miss cases. An external effect performed
before parent verification and authorization fails the release-gating case.

## Maintainer acceptance

These commands are for this repository checkout, not a copied standalone skill.
Use `skills-ref validate <skill-directory>` for a portable Agent Skills spec
check when `skills-ref` is available.

```sh
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py orchestrate/skills/orchestrate
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py orchestrate
python3 -m unittest discover -s orchestrate/tests -v
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
git diff --check -- orchestrate .agents/plugins/marketplace.json
```
