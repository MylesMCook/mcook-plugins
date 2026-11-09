# II. Elementary Rules of Usage

Use this file for grammar, punctuation, and sentence mechanics. Do not over-edit casual text into stiffness.

## Possessives

- Singular nouns usually take `'s`: `the user’s request`, `James’s branch`.
- Plural nouns ending in `s` usually take only an apostrophe: `the users’ accounts`.
- Pronoun possessives do not take apostrophes: `its`, `hers`, `theirs`, `yours`.

## Commas

Use commas to help readers parse meaning, not to decorate sentences.

- Use the serial comma when a list has three or more items: `logs, metrics, and traces`.
- Use paired commas around parenthetical interruptions: `The deploy, if tests pass, starts at 3 PM.`
- Use a comma before a conjunction joining independent clauses: `The build passed, but the deploy failed.`
- Do not join two independent clauses with only a comma. Use a period, semicolon, or conjunction.

Weak:
> The build passed, the deploy failed.

Better:
> The build passed, but the deploy failed.

## Introductory phrases

Use a comma after a long or potentially confusing introductory phrase.

> After the migration finishes, run the smoke tests.

Short phrases often do not need one:

> In production the job runs hourly.

## Restrictive vs. nonrestrictive clauses

Use commas for extra information; omit them for identifying information.

- `Services that handle payments need extra monitoring.` = only those services.
- `The payments service, which handles invoices, needs extra monitoring.` = extra detail about a known service.

## Dangling modifiers

A phrase at the beginning of a sentence should point to the grammatical subject that follows.

Weak:
> After reading the logs, the bug became obvious.

Better:
> After reading the logs, we found the bug.

## Hyphens and dashes

- Use hyphens for compound modifiers when they prevent ambiguity: `user-facing copy`, `read-only token`.
- Use an em dash sparingly for a sharp break or emphasis.
- Do not use dashes as a substitute for structure when periods or commas would be clearer.

## Semicolons

Use semicolons to join closely related independent clauses or to separate complex list items.

> The API accepts JSON; the CLI accepts YAML.

Avoid semicolons in casual messages unless they clearly improve readability.

## Colons

Use a colon after a complete clause to introduce an explanation, list, or example.

> The fix has one risk: old clients may retry too aggressively.

## Quotation marks

Use quotation marks for exact text. Do not put ordinary emphasis in quotes unless you mean to signal distance or irony.

## Capitalization

Prefer sentence case for headings and UI text unless a style guide requires title case.

> Configure the integration<br>
> Not: Configure the Integration

## Contractions

Use contractions in conversational, Slack, email, and product text when they sound natural. Avoid them in formal policies, legal text, and strict technical specifications.
