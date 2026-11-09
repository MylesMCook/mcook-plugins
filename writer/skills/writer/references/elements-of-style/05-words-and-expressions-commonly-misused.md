# V. Words and Expressions Commonly Misused

Use this file for word-choice cleanup. These are defaults, not laws.

## Prefer direct replacements

| Instead of | Prefer |
|---|---|
| utilize | use |
| leverage | use, apply, build on |
| facilitate | help, enable, make possible |
| robust | reliable, fault-tolerant, well-tested, resilient — only if true |
| seamless | uninterrupted, automatic, no extra step — only if true |
| impactful | specific effect |
| key | main, important, required, or delete |
| various | name the types or delete |
| numerous | many, several, or the exact number |
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| aforementioned | earlier, previous, or name it |
| commence | start |
| terminate | end, stop, delete — depending on meaning |
| make use of | use |
| perform an analysis of | analyze |
| provide assistance | help |
| ensure | make sure, verify, require — only if it explains the mechanism |

## Watch vague nouns

Replace vague nouns with the real thing.

- `aspect`, `area`, `factor`, `element`, `component`, `capability`, `functionality`, `solution`, `experience`
- If the noun hides a verb, restore the verb: `implementation of validation` → `validate`.

## Watch weak verbs

Forms of `be`, `have`, `make`, `do`, `provide`, and `enable` are often fine, but they can hide action.

Weak:
> The release provides improvements to search.

Better:
> The release ranks exact matches first and adds typo tolerance.

## “Ensure”

`Ensure` often promises too much. Replace it with the real action.

Weak:
> Add retries to ensure uploads succeed.

Better:
> Add retries so transient network errors do not fail uploads immediately.

## “May” and “might”

Keep hedging when uncertainty matters. Cut it when the condition is known.

Weak:
> The API may return 401 when the token expires.

Better:
> The API returns 401 when the token expires.

Accurate:
> The API may return 429 during traffic spikes.

## “Interesting”

Do not announce that something is interesting. Show the fact that makes it interesting.

Weak:
> Interestingly, the cache expired at the same time.

Better:
> The cache expired at the same time as the deploy.

## “Easy,” “simple,” and “just”

Avoid words that minimize effort unless you know the reader’s context.

Weak:
> Just run the migration.

Better:
> Run the migration.

## “Obviously” and “clearly”

These can sound condescending and often add nothing.

Weak:
> Clearly, the endpoint needs authentication.

Better:
> The endpoint needs authentication.
