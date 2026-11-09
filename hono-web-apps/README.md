# Hono Web Apps

Evaluate, create, modify, test, and verify Hono web applications without making Hono or an adjacent
frontend tool the automatic answer.

## Component boundary

Version `0.1.0` contains one portable Agent Skill plus the OpenAI compatibility manifest. It has no
MCP server, hooks, scripts, starter templates, commands, custom agents, app, UI, or background state.

Its design follows the `simple-code` method without depending on that skill at runtime: establish
the real repository state, choose the smallest fitting design, make one local reversible change, and
verify observable behavior at stable boundaries.

The skill can use an already-configured `hono-docs` MCP server, project-local `@hono/cli`, or other
documentation tools, but none is bundled or required. `@hono/mcp` is intentionally excluded because
it is for building MCP servers with Hono, not for developing ordinary Hono applications.

## What it enforces

- Inspect repository instructions, manifests, lockfiles, installed versions, runtime, target, and
  existing conventions before recommending or changing anything.
- Preserve an existing framework unless migration is explicit, including the option to decide that
  Hono is not a fit.
- Apply the Hono/HTML/htmx/Vue/Tailwind ladder only to approved greenfield work.
- Keep `create-hono` and `@hono/cli` separate, project-local, version-aware tools.
- Refuse to scaffold over an existing path or permit an implicit `npx` installation.
- Use `hono request` as a quick probe, then run committed tests and the real runtime or browser path.
- State what was tested and avoid turning one-host proof into a Windows-and-macOS claim.

## Install after release

After this plugin is committed and published to `mcook-plugins-local`:

1. Close active Codex tasks using the plugin.
2. Run:

```text
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add hono-web-apps@mcook-plugins-local
codex plugin list
```

3. Confirm `hono-web-apps` is listed, then start a new Codex task so the current skill metadata is
   loaded.

## Existing skill migration

After installed-state acceptance passes, disable or remove the standalone `hono` skill so only
`hono-web-apps` owns the workflow. Do not remove the older skill before the replacement is installed
and verified in a fresh task.

## Sources and license

The workflow is an original synthesis informed by official Hono documentation, `honojs/cli`,
`honojs/create-hono`, and Yusuke Wada's `hono-skill`. See [ATTRIBUTION.md](ATTRIBUTION.md).

Licensed under MIT. See [LICENSE](LICENSE).
