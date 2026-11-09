# Thermos design

The portable plugin and OpenAI overlay distribute four focused skills. Paired
and adversarial review share scope resolution and parent-side verification in
`skills/thermos/references/review-contract.md`, and the common no-write child
contract in `skills/thermos/references/subagent-contract.md`.

The entrypoint selects reviewer count, rubric, and verdict. The two existing
single-lens skills remain explicit-only. Paired and adversarial entrypoints
match their own requested review modes; neither should trigger for an ordinary
fix or quick review. Do not invoke both modes for one request.

Inspect the host's actual native spawn surface. Use supported options and do
not install profile files or assume an API from another client. Missing native
reviewers leave coverage incomplete; the parent cannot substitute its own
imagined independent review. Only the parent integrates findings or performs
explicitly authorized repairs.

Package grouping and progressive disclosure follow OpenAI's
[skills guidance](https://developers.openai.com/plugins/build/skills).
Reviewer lenses, counts, scope rules, and verdict thresholds are this plugin's
choices, not requirements imposed by OpenAI.
