# Comment decisions

These are synthetic editorial examples, not study results. The supplied
evidence is part of each example; never infer a rationale from a snippet alone.

## A constraint rather than narration

Given a documented provider requirement that request signatures use the
original bytes, this explains the order:

```ts
// Verify the original bytes; parsing and reserializing can change the signature.
verifySignature(rawBody, signature);
const event = JSON.parse(rawBody);
```

“Verify signature, then parse JSON” merely repeats the statements. If the
provider requirement is unavailable, describe only what can be verified or
flag the missing evidence; do not invent a security guarantee.

## A useful public contract

Given an implementation and tests that establish these exact rules:

```go
// Normalize returns a trimmed, lowercase key. It returns ErrEmpty when the
// trimmed key is empty. It does not modify the caller's input.
func Normalize(key string) (string, error)
```

This documents observable use, even though it says what the function does.
Do not add a claim about Unicode normalization, validation, or performance
unless that behavior is supported.

## No comment needed

```python
active_users = [user for user in users if user.active]
```

“Keep active users” adds little in ordinary private code. A documented domain
meaning of `active` may deserve explanation at its definition instead.

## Orient a human reviewing generated code

Given an invoice allocator whose specification requires exact proportional
rounding and invoice-order ties, a short introduction supplies a mental model:

```python
"""Allocate an invoice discount in integer currency units.

Floor each proportional share, then give leftover units to the lines with
the largest fractional shares. Invoice order breaks ties.
"""
```

A local explanation can then cover the arithmetic that is easy to misread:

```python
# Every fraction has the same denominator, so integer remainders rank the
# fractional shares exactly.
```

The introduction explains the approach; the local comment explains its valid
comparison. The API docs still need relevant input assumptions, errors, and
output rules. Do not repeat this overview above each loop or assignment.

## Repair a stale claim without changing code

An existing comment says “Retries every failure three times.” Current code
retries only HTTP 429 and 503 and makes at most three total attempts. Replace
the inaccurate sentence with those observed rules. Do not change the loop to
match the old prose or infer that all operations are safe to retry.

## An actionable TODO

Given an existing issue for upstream pagination support:

```python
# TODO(PROJ-42): Remove this cursor adapter when the client supports opaque cursors.
```

Use the actual existing issue and verified condition. Without one, a concrete
task and condition are still useful; do not invent a ticket to fill the pattern.

## Preserve tool-consumed text

```go
//go:build linux
```

This selects builds. It is not prose to rewrite into a sentence. Apply the same
care to suppression comments, license notices, doctest examples, and SQL hints.
