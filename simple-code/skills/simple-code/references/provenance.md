# Source Notes and Provenance

This skill is intentionally opinionated, but not every principle in it has the same provenance. Use this file to distinguish between the four primary influences, added engineering heuristics, and strong house defaults layered on top.

## Primary Influences

| Source | Core ideas reflected in this skill |
|---|---|
| Carson Gross, *The Grug Brained Developer* | skepticism toward speculative complexity, practical local reasoning, suspicion of excessive abstraction |
| Richard Gabriel, *Worse Is Better* | implementation simplicity, common-case-first design, shipping a smaller good thing before a larger theoretical one |
| John Ousterhout, *A Philosophy of Software Design* | deep modules, information hiding, interface comments, strategic programming |
| John Maeda, *The Laws of Simplicity* | reduction, organization, time savings, and acknowledgement that some complexity is irreducible |

These four works are the philosophical spine of the skill.

## Additional Named Patterns and Heuristics

The skill also uses several widely known engineering patterns and heuristics that do not come only from the four primary texts:

| Pattern or heuristic | Where it appears | Why it is included |
|---|---|---|
| Chesterton’s Fence | `references/refactoring.md` | protects against deleting code before understanding why it exists |
| Strangler Fig pattern | `references/refactoring.md` | practical model for incremental replacement rather than big rewrites |
| Boy Scout Rule | `references/refactoring.md` | encourages bounded local improvement during necessary changes |
| Monolith-first default | `references/architecture.md` | practical bias toward fewer distributed failure modes until a split is justified |
| Reversibility and staged change | `references/architecture.md` | lowers the cost of mistakes and supports incremental evolution |
| Structured logging and request correlation | `SKILL.md` | modern observability guidance for production debugging without high-noise log spam |
| Locality of behavior | `SKILL.md` | practical readability heuristic that complements anti-indirection guidance |

## How Strongly to Apply a Principle

Treat the four primary influences as the deepest defaults of the skill.

Treat added heuristics as strong but situational defaults.

Treat the most opinionated house guidance — for example, skepticism toward advanced type machinery in ordinary application code — as a prompt to justify the complexity, not as a universal ban.

## Precedence Reminder

No philosophy in this skill outranks correctness, security, privacy, accessibility, data integrity, explicit requirements, or binding legal and regulatory constraints. When a principle here conflicts with one of those, keep the requirement and isolate the complexity.
