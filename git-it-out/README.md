# Git It Out

Git It Out packages the final repository-closeout workflow as a marketplace
skill. Use it when implementation is substantially complete and the remaining
work should be verified, committed, landed on main or the repository's actual
mainline, pushed, and carried through any configured release, deployment,
tracker, checkpoint, cleanup, and handoff steps.

The plugin preserves the standalone `$git-it-out` workflow and stable skill
name. It adds no MCP server, hooks, app, background process, external
dependency, or stored state. It uses the repository's existing tools and
documented finish line and does not invent or bypass release gates.

## Use it

Invoke the skill explicitly when you want complete last-mile ownership:

```text
$git-it-out finish this session and leave the repository landed, pushed, clean, and clearly handed off
```

The skill may also activate for clear closeout language such as "get it out,"
"ship this completed work," or "take this off my plate and finish it." A bare
statement such as "I'm done" or "I'm going to bed" does not authorize external
closeout actions. It is not a greenfield implementation, broad refactoring, or
open-ended debugging workflow.

External actions still follow the user's authorization and repository policy.
Implicit activation permits only read-only inspection and safe local
validation until the user directly requests closeout. The skill stops for an
ambiguous irreversible target, missing authority or credentials, or a failing
production-impacting gate that has no safe scoped fix.

## Install

```sh
codex plugin add git-it-out@mcook-plugins-local
```

Start a new task after installation or an update so Codex loads the
marketplace-owned skill.

## License

MIT. See [LICENSE](LICENSE).
