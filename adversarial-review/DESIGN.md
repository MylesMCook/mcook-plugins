# Adversarial Review design

This package is a deliberate, skills-only distribution of the locally authored
`adversarial-review` workflow. It follows the relevant current OpenAI Codex and
ChatGPT app documentation checked on 2026-07-27.

## Decisions

| Decision | Reason |
| --- | --- |
| One bundled skill with references | Codex skills use progressive disclosure: metadata first, `SKILL.md` when chosen, and references only as needed. |
| Repo marketplace entry | A repo marketplace at `.agents/plugins/marketplace.json` is the documented catalog surface for the ChatGPT desktop app and Codex. |
| `agents/openai.yaml` with implicit invocation off | Optional skill metadata controls desktop presentation and invocation policy. Three subagents are expensive enough that routine review should not silently invoke this workflow. |
| Native Codex Subagent V2 only | The workflow uses the current spawn, supervision, and wait surface. It has no legacy agent, task/thread workaround, external runtime, or single-agent fallback. |
| Three fresh V2 children | Skeptic, Architect, and Minimalist are prompt lenses. One automatically selected shared run number produces valid, repeat-safe names such as `skeptic_r2`, without pretending task names select agent profiles. |
| Repeat-safe in one parent task | Before spawning, the parent skips every run number reserved by a running, completed, failed, interrupted, or partial earlier trio. Repeated invocation needs no fresh parent task or user intervention. |
| Invocation is sufficient | Explicitly selecting the skill authorizes the trio. The workflow infers a narrow target and never asks the user to configure permissions, agents, models, or ordinary scope separation. |
| Momentum-first routing | Prefer V2 `default` on `gpt-5.6-terra` with high reasoning when exposed and use fresh contexts. Allow three minutes normally, extend active progress up to five minutes, and interrupt stalls. |
| Inherited tools and automatic approvals | V2 children use the parent task's tools, permission mode, and approval handling—including automatic approval review when active—to run targeted diagnostics. They investigate freely but do not implement fixes or create external side effects. |
| Source-integrity audit | Before/after tracked-source fingerprints catch accidental edits while ignoring ordinary build and test caches. |
| One canonical discoverable skill | The marketplace bundle is the canonical source. The retired same-named standalone copy is not part of acceptance or rollback. |
| No MCP, hook, app, or repair loop | The job is a focused review procedure. Additional integration surfaces would add permissions, trust requirements, or state without improving the review contract. |

## Official documentation

- [Skills and progressive disclosure](https://developers.openai.com/codex/concepts/customization#skills)
- [Skill creation, metadata, and distribution](https://learn.chatgpt.com/docs/build-skills)
- [Plugin structure and manifest paths](https://developers.openai.com/codex/plugins/build#plugin-structure)
- [Marketplace metadata and desktop-app catalog behavior](https://developers.openai.com/codex/plugins/build#marketplace-metadata)
- [Subagent orchestration](https://learn.chatgpt.com/docs/agent-configuration/subagents#orchestration-and-thread-controls)
- [Subagent approvals and sandbox inheritance](https://learn.chatgpt.com/docs/agent-configuration/subagents#approvals-and-sandbox-controls)
- [Subagent models and reasoning](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning)
- [Code-review scopes](https://learn.chatgpt.com/docs/code-review#choose-a-review-scope)
- [Plugin installation and new-task behavior](https://learn.chatgpt.com/docs/plugins#use-and-install-plugins)

These links justify the package shape. They do not change the skill's strict
three-lens contract or authorize unsolicited implementation or external side
effects during a review.
