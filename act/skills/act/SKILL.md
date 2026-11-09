---
name: act
description: >-
  Discover and use the current machine's nektos/act installation to validate or
  debug GitHub Actions locally. Use when act is requested, or when local execution
  of an existing CI test job would help authorized coding work. Check the installed
  CLI, configuration, container runtime, and workflow before running. Do not use
  for unrelated meanings of act or generic tests without GitHub Actions workflows.
---

# Use act on this machine

Requires local command execution, an installed act CLI or gh act extension, and
a compatible container runtime for container jobs.

Use the machine's existing capability. Discover it again on each invocation;
previous paths, versions, endpoints, image mappings, and capacity are historical
context. This skill does not install a service or replace hosted CI.

## Discover before choosing a command

Read [machine-discovery.md](references/machine-discovery.md). Establish the current
host, OS, architecture, shell, repository, invocation directory, act command and
version, applicable configuration, and actual runtime endpoint. Recheck after
changing machines, repositories, configuration, or runtime.

Inspect configuration locally with values filtered before returning tool output.
Never dump `.actrc`, credential files, environment variables, Docker configuration,
or `act --bug-report`. Report credential names and presence only. Do not retrieve
tokens from another CLI or automatically pass ambient credentials to a workflow.

Distinguish missing CLI, missing or unreachable runtime, stopped runtime confirmed
by its manager, and permission/sandbox denial. A denied probe is not proof that
Docker is down. Diagnose unavailable prerequisites and propose the smallest remedy.
Installation, persistent configuration, shared-service restarts, privilege changes,
or larger resource allocations need applicable authorization. Do not bypass a
sandbox or silently change runtime/context.

## Select a suitable job

Read [workflow-execution.md](references/workflow-execution.md). Start from the
task's intended validation and inspect the exact workflow, selected job, transitive
`needs`, matrix, reusable workflows, local actions, and invoked scripts. Inspection
and review requests stay read-only unless execution is requested.

Choose one workflow file, an explicit event, a job ID, and the smallest useful
matrix subset. Do not run bare `act` against all workflows. A job named `test` can
still publish, deploy, mutate shared data, or invoke unsafe dependencies. Stop when
the execution chain cannot be inspected enough to establish authorized scope.

Use installed `--help` to confirm needed flags. Preserve compatible settings and
pinned images. Check architecture, image availability, container/service options,
resource limits, secret-file loading, and cache/artifact listeners before even a
preview. Do not change shared defaults to make a job pass.

Normal test authorization does not authorize publication, deployment, host runner
execution, Docker socket mounts, privileged containers, sensitive host mounts,
credential forwarding, or access to an unapproved remote runtime. Ask only for the
specific unresolved behavior or protected action; continue independent checks.

## Preview, run, and verify

1. List the selected workflow/event. Preview the selected job with `--dryrun`,
   using the same reviewed arguments planned for execution. Prevent first-run
   setup prompts and unapproved listeners or credential loading.
2. Run only the inspected, authorized selection with bounded concurrency,
   resources, and a process deadline. Act's workflow timeout/concurrency settings
   alone are not reliable safeguards. Keep workspace copying unless binding is
   explicitly authorized. Avoid `--watch` and `--reuse` for a finite test task.
3. Check that expected jobs, matrix entries, steps, and assertions actually ran.
   Zero jobs, skipped assertions, listing, and previews do not prove a pass.
4. On failure, separate workflow defects from act incompatibility, missing inputs,
   image/tool gaps, architecture, permission, connectivity, and resource limits.
   Do not weaken assertions or expand privileges to get green output.
5. Clean up only resources created by this run. Compare shared-runtime state when
   relevant. Do not prune caches, images, volumes, or unrelated containers.

## Report the outcome

Briefly state the checked machine and time, discovered command/version/runtime,
selected workflow/event/job/matrix, sanitized command, and actual result. Include
the failing step or exact prerequisite gap and one concrete next action. Link
local sanitized evidence when useful. State unexecuted or skipped coverage and
hosted-CI differences, including mocked services or credentials. Do not claim a
fresh install, another OS, reboot persistence, or hosted CI was tested without
observing it.
