# Bug Reporter

Bug Reporter creates evidence-based reports that another person or agent can
reproduce, diagnose, fix, and verify without first excavating the original
conversation.

Its output is always a saved Markdown report: portable, diffable,
tracker-friendly, and easy for humans and agents to read. Chat receives a
clickable file link instead of a duplicate wall of Markdown. The report follows
a target tracker's required form when one is provided.

The plugin contains one portable skill, one adaptive report template, and one
defect-specific evidence guide. It has no MCP server, hooks, app, background
process, external dependency, or stored state.

## What it does

- Drafts from supplied evidence without launching an unwanted investigation.
- Safely investigates when the request actually calls for it.
- Improves incomplete reports without inventing missing facts.
- Adapts to repository issue templates, contribution rules, ownership, and
  security policies.
- Captures exact environments, atomic reproduction steps, actual and expected
  behavior, reproduction rates, regression windows, and minimal artifacts.
- Adds focused evidence for crashes, performance, concurrency, data,
  accessibility, builds, integrations, infrastructure, and security defects.
- Separates observations, inferences, and unknowns.
- Cuts preambles, duplicated facts, generic conclusions, and irrelevant fields.
- Produces acceptance criteria that a human or coding agent can turn into a
  regression test and fix verification.
- Saves every report as a `.md` artifact and returns only its clickable file
  link plus any essential safety or submission note.

Bug Reporter keeps one defect per report, omits irrelevant boilerplate, and
routes suspected vulnerabilities through private disclosure channels.

## Use it

Invoke the skill directly or ask Codex to create or improve a report:

```text
$bug-reporter turn these logs and reproduction notes into a fix-ready report
```

```text
$bug-reporter improve this issue without inventing the missing environment details
```

```text
$bug-reporter investigate this intermittent CI failure and draft the report
```

The skill creates the report. It does not patch the product, publish an issue,
or contact maintainers unless the user separately authorizes that action.

## Research basis

The workflow is an original synthesis of empirical bug-report research and
maintainer guidance:

- Bettenburg et al., [What Makes a Good Bug Report?](https://www.st.cs.uni-saarland.de/publications/details/bettenburg-tr-2008/)
- Chaparro et al., [Assessing the Quality of the Steps to Reproduce in Bug Reports](https://arxiv.org/abs/1906.07107)
- Johnson et al., [An Empirical Investigation into the Reproduction of Bug Reports for Android Apps](https://arxiv.org/abs/2301.01235)
- Mozilla, [Bug Writing Guidelines](https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html)
- Chromium, [Bug Life Cycle and Reporting Guidelines](https://www.chromium.org/for-testers/bug-reporting-guidelines/)
- Linux kernel, [Reporting issues](https://docs.kernel.org/admin-guide/reporting-issues.html)
- GitHub, [Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- GitHub, [Privately reporting a security vulnerability](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately)

The central finding is pleasantly unglamorous: precise reproduction steps,
minimal failing artifacts, exact observed behavior, and complete relevant
context save maintainers the most time. The skill makes those elements easy to
collect without pretending every defect needs the same form or the same word
count.

## Install

```sh
codex plugin add bug-reporter@mcook-plugins-local
```

Start a new task after installation or an update so Codex loads the current
skill.

## License

MIT. See [LICENSE](LICENSE).
