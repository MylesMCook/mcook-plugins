# Changelog

## 0.2.4 - 2026-10-10

- Add a reusable native feedback watch-and-fix workflow to the existing Wails skill.
- Route short watch/fix requests directly to comment handling, verification and recovery.
- Continue after normal timeouts and app restarts, with explicit stop/pause behavior.
- Preserve local-review defaults and approval boundaries without hooks or background jobs.

## 0.2.3 - 2026-10-10

- Connect Codex once through a stable stdio launcher that discovers each private run.
- Keep tools available while the app is closed and reconnect after app/port changes.
- Preserve existing Agentation tools without another service, listener or dependency.
- Add idempotent connection/disconnection commands that protect unrelated registrations.
- Verify offline recovery, comment resolution after restarts and no interrupted-write replay.
- Include the connection regression in generated apps and the three-platform kit CI.

## 0.2.2 - 2026-10-10

- Avoid rewriting an already-correct Windows state-directory owner.
- Keep owner/SYSTEM-only ACLs and support ordinary, non-admin desktop launches.
- Select the built-in Windows security module even when launched from PowerShell 7.
- Add a regression for owners without ownership permission and incompatible caller modules.
- Verify Burf feedback from its normal Windows checkout through native WebView2,
  comment retrieval and resolution, hot reload, and browser-pane isolation.

## 0.2.1 - 2026-10-10

- Preserve LF/CRLF when wiring TypeScript and retaining private state ignores.
- Validate Windows ACL fixtures through canonical temporary paths.
- Cover both line endings in exact-source restoration and safe reinstall checks.

## 0.2.0 - 2026-10-10

- Add reversible React/Vite native-feedback setup with split Wails layouts.
- Preserve existing development workflows and trusted-window security.
- Keep feedback off by default and exclude it from release builds.
- Separate macOS and Windows implementation and native verification.
- Keep native StyleX CSS refreshes from blocking JavaScript hot reload.
- Preserve private data protection on undo and reject active-run mutations.
- Prepare startup modules before native launch and reuse Vite dependency caches.
- Overlap frontend preparation and Go compilation with bounded readiness checks.

## 0.1.0

- Add a Wails skill that resolves v2/v3 dependencies before reading live docs.
- Route v3 through its official llms.txt and v2 through official docs/MDX.
- Add a small source index with version checks and upstream path discovery.
- Distinguish browser checks from native desktop and platform verification.
