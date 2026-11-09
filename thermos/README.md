# Thermos

One package for independent review with shared scope and evidence verification.

| Skill | Job |
| --- | --- |
| `thermos` | Two parallel lenses: correctness/security and maintainability. |
| `adversarial-review` | Three parallel lenses: Skeptic, Architect, Minimalist; supports plans and patches. |
| `thermo-nuclear-review` | Explicit single correctness/security lens. |
| `thermo-nuclear-code-quality-review` | Explicit single maintainability lens. |

Use one mode per request. Ordinary quick reviews and full-repository security
scans remain separate. Both multi-reviewer modes verify findings against one
scope identity and disclose missing coverage. The parent owns any explicitly
requested fixes; reviewers remain read-only.

`Run Thermos` retains its two-reviewer meaning. `Run an adversarial review`
selects the three-reviewer skill. Paired review retains its patch verdict;
adversarial review retains PASS/CONTESTED/REJECT with remaining findings shown.

## Migration

Version 0.3.0 incorporates the standalone Adversarial Review workflow. Install
and verify this replacement before removing `adversarial-review` or loose
Thermos skills. Retired source remains recoverable from Git history and the
machine's consolidation backup.

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add thermos@mcook-plugins-local
```

Start a fresh task after updating. See [evals](evals/README.md) for acceptance
cases and [design](DESIGN.md) for the shared contracts. No MCP server, hook,
custom-agent profile, or external service is bundled.

MIT; see [LICENSE](LICENSE) and [attribution](ATTRIBUTION.md).
