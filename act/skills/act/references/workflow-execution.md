# Select, preview, and execute a workflow

## Inspect the whole selected execution chain

Read the workflow before any act invocation that could run jobs. Inspect event
conditions, inputs, job IDs, `needs`, matrix inclusion/exclusion, `runs-on`,
container/service definitions, environment, permissions, local actions, reusable
workflows, and scripts or package commands invoked by steps. Follow transitive
dependencies. Resolve external action/workflow references sufficiently to assess
their relevant behavior; use current official/version-matched sources rather than
guessing. Missing or opaque execution paths are a scope gap, not permission.

Choose a test/lint/build job that answers the task. A build can publish artifacts
or contact production. Act can ignore GitHub permission and environment protections;
their presence does not authorize or contain a local external write. If a selected
job has an unsafe dependency, choose another suitable job or report the blocked
selection. Do not edit workflows, add bypass conditions, or sever `needs` solely
to get a local pass.

## Compatibility and limits

| Check | Required decision |
| --- | --- |
| Linux runner label | Verify its existing mapped image and required tools. Preserve approved digests; diagnose absent mappings rather than accepting a first-run survey. |
| Host/image architecture | Match the job's requirements and runtime support. amd64 on ARM may use emulation; do not silently select ARM to make an amd64 job pass. |
| macOS / Windows runner | Linux containers do not prove native behavior. Host runner execution needs explicit authorization and matching host prerequisites. |
| Matrix | Select actual supported values; inspect `include`, `exclude`, and dependencies. Check the executed count, since an excluded selection can yield zero jobs. |
| Container/services | Inspect privileged settings, socket/host mounts, networking, published ports, images, resource options, and service demand as well as job limits. |
| Credentials/private actions | Identify required keys and approved input sources. Missing authorization blocks secret-dependent execution, not other independent checks. |
| Event context/OIDC | Supply only necessary synthetic event/input data. Diagnose unsupported context/authentication; do not fetch private events or invent production credentials. |
| Cache/artifacts | Disable unneeded listeners. If required, agree on scoped storage and a permitted bind address; do not silently open public listeners. |
| Resources/deadline | Use bounded concurrent jobs and CPU/memory settings. Workflow `container.options` can replace act's container defaults. Bound service containers separately where needed. |

Consult the installed release and [unsupported functionality](https://nektosact.com/not_supported.html)
when a result depends on GitHub semantics. The current guide lists ignored
workflow concurrency, job permissions, job timeouts, and environment protections,
plus incomplete GitHub context and missing OIDC. Keep an independent process
deadline; arrange run-specific cleanup after cancellation. A tool's output-yield
timeout is not necessarily a process deadline.

## Construct one reviewed selection

Start in the repository so invocation-directory configuration is predictable.
The following is an example shape, not a universal runner configuration:

```sh
act workflow_dispatch -W .github/workflows/ci.yml -j test --matrix node:22 --list
act workflow_dispatch -W .github/workflows/ci.yml -j test --matrix node:22 --dryrun
act workflow_dispatch -W .github/workflows/ci.yml -j test --matrix node:22
```

Use the actual event/job/matrix supported by the workflow. With the installed
extension, replace `act` with `gh act`. Invoke arguments as separate tokens and
quote paths for the actual shell. For PowerShell use `&` with the resolved binary
and an argument array; do not evaluate a command string. Set any endpoint override
only in the child process, or save and restore the previous process environment
in `finally` when the shell requires it.

Apply the same inspected endpoint, runner, input, and safety arguments to listing,
preview, and execution. Confirm each flag with installed `--help`. Where needed
for an ordinary credential-free container test, supported per-run safeguards are
`--secret GITHUB_TOKEN=`, `--container-daemon-socket=-`, `--no-cache-server`, and
explicit approved empty files for default secret/env/var/input loading. Preserve
compatible existing settings. These flags do not override every workflow
container option or make an uninspected workflow safe.

Review `--env` settings such as cache URLs and artifact-server options from every
config source. A configured artifact server needs explicit handling; disabling
the cache server alone does not disable it. Dry-run disables job container
creation, but initialization can still load secrets, start cache/artifact
listeners, fetch action metadata, or prompt/write runner configuration. Avoid
unapproved initialization effects before listing or previewing.

For a finite run, avoid watch/reuse/bind/privileged behavior. Verify existing images
before allowing a pull; preserve configured pull/offline choices. An image pull
or action download may be required and is not evidence that tests ran. Diagnose
network restrictions without broadening host access or upgrading dependencies.

## Evidence and recovery

Capture the selected workflow/event/job/matrix, sanitized command, start/end,
exit status, executed job/step counts, expected assertions, and failure location.
Keep logs local, filtered, and out of Git; secret masking does not guarantee that
arbitrary scripts will keep values private. Avoid verbose logs for sensitive runs.

Use before/after IDs, start timestamps, restart counts, runtime/health status, and
run-specific resource names when checking shared-runtime impact. Obtain only the
needed inspect fields, never whole container/environment dumps. After failure or
deadline cancellation, remove only this run's disposable resources. `--rm` can
help with failure cleanup where supported; do not use broad prune operations or
stop containers selected only by a generic `act` name prefix.

Separate a workflow assertion failure from a missing runner tool, unsupported
feature, unreachable engine, image issue, or insufficient capacity. Report which
assertions ran. Listing, dry-run, zero jobs, skipped assertions, mocks, or an
unsupported runner are not successful acceptance tests. Hosted CI, private
integrations, native runners, and reboot persistence remain separate evidence.

## Sources

- [Selection, events, inputs, and matrices](https://nektosact.com/usage/index.html)
- [Runner mappings and host execution](https://nektosact.com/usage/runners.html)
- [Unsupported functionality](https://nektosact.com/not_supported.html)
- [Act v0.2.89 initialization and dry-run ordering](https://github.com/nektos/act/blob/v0.2.89/cmd/root.go)
