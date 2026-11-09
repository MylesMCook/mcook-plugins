---
name: cli-for-agents
description: >-
  Designs or reviews CLIs so coding agents can run them reliably: non-interactive
  flags, scoped --help with examples, stdin and pipelines, stable output,
  actionable errors, idempotency, dry runs, and predictable structure. Use when
  building a CLI, adding commands, writing --help, or reviewing terminal and
  automation workflows.
---

# CLI for agents

Design the command interface as a contract that a person, a CI runner, and a coding agent can use without guessing. Prefer a small, explicit, headless interface over a clever interactive flow.

## Start with the command contract

Before changing implementation, identify the command's inputs, effects, outputs, failure modes, and whether it mutates anything. Keep the surface narrow and fit it to the existing CLI's conventions.

- Use stable command and flag names. Prefer one clear spelling over aliases that behave differently.
- Make every required value expressible with a flag, argument, file, environment variable, or stdin.
- Use a consistent command grammar. If the CLI uses `resource list`, keep that order for comparable resources.
- Do not add a new wrapper command or output mode unless the task needs it.
- When flags, environment variables, profiles, config files, and defaults can all supply a value, document one precedence order and provide a redacted way to inspect the resolved target and configuration.
- Require an explicit target or profile when silently choosing one could affect the wrong account, environment, or resource.

## Non-interactive first

The default execution path must work without a TTY. Interactive prompts may be a convenience after all required values are supplied non-interactively; they must never be the only way to complete an operation.

```text
Bad:  mycli deploy
      ? Which environment? (use arrow keys)

Good: mycli deploy --environment staging
```

- Never require menus, arrow keys, timed prompts, or a browser for ordinary automation.
- Missing required input should fail immediately with a concise error and a correct invocation.
- If a command can prompt, provide a documented `--non-interactive` or `--no-input` mode that refuses every prompt, pager, browser launch, and credential dialog even when a TTY exists.
- Use `--yes` only to bypass a documented confirmation. It must not invent missing values or act as a synonym for `--force`.
- Let TTY detection change presentation only; do not let it change targets, defaults, authorization, or mutation semantics.

## Help that agents can discover incrementally

Agents normally inspect `mycli`, then `mycli deploy --help`. Keep help local to the command rather than printing the full manual at every level.

Every command and subcommand should support `--help`. Include valid, copy-pasteable examples that cover the normal path and any consequential option. Support a fast, side-effect-free `--version` when the installed version can affect behavior or output.

```text
Usage:
  mycli deploy --environment <name> --tag <tag>

Options:
  --environment <name>  Target environment (staging, production)
  --tag <tag>           Image tag to deploy
  --yes                 Skip the confirmation prompt

Examples:
  mycli deploy --environment staging --tag v1.2.3
  mycli deploy --environment production --tag v1.2.3 --yes
```

## Inputs and composition

- Accept stdin when it represents a natural input, and make the stdin contract explicit (for example, `--input -` or `--stdin`). Do not silently read stdin when a terminal user expects a prompt.
- Support file paths and flags as alternatives when both make sense.
- Preserve ordinary shell composition: `mycli build --output tag | mycli deploy --tag -` should not need temporary interactive state.
- Accept `--` as an end-of-options delimiter. For every relevant argument, document whether `-` means a standard stream or a literal filename.
- Do not accept secrets in positional arguments or ordinary flags. Prefer the existing credential store; if direct input is necessary, offer an explicit file, inherited descriptor, or `--*-stdin` path and document its permissions and precedence.
- For a mutable, machine-readable list, use a stable sort plus an opaque cursor that callers pass through unchanged. Document limit bounds, the terminal `next_cursor` value, invalid-cursor recovery, and whether traversal is snapshot-consistent or best-effort. Numeric pages are acceptable only when that limitation is explicit.
- Avoid ambiguous positional arguments and magic defaults that change according to terminal state, current time, or a hidden profile.

## Output and exit behavior

Success output should carry the information needed for the next command: identifiers, paths, URLs, state, and duration. Decorative output alone is not enough.

```text
deployed v1.2.3 to staging
url: https://staging.example.com
deploy_id: dep_abc123
duration: 34s
```

