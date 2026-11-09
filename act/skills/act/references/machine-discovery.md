# Discover the current installation

Use bounded commands through the current assistant's permitted shell or process
tool. Give each probe a deadline of about 10 seconds. Use the task's actual shell;
WSL is a Linux environment, not automatically the Windows installation. Keep the
results in this task; do not create a machine inventory or persistent cache.

## Identity and command

On macOS/Linux, start with `hostname`, `uname -s`, `uname -m`, `pwd -P`, and
`git rev-parse --show-toplevel`. Resolve `act` with `command -v act` and inspect
other candidates with `type -a act` if there is ambiguity. Prefer an installed
executable over an unexplained alias or wrapper. Record the resolved path, then
use it for `--version` and `--help`.

On Windows PowerShell, use `[Environment]::MachineName`,
`[System.Runtime.InteropServices.RuntimeInformation]::OSDescription`,
`[System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture`,
`Get-Location`, and `git rev-parse --show-toplevel`. Use
`Get-Command act -All -ErrorAction SilentlyContinue` to identify an application
and invoke its resolved path with `&`. Do not assume a Homebrew path or POSIX shell.

If no standalone executable exists, check an installed `gh` and `gh extension list`
for `nektos/gh-act`. Confirm `gh act --version` and `gh act --help`, then use
`gh act` as the command prefix throughout. Do not install the extension or invoke
`gh auth token` as discovery. If neither exists, report the missing CLI and propose
the platform's official installation method for approval.

Record when these checks occurred. File modification time is not installation
time. Do not infer the package manager, installation date, or readiness from a
remembered setup folder. Inspect package-manager metadata only if needed for a
diagnosis, without updating it.

## Configuration and sensitive inputs

Change to the intended repository before invoking act. Its configuration in the
invocation directory is not necessarily the same as the directory passed via
`--directory`. Read applicable AGENTS.md and repository act guidance first.

Act appends arguments from platform configuration, home `.actrc`, invocation
`.actrc`, then CLI arguments. The platform file is `act/actrc` under the installed
version's config-home rules, not always `~/.config`.

For the verified act v0.2.89 / adrg/xdg v0.5.3 implementation:

| Environment | Platform config candidate before `act/actrc` |
| --- | --- |
| Linux | Valid `XDG_CONFIG_HOME`, otherwise `$HOME/.config` |
| macOS | Valid `XDG_CONFIG_HOME`, otherwise `$HOME/Library/Application Support` |
| Windows | Valid `XDG_CONFIG_HOME`, otherwise the user's Local AppData known folder |

Check the relevant paths without creating them. Verify changes against the
installed release's source if paths or parsing differ. Do not use `--bug-report`
to find paths: it prints raw configuration. Even help/version commands can create
the platform configuration directory in versions using `xdg.ConfigFile`.

Check the config candidate and its parent before those probes, using installed
package metadata or release source first when necessary. If the original platform
actrc is absent and act would create its directory, use a disposable task-local
`XDG_CONFIG_HOME` only in act's child process, including later list/preview/run
commands. Keep the real home and invocation-directory configs, record the absent
original platform file, and remove the scratch directory afterward. If the
platform actrc exists, preserve its source and existing directory. Do not point
discovery at a new persistent config directory or use the scratch override to
skip an existing config. If paths cannot be established safely, report incomplete
discovery and continue static inspection rather than triggering setup.

Process files locally and return only a sanitized summary. Treat environment
expansion as potentially secret-bearing. Do not `cat` these files into tool output
or run their text as shell code. Summarize:

- Runner-label mappings, image tags/digests, architecture, pull/offline behavior.
- Concurrent jobs, CPU/memory bounds, and workflow container overrides.
- Socket mounting, host runner mappings, binding, privileges, capabilities,
  networking, and sensitive volumes.
- Credential/input file paths and key names or presence, never values. Also check
  implicit `.env`, `.secrets`, `.vars`, and `.input` loading.
- Cache/artifact configuration, listener addresses, and ports. Sanitize endpoints
  containing credentials and avoid unrelated Docker configuration dumps.

