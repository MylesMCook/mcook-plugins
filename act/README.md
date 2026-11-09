# Act

Use the current machine's installed [nektos/act](https://github.com/nektos/act) to
validate and debug GitHub Actions locally. The plugin checks the installation,
configuration, container endpoint, and selected workflow before running a job.

Invoke `$act` directly, or let it activate when an existing CI test job would
help authorized coding work. Examples:

- "Use act to run this repository's Linux test job locally."
- "Check whether this machine can run our pull-request checks with act."
- "Debug this CI failure locally and distinguish workflow errors from act gaps."

The skill prefers an installed `act` binary and supports an existing `gh act`
extension. Discovery instructions cover macOS, Linux, and Windows, including
platform-specific configuration paths and Docker's active endpoint. They do not
assume the setup on the plugin author's machine.

Missing prerequisites produce a diagnosis and a proposed remedy. Installation,
host changes, shared-service restarts, credential forwarding, host runners, and
privileged access need applicable authorization. A test request does not authorize
deployment or publication through a workflow. Local success supplements hosted CI.

The package contains one skill and focused references, with portable and OpenAI
manifests. It has no MCP server, hooks, background service, or new runtime dependency.
Machine discovery uses the tools already available to the calling assistant.

Install from the Git-backed marketplace:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add act@mcook-plugins-local
```

Start a new task after installation. Building this source package does not publish
it, refresh the marketplace, or change the user's active installation.
