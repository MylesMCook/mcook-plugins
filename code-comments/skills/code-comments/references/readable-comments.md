# Readable comments

A human reviewer needs the fact quickly, with enough context to check it.
Apply the editing principles below after establishing what the code does.
They are editorial guidance, not research findings or a readability score.

## Shape the explanation around the reader's question

Start with the approach, contract, or constraint. Add its reason when supported.
Keep related words together; name who acts and what changes. Define a domain
term once at the place readers first need it. Use the same term and identifier
afterward. A short paragraph can explain an algorithm; a local comment can
explain a boundary. Neither needs a preamble or closing summary.

Use ordinary language around necessary technical terms. Split a sentence when
it mixes independent ideas. Use prose for a relationship and a list for facts
that readers need to compare. Follow the repository's comment wrapping and doc
format; avoid decorative headings or emphasis in small local comments.

## Remove polish that hides the fact

Given code and tests proving byte-for-byte signature verification:

```ts
// Weak: It is important to note that this robust validation mechanism ensures
// seamless integrity of incoming payloads before subsequent processing.

// Better: Verify the original bytes before parsing the payload.
// Parsing and reserializing can change the bytes used for the signature.
```

The revision names the operation and constraint. It does not claim the whole
system is secure. If the second sentence lacks evidence, omit it or report
the uncertainty rather than filling the gap with confidence.

Given code and a specification using proportional invoice discounts:

```python
# Weak: Leverage deterministic allocation to facilitate equitable distribution.

# Better: Give leftover cents to the lines with the largest fractional shares.
# Break ties by invoice order.
```

“Equitable” implies a value judgment. The revision lets a reviewer check the
actual rounding and tie-breaking rules. Use “minor units” rather than “cents”
when the contract supports currencies with other unit sizes.

## Preserve the meaning during cleanup

A comment saying “Retries HTTP 429 and 503 at most twice after the first
attempt” must not become “Retries failed requests.” The shorter version loses
the status filter and limit. Likewise, preserve “may,” “only,” “unless,” units,
preconditions, error types, mutation, and cancellation details when meaningful.

Do not make the prose more persuasive than the evidence. Remove unsupported
assurances and unnecessary hedging separately; uncertainty that reflects a
real knowledge gap stays visible. When a confusing algorithm needs structural
work, concise prose alone does not make it reviewable.

## Provenance

Original synthesis of the relevant principles in this marketplace's
[Writer 0.2.0 workflow](https://github.com/MylesMCook/mcook-plugins/blob/f882229/writer/skills/writer/SKILL.md),
[cleanup guide](https://github.com/MylesMCook/mcook-plugins/blob/f882229/writer/skills/writer/references/signs-of-ai-writing.md),
[composition guide](https://github.com/MylesMCook/mcook-plugins/blob/f882229/writer/skills/writer/references/elements-of-style/03-elementary-principles-of-composition.md),
and [format playbook](https://github.com/MylesMCook/mcook-plugins/blob/f882229/writer/skills/writer/references/format-playbook.md),
inspected 2026-10-02. Examples above are newly authored. No Writer reference
text, legacy voice advice, or third-party examples are bundled. The adaptation
preserves technical precision and drops advice about personality that does not
fit source comments. No Writer installation or external lookup is needed.
