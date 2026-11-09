# External Golang plugin

`cc-skills-golang@mcook-plugins-local` connects directly to
[Samuel Berthe's upstream repository](https://github.com/samber/cc-skills-golang).
The catalog tracks `main`. This marketplace contains no copied implementation.
Upstream publishes the package under the MIT license; the installed package
preserves its license and attribution.

## Update behavior

Refresh the marketplace and reinstall to fetch the current upstream revision:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add cc-skills-golang@mcook-plugins-local
```

Start a new task to load the installed skills. An active task does not continuously
pull upstream changes. Tracking `main` allows future upstream changes without a
catalog commit; those changes have not been reviewed by this marketplace.

## Native-only exception

The marketplace owner explicitly approved this external Codex-native package
and tracking upstream `main` on 2026-10-10. This approval overrides the builder's
portable-package release gate and full-commit-pin requirement for this entry.
The exception reflects the owner's choice to preserve upstream packaging;
no technical inability to add a portable core is claimed.

The reviewed upstream package has `.codex-plugin/plugin.json` and `skills/`,
with no portable root `plugin.json`. This entry is Codex-only in this marketplace;
it is not added to the Claude or Cursor catalogs. No Agent Plugins conformance
is claimed. Reconsider the exception if upstream adds a portable manifest or
the owner requests a pinned or repackaged distribution.

## Verified installation

Codex CLI 0.144.1 installed version 2.0.1 in a fresh isolated `CODEX_HOME`.
The tested upstream revision was
`8e899e20ff0cd4dc524af3993e4c62d8ee8c5717`.
Installation and listing reported `cc-skills-golang@mcook-plugins-local` enabled.
All 46 skill directories contained `SKILL.md`. SHA-256 comparison of all
324 tracked upstream files matched the fresh installed files, including LICENSE.

The builder's marketplace metadata check passes with zero warnings for the
reviewed commit. The final `main` selector is an owner-approved departure from
that validator's commit-pin policy, and is tested by a fresh installation.
The check does not establish portable package conformance or exercise Go
workflows. Desktop icons, clean-task activation, and skill behavior have not
been tested. The package declares no MCP server or automatic hooks.
