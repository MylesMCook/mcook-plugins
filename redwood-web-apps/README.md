# RedwoodSDK Web Apps

Build, change, and verify RedwoodSDK React applications on Cloudflare with
current official documentation. A separate alternative to Hono Web Apps for
full-stack React work; installing it does not replace Hono or migrate any app.

## Use it

- “Use RedwoodSDK Web Apps to build this Cloudflare app.”
- “Evaluate RedwoodSDK versus Hono for this project before changing anything.”
- “Fix this rwsdk server action and verify the browser flow.”

The plugin contains one `redwood-web-apps` skill. It reads the live
[RedwoodSDK docs index](https://docs.rwsdk.com/llms.txt) and relevant pages,
checks examples against installed versions, and verifies real application
behavior. It distinguishes RedwoodSDK from legacy RedwoodJS and keeps
experimental APIs explicit.

New React work defaults to strict TypeScript and StyleX, with a real compiler
integration check. Existing styling, frameworks, and data are preserved unless
the requested change includes them. Cloudflare deployment remains a separate
authorization boundary from local development.

No MCP server, hook, background process, bundled framework, or API key is needed
for the plugin itself. Application development needs the project's own tooling
and access to documentation; deployment needs its own Cloudflare credentials.

## Research and validation

Three Luna research passes covered architecture, runtime/deployment, and fit
against the Hono workflow. [Research notes](RESEARCH.md) record sources and
design decisions. The skill keeps procedural guidance and links rather than
copying the documentation or pinning applications to the research version.

Package checks validate portable Agent Plugins metadata, OpenAI compatibility,
skill metadata, references, and catalog mapping. Behavioral evaluation cases
live in [evals/cases.md](evals/cases.md). These checks do not prove that a future
application builds or deploys; the skill requires project-specific verification.

## Install from the published marketplace

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add redwood-web-apps@mcook-plugins-local
codex plugin list --marketplace mcook-plugins-local
```

Start a new Codex task after installation. Invoke `$redwood-web-apps` or select
RedwoodSDK Web Apps. Installation is left to the user unless requested.

Original workflow, licensed under [MIT](LICENSE). RedwoodSDK is a separate
upstream project; this plugin is not an official RedwoodSDK distribution.
