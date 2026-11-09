# Tufte

Build and review charts and dashboards to a cited, Tufte-led design standard.

The `tufte` skill loads a rulebook of about 45 rules. Tufte supplies the philosophy; Cleveland & McGill, Few, Munzner, Brewer, WCAG and the empirical literature fill the gaps on screens, interaction and accessibility. Each rule names the default an LLM tends to produce, a severity, the inputs that can detect it, and a source with its verification status.

## Install

Claude Code:

```bash
/plugin install tufte --marketplace MylesMCook/mcook-plugins
```

Codex:

```bash
codex plugin add tufte@mcook-plugins-local
```

## Use

- **Build:** ask for a chart or dashboard as usual. The skill loads when you build or change a visual, applies the rules, and checks the result before handing it off.
- **Review:** ask for a review or critique of a screenshot, HTML/React/Vega-Lite code, a Power BI PBIR or Deneb spec, or a live page. You get at most 7 ranked findings with rule IDs, evidence, fixes and sources, plus a Keep list.
- **Claude Code:** the `tufte-critic` agent gives an independent second opinion on a finished page and edits nothing.

If the skill does not load on its own, name it: "use the tufte skill".

## Evidence

Tested on one-line dashboard requests ("Make a dashboard on our support costs this year") with synthetic data containing planted traps:

- Traps handled rose from 69% to 96% (Haiku) and 73% to 94% (Sonnet). Opus was already at 98%.
- In a blind review of 20 plain-versus-rulebook pairs, the owner preferred the rulebook build 15 to 5 (p = 0.041).
- Word budgets (v0.3) cut median page text from 454 to 208 words while traps held.
- As a reviewer, a stock Opus model already finds the planted problems; the rulebook adds consistent form and sources rather than detection.

Evals, prompts and results live in the source repository (`tufte-critic`, private).

## Limits

- Rulebook v0.4. Tufte page references marked `[B]` and five `[K]` items are not yet checked against the books. The v0.4 type-size and no-clipping rules have not been through a blind review.
- `[P]` rules are practitioner judgment and the skill says so.
- Screenshot-only reviews cannot confirm contrast ratios, scale functions or hover-only content.
