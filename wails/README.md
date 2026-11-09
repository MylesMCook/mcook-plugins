# Wails

Build and investigate Wails apps using current official documentation matched to
the project's version. One skill, with no bundled server, hooks, credentials,
scheduled refresh, or copied framework manual.

Use `$wails` to research an API, implement a change, debug bindings, evaluate
Wails, or investigate an explicit v2 to v3 migration. Existing apps keep their
Wails major version and frontend stack unless changing them is requested.

## Documentation

[The small llms.txt index](skills/wails/references/llms.txt) points to upstream
sources. For v3, the skill fetches the official
[live llms.txt](https://v3.wails.io/llms.txt) and reads the relevant pages. For v2,
it uses the official site or raw GitHub MDX. Local dependency source and exact
release tags resolve differences between current docs and an installed version.
When paths move, the skill rediscovers them through upstream navigation or the
repository rather than depending on a frozen catalog.

No routine documentation-copy refresh is needed. Upstream URLs and retrieval
tools can still fail or change; the skill reports that limitation and falls back
to verified official source or local versioned code. Existing web/GitHub tools
or a configured Firecrawl connection provide retrieval; Firecrawl is optional.

## Verification provenance

On 2026-10-10, the existing self-hosted Firecrawl service returned HTTP 200 and
plain text for `https://v3.wails.io/llms.txt`. The v2 `llms.txt`, v3
`llms-full.txt`, and an installation URL with an added `.md` suffix returned 404.
GitHub's API and raw source confirmed the v2 `website/docs` and v3
`docs/mpress/content` directories on upstream `master`. These are dated checks,
not permanent promises about upstream endpoints.

The plugin's workflow and link annotations are original. Wails documentation
remains upstream under its own [license](https://github.com/wailsapp/wails/blob/master/LICENSE).

## Install

From the configured Myles Codex Plugins marketplace:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add wails@mcook-plugins-local
```

Start a new task after installation so the skill loads.

## Native feedback setup

The skill includes an opt-in Agentation feedback source kit for React/Vite Wails v3
apps. One command detects npm/pnpm and split layouts, wires Go/Vite/React, adds a
separate development command, and records reversible edits. It preserves normal
builds and keeps release feedback disabled. See
[setup and verification boundaries](skills/wails/references/native-feedback.md).

Codex connects once through the generated `feedback:connect` script. Each later
`dev:feedback` run is discovered automatically, including after app restarts and
port changes. The connection also loads while the app is closed and remains
reversible through `feedback:disconnect`.

## Watch and fix feedback

In a task on the app's machine and checkout, ask:

> Wails, watch and fix my Burf feedback.

The skill reads existing comments, acknowledges each change, verifies the fix,
replies and resolves it, then keeps watching for the next comment. It handles
timeouts and app restarts through the same connection. Fixes stay local until
you request delivery, and watching stops when you ask. See
[the watch-and-fix workflow](skills/wails/references/watch-feedback.md).

This runs in the active task. It creates no background service or automatic hook.

This remains an Agent Plugins portable skill with OpenAI compatibility. The
native desktop integration does not require a native-only package exception.
Agentation dependencies have separate upstream licensing; see [ATTRIBUTION.md](ATTRIBUTION.md).
