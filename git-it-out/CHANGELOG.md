# Changelog

## 0.1.1 - 2026-08-27

- Separate implicit skill discovery from authorization for external or
  destructive closeout actions.
- Require direct takeover language before push, merge, release, deployment,
  publication, tracker mutation, or branch deletion.
- Tighten the trigger description and default prompt without changing the
  closeout workflow.
- Add direct, indirect, incomplete, non-trigger, and safety eval cases with
  observable output assertions.

## 0.1.0 - 2026-08-27

- Package the standalone `git-it-out` workflow as a marketplace-owned skill.
- Preserve the existing skill ID, instructions, checklist, and invocation
  metadata.
- Add portable Agent Plugins 1.0.0 metadata and an OpenAI compatibility
  manifest.
