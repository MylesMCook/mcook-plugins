# Native feedback for Wails v3

The reusable setup targets React + TypeScript + Vite with npm or pnpm and an
existing Wails v3 runtime. It detects Burf's split `app/` and `app/native/`
layout. Vue, Svelte and vanilla are detected and rejected before edits; no
frontend migration happens. They remain future adapters.

Run from the application repository root, using this skill's installed path:

```sh
node <wails-skill-root>/assets/native-feedback/setup.mjs .
```

Use `--dry-run` to inspect detection. Setup wires the native service, wraps the
existing Vite config, adds the React overlay, pins Agentation 3.1.2 and its MCP
companion 1.3.2 as development dependencies, and adds `dev:feedback`. It retains
existing scripts, plugin ordering, aliases and build options. No global
configuration or installed application changes.

For Burf, run `pnpm dev:feedback` in `app/`. The runner uses the existing
development script, including plugin compilation, and a free loopback port
between 1421 and 1439. It preserves Vite's dependency cache and versioned URLs,
which follow the lockfile and configuration. See
[Vite's dependency cache guidance](https://vite.dev/guide/dep-pre-bundling.html#caching).
Startup transforms the detected entry and feedback modules before opening the
native window. Burf additionally prepares its plugin host, App and existing Go
binding module. Preparation transforms source without executing app code or
changing the ordering of UI-state restoration. A development-only readiness
route returns status codes; it carries no application configuration or secrets.
The Go build overlaps frontend preparation. It compiles the shell once and keeps Vite hot reload
for frontend changes. Restart the command after Go changes. Ordinary `pnpm dev`
and existing release commands keep feedback disabled.

Feedback mode supplies native loopback HMR only when the app has no explicit
HMR configuration. For Burf's StyleX 0.19.1 full development runtime, it also
coalesces CSS refreshes outside Vite's serial HMR queue and bounds requests to
five seconds. A stalled CSS response cannot block later JavaScript updates.
Unrecognized StyleX runtime shapes fail explicitly. Normal development and
builds do not apply this adapter or edit installed package files.

Burf's development optimizer groups Lucide icons using the same rule as its
existing release build. This removes roughly two thousand native module requests
while preserving all 2,121 names and their dynamic SVG data. On mc-pc, the current
source reached the UI and toolbar in 14.5 seconds with a cold dependency cache,
and 4.7 seconds with a fresh WebView2 profile and retained dependencies. Complete
command-to-ready times were 26.4 and 24.2 seconds, including preparation and Go.
These are development launch measurements; installed release startup was not
the slow path under investigation.

Setup records its owned edits in `.wails-feedback/setup.json`. Commit this
receipt with the generated source. Rerunning setup is safe. Undo with the same
command plus `--undo`; unrelated later edits are merged back, and conflicting
owned edits stop before changing files. Dependency restoration follows the
restored lockfile. Never discard a conflicting file to force undo.
Close feedback before setup or undo; an existing run lock blocks mutations.
Undo preserves private annotations and profiles, retaining their `state/` Git
ignore rule. Reinstallation recognizes that exact protective rule. Private
data cleanup remains explicit, so undo never discards feedback history.

## Connect Codex once

From the detected frontend folder, run the package manager's `feedback:connect`
script once. For Burf's normal split layout, use:

```sh
pnpm --dir app feedback:connect
```

Start a new Codex task once after registration. Later runs need only
`pnpm --dir app dev:feedback`. One stdio connection reads the current private
session per request, including after app restarts and new ports. Its nine existing
Agentation tools load even when the app is closed. Offline calls explain how to
start feedback. Interrupted writes are never automatically replayed.

Use `feedback:disconnect` before setup `--undo`. Rerunning either connection
command is safe. A differently configured server with the same app-derived name
is preserved and reported as a conflict. Private comments are never deleted.
The registration helper is Codex-specific client integration. Other MCP clients
can configure the same generated `node wails-feedback/mcp.mjs` stdio launcher.
This does not register a global plugin server or start a persistent service.

## Trust and release boundaries

- Go requires both `dev,wailsfeedback` build tags and the private runner's
  runtime opt-in. The `production` tag always disables the bridge.
- Only the exact attached main native window can obtain its capability URL.
  No public asset configuration route exists. Burf's trusted marker, CSP and
  native browser isolation remain intact.
- The private proxy accepts only its capability, exact host and native origin,
  including Wails' development port. It forwards the toolbar's bounded API and
  SSE; companion MCP, accounts and bulk session routes stay outside it.
- Vite requires the serve command, explicit feedback mode and runtime opt-in. All
  builds eliminate the lazy feedback payload even with inherited opt-in.
  Burf's existing UI manifest workflow rejects feedback-marked bundles.
- The runner owns its companion, frontend and native process, private data and
  isolated development identity. It clears inherited Agentation cloud/webhook
  settings. No live agent/provider is used for setup acceptance.

`pnpm dev:feedback --inspect` additionally compiles Wails' development inspector
with a fresh private token. Inspector configuration is not part of the plugin
manifest and does not become a global MCP service. Use only this owned app for
native API checks. Session/token files remain under ignored private run state.

## Platform evidence

Verify macOS and Windows separately. Node/unit checks, browser fixtures and
cross-compilation do not prove native desktop behavior. Windows needs an
ordinary desktop session and Burf's verified WebView2 loader beside the
development binary. macOS uses a temporary bundle identity to isolate WebKit
storage. Keep installed Burf running and its profile untouched.

Acceptance evidence belongs in `tests/verification.json`, with exact source
version, commands, actual results and gaps. Do not claim the initial Feedback
Lab experiment proves Burf integration or the one-command path.

## Attribution and compatibility

Agentation's upstream license is PolyForm Shield, not this plugin's MIT
license. Preserve its license in redistributed material. The private companion
adapter verifies the exact upstream CLI version/hash, then changes only its
data-directory location in a generated copy. It never edits installed package
bytes or copies user credentials.

This is a portable skill and source kit with OpenAI manifest compatibility.
The generated Wails app is a native desktop feature; it is not a native-only
Agent Plugins package exception. No server is automatically registered by
installing the skill.