Later scalar flags generally replace earlier values; repeatable flags accumulate
and can have their own precedence. For example, platform mappings and secrets
must be checked against the installed parser, not merged as a generic last-wins
dictionary. Duplicate secrets can override file values, including an explicitly
empty `GITHUB_TOKEN`. Resolve ambiguity before execution.

Do not assume secret-file absence prevents token discovery. Some act releases
obtain a default GitHub token through `gh`. For an ordinary credential-free run,
use a supported explicit empty `--secret GITHUB_TOKEN=` and approved empty input
files when needed to prevent implicit credential/environment loading. Use local
ignored scratch files, not values interpolated into command text. Supply actual
secrets only through an explicitly approved file/environment or secure user input;
never extract credentials from another tool or place values in argv/history.

## Runtime endpoint and readiness

Resolve `docker` or the existing compatible runtime's CLI. Inspect only the active
context name and its Docker endpoint, for example `docker context show` followed
by `docker context inspect CONTEXT --format '{{.Endpoints.docker.Host}}'`.
Determine whether `DOCKER_HOST`, TLS settings, wrappers, or act flags override the
endpoint. Read only relevant environment keys through local filtering.

Act does not automatically honor Docker contexts. If its discovered endpoint
differs from the intended existing runtime, use a process-local `DOCKER_HOST` for
that act invocation after verifying the endpoint and preserving required TLS
settings. Do not run `docker context use`, create a socket symlink, or overwrite
shell startup files. `--container-daemon-socket=-` disables socket mounting into
jobs; it does not disable act's connection to the engine.

Probe the exact endpoint through Docker's matching `--host` or `--context` options,
not whichever engine the default CLI happens to use. A narrow info format is:

```sh
docker --context CONTEXT info --format 'OS={{.OSType}} Arch={{.Architecture}} CPUs={{.NCPU}} MemoryBytes={{.MemTotal}} Server={{.ServerVersion}}'
```

For Windows named pipes, retain the discovered `npipe://` endpoint. For an existing
Podman-compatible API, retain its configured socket; do not start a new socket
service. Remote SSH/TCP endpoints require a task that authorizes that target. Do
not automatically fall back to a different engine, insecure TCP, or remote host.

| Observed result | Conclusion and next action |
| --- | --- |
| CLI missing | Propose installation; do not install automatically. |
| Permission denied / sandbox denial | Access unverified; use the supported approval path if authorized, never weaken permissions. |
| Endpoint missing / connection refused | Endpoint unavailable; check the existing runtime manager read-only before claiming it is stopped. |
| Probe timeout | Runtime unreachable within the deadline; report endpoint and error safely. |
| Engine responds | API readiness only; still inspect image, architecture, workflow, and capacity. |

If another task is changing the shared runtime, wait for stable readiness before
execution or before/after comparisons. Do not overlap its restart or recovery.

Use engine capacity, selected limits, and narrowly scoped current container usage
to assess room for a job. Physical host RAM is not the Docker VM allocation. Do
not run large work because a historical snapshot showed spare memory. Preserve
existing limits; diagnose inadequate or absent bounds before execution and propose
a bounded task-local change. Persistent allocation changes or service restarts
require approval and a recovery plan.

## Sources

- [Act configuration and usage](https://nektosact.com/usage/index.html#configuration-file)
- [GitHub CLI extension](https://nektosact.com/installation/gh.html)
- [Docker context limitation](https://nektosact.com/missing_functionality/docker_context.html)
- [Custom container engine](https://nektosact.com/usage/custom_engine.html)
- [Act v0.2.89 configuration/parser source](https://github.com/nektos/act/blob/v0.2.89/cmd/root.go)
- [Its dependency versions](https://github.com/nektos/act/blob/v0.2.89/go.mod)
- [macOS config paths](https://github.com/adrg/xdg/blob/v0.5.3/paths_darwin.go)
- [Windows config paths](https://github.com/adrg/xdg/blob/v0.5.3/paths_windows.go)

These source versions establish the path examples, not a required act version.