- Keep machine-readable output stable. When structured output is useful, provide an explicit mode such as `--output json` and document fields, types, nullability, ordering, and compatibility rules.
- In structured mode, write exactly the documented data format to stdout: no prose, color, progress, pager text, or duplicate JSON keys. Keep it backward-compatible when possible; introduce an explicit format version only when the output is a long-lived integration contract.
- Send the requested result to stdout and diagnostics, warnings, progress, and errors to stderr. Avoid color or progress spinners when output is not a TTY; offer `--no-color` when color is otherwise enabled.
- Return zero only after the command's documented success condition occurs. Use a non-zero exit status for invalid input, failed work, and unavailable prerequisites; if callers need different recovery, document a small stable taxonomy rather than reusing shell-reserved command-not-found statuses.
- Give structured failures a stable symbolic code, retryability, and any safe operation or request ID alongside the human diagnostic.
- Do not parse presentation text internally or force callers to scrape it. Expose IDs, paths, and structured fields directly.

## Fail fast with an actionable recovery path

Errors must name the bad input or failed dependency, state what the command did not do, and show the next valid command when one exists.

```text
Error: no image tag was supplied; nothing was deployed.
Try: mycli deploy --environment staging --tag <image-tag>
List tags: mycli build list --output tags
```

Do not hide an error behind a retry loop, a hanging prompt, or a generic "failed" message. Redact secrets before rendering normal, debug, dry-run, JSON, or recovery output; never dump credential-bearing headers, environment values, connection strings, or raw request bodies by default.

## Safe, retryable mutations

Coding agents retry commands. A successful retry should be a clear no-op or report the existing result, not create a duplicate side effect.

- Make create, apply, and deploy commands idempotent where the domain allows it.
- Require an explicit, bounded target for consequential mutations. Keep `--all`, broad selectors, and named targets mutually exclusive when combining them would be unsafe.
- Add `--dry-run` to consequential mutations. It should run the same validation, target resolution, authorization, and cascade planning as the real command, then make zero writes.
- For irreversible work, show a bounded plan before execution and require an explicit confirmation in interactive use.
- For duplicate-prone remote mutations, accept a caller-supplied request or idempotency key (or a deterministic resource identity). Reusing it with different parameters must fail clearly.
- State whether an already-absent resource is success. Make any `--ignore-not-found` behavior an explicit opt-in so it cannot hide a wrong target.
- Define completion precisely: request accepted, resource changed, or asynchronous operation finished. Return the durable resource or operation ID so a later command can inspect, resume, cancel, or roll it back.

## Remote, asynchronous, and retryable work

For commands that call remote services or submit background jobs, make waiting behavior bounded and observable.

- Document an end-to-end deadline, including connection, polling, and retry time. Never wait indefinitely by default.
- Define cancellation behavior: stop local work promptly, propagate cancellation when safe, clean up local temporary state, and say whether the remote outcome is cancelled, pending, or unknown.
- Retry only documented transient failures, with finite attempts and a visible timeout budget. Honor server-directed delays. Never automatically retry a non-idempotent mutation unless an idempotency guard proves the first attempt cannot duplicate work.
- If the command returns after submission, make that contract explicit with `--wait` or `--no-wait` where appropriate. Emit the operation ID and state; zero then means successful submission, while a waiting command returns zero only after its documented terminal success state.

## Review and delivery checklist

When reviewing an existing CLI, check the actual commands and help text where possible. Report concrete findings with the affected command, the agent failure mode, and the smallest safe fix.

- A non-interactive path exists for each normal and mutating command.
- `--help` is scoped, complete, and includes real examples.
- Input, stdin, file, pagination, and shell-pipeline behavior are explicit.
- Output, JSON modes, stderr usage, and exit statuses are usable in automation.
- Invalid input fails promptly with a recovery command.
- Retries are safe; mutations have dry-run and confirmation behavior proportionate to risk.
- Command grammar, naming, defaults, and output formats stay consistent across siblings.
- Closed stdin and a non-TTY never open a prompt, pager, browser, or spinner; `--help` exits zero without mutation.
- A dry run makes zero writes, and a destructive non-interactive command without its explicit confirmation fails before changing state.
- Structured output parses without filtering prose; a cursor-based list can be followed until its documented terminal cursor value.
- Remote commands have a finite deadline and preserve a durable operation ID when cancellation or timeout leaves the outcome pending or unknown.

For an implementation task, make the smallest compatible change, update relevant help and examples, and run the narrowest real commands or tests that prove the contract.
