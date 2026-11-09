# III. Elementary Principles of Composition

Use this file for substantial drafts and rewrites. It turns the classic rules into practical editing moves.

## 1. Make each paragraph do one job

A paragraph should advance one idea, decision, instruction, or piece of evidence. Split a paragraph when the reader’s task changes.

Weak:
> The migration is complete. The rollback plan is in the runbook. We should also update the onboarding guide because new engineers still use the old command.

Better:
> The migration is complete. The rollback plan is in the runbook.
>
> We should also update the onboarding guide. New engineers still use the old command.

## 2. Put the point early

For most practical writing, start with the answer, request, decision, or outcome. Background comes after.

Weak:
> After reviewing the logs and checking the deploy history, I noticed a pattern that may explain the incident.

Better:
> The incident likely came from a stale cache after deploy. The logs and deploy history show the same pattern.

## 3. Use active voice by default

Active voice is usually clearer because it names the actor.

Weak:
> The configuration file is read by the application at startup.

Better:
> The application reads the configuration file at startup.

Use passive voice when the actor is unknown, irrelevant, or less important than the receiver:

> The account was locked after five failed attempts.

## 4. Put statements in positive form

Tell the reader what is true or what to do.

Weak:
> Do not forget to rotate the token.

Better:
> Rotate the token.

Weak:
> This is not available for free plans.

Better:
> This requires a paid plan.

## 5. Use definite, specific language

Replace vague abstractions with concrete subjects, verbs, and evidence.

Weak:
> Several improvements were made to enhance reliability.

Better:
> The worker now retries failed uploads three times and logs the final error.

Weak:
> The feature improves collaboration.

Better:
> The feature lets reviewers comment on draft invoices before approval.

## 6. Omit needless words

Cut words that do not change meaning.

- `in order to` → `to`
- `due to the fact that` → `because`
- `at this point in time` → `now`
- `a number of` → `several` or the exact number
- `is able to` → `can`
- `make a decision` → `decide`
- `perform an analysis` → `analyze`
- `provide assistance` → `help`

Do not cut terms of art, caveats, or legally required language.

## 7. Avoid monotony

A row of same-shaped sentences can sound generated. Vary length and structure when it helps rhythm, but do not add ornament for its own sake.

Weak:
> The CLI validates the config, and it writes the output, and it reports errors, and it exits with a status code.

Better:
> The CLI validates the config, writes the output, reports errors, and exits with a status code.

## 8. Use parallel structure

Make similar ideas look similar.

Weak:
> The script checks schema drift, missing indexes, and whether queries time out.

Better:
> The script checks schema drift, missing indexes, and query timeouts.

## 9. Keep related words together

Put modifiers next to what they modify.

Weak:
> We only found two regressions in checkout.

Better:
> We found only two regressions in checkout.

Weak:
> The team discussed a rollout plan for enterprise customers on Friday.

Better:
> On Friday, the team discussed a rollout plan for enterprise customers.

## 10. Put emphasis where readers feel it

The end of a sentence carries weight. Put the important word, risk, or action there.

Weak:
> Because the migration deletes the old index, the rollback window matters most.

Better:
> The rollback window matters most because the migration deletes the old index.

## 11. Keep summaries disciplined

A summary should compress, not narrate every step. Use one tense. Remove repeated “the author says,” “the report states,” and “it also mentions” once attribution is clear.

## 12. Finish without fake finality

Do not add “In conclusion,” “Overall,” or a generic moral unless a real synthesis helps. End on the decision, next step, risk, or takeaway.
