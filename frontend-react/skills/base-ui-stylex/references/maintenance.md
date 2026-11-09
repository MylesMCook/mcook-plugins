# Maintaining Base UI + StyleX

## Edit the plugin source

The authoritative source is [mcook-plugins/frontend-react/skills/base-ui-stylex](https://github.com/MylesMCook/mcook-plugins/tree/main/frontend-react/skills/base-ui-stylex). Make skill, reference, and OpenAI metadata changes there. `stylex` is also maintained in that plugin repository. Installed plugin caches are generated copies, never authoring locations.

Validate the edited skill and plugin, bump the plugin version, and follow the repository's normal release and installation workflow. The third-party upstream sync does not own or overwrite either skill. Updating this plugin requires no mcook-skills edit or source-pin change.

## Optional standalone export

The [mcook-skills copy](https://github.com/MylesMCook/mcook-skills/tree/main/skills/base-ui-stylex) is a standalone distribution of this skill. It may lag the plugin until a standalone refresh is requested; it never supplies updates to the plugin.

When refreshing that distribution, use the committed plugin source and copy the complete skill directory outward, including this reference and metadata. Inspect the destination for local edits first and preserve unrelated work. Verify directory parity, run mcook-skills frontmatter/discovery/install checks, and record the plugin source commit in the export commit message. Follow the existing release authorization. Do not maintain divergent behavior in the exported copy or add a reverse sync.

Both distributions keep live official documentation lookup and the same component/styling ownership boundaries. No runtime dependency on the other repository is introduced.
