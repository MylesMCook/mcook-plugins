# API and Interface Design

Load this when the task is mainly about functions, classes, module boundaries, public APIs, parameter shape, or interface ergonomics.

Extended guidance for designing interfaces that stay simple for callers while hiding real work inside the implementation.

## The Depth Test

Before finalizing an interface, draw a line between the interface and the implementation. If the implementation side is substantially more complex than the interface side, the module is deep and likely earning its place. If both sides are roughly equal, the module is shallow and may not be hiding enough to justify its existence.

Deep interfaces absorb complexity. Shallow interfaces redistribute it.

## Parameter Budget

Every parameter is surface area. Start with the smallest set of inputs needed for the common case.

Prefer:

- required parameters only when they are truly required
- good defaults over tuning knobs
- named options when they make calls clearer
- separate advanced configuration only when the common path stays small

Do not let an options object become a grab bag of hidden modes. If the option set grows without a clear center, the API is trying to do too much.

## Layered APIs

When a domain has both simple and complex use cases, provide layered access rather than one flat interface that exposes everything at once.

- **Layer 1:** the common case, dead simple
- **Layer 2:** additional control for callers that genuinely need it
- **Layer 3:** rare escape hatches for unusual requirements

The common path should feel obvious. The advanced path can be more verbose as long as it stays out of the way for everyone else.

Example — bad (one flat interface for everything):

```python
def send_email(
    to,
    subject,
    body,
    cc=None,
    bcc=None,
    reply_to=None,
    headers=None,
    attachments=None,
    encoding="utf-8",
    smtp_server=None,
    port=None,
    use_tls=True,
    timeout=30,
    retry_count=3,
    retry_delay=1.0,
    tracking_id=None,
    template_engine=None,
):
    ...
```

Example — better (layered):

```python
def send_email(to, subject, body, *, cc=None, bcc=None, attachments=None):
    """Common case stays simple; advanced callers opt in."""
    ...

class EmailMessage:
    """Escape hatch for unusual delivery requirements."""

    def add_header(self, name, value):
        ...

    def set_transport(self, transport):
        ...

    def send(self):
        ...
```

## Boolean Flags Usually Hide Multiple APIs

A boolean flag that materially changes behavior often means the interface is trying to serve two different operations through one doorway.

Prefer separate functions, methods, or named policies when the flag changes semantics rather than just a small option.

Bad:

```ts
save(user, true)
```

Better:

```ts
saveDraft(user)
publish(user)
```

## Define Errors Out of Existence

The best API makes classes of errors structurally hard to produce rather than merely documenting how to recover from them.

If a resource must be opened and closed, prefer a pattern that makes cleanup structural:

```python
with open_resource() as resource:
    process(resource)
```

If an empty collection is a valid input, often return an empty result instead of throwing. If a parameter can be invalid, consider whether a narrower type, enum, constrained wrapper, assertion, or validation layer would make misuse harder.

Be cautious with unsigned numeric types. In many languages they create surprising behavior or awkward conversions. Use them when the language and domain genuinely benefit, not just to assert non-negativity.

## Information Hiding Checklist

When designing a module boundary, check that the following stay hidden unless callers truly need them:

- data representation
- algorithm choice
- caching, retry, or fallback policy
- external dependency details
- most recovery mechanics for internal failures

If callers must understand these details to use the interface safely, the interface is leaking.

## Pass-Through Methods Are a Smell

If a method only forwards arguments to another method with nearly the same signature, it is a pass-through. Pass-through methods add indirection without adding abstraction.

When you find one, either:

- remove it
- give it real responsibility
- merge the two layers

The same rule applies to thin wrappers and decorators. A wrapper earns its existence when it changes the abstraction, not when it republishes the same surface area.

## General-Purpose Interfaces Are Often Deeper

A slightly more general interface is often simpler than a pile of narrow special cases. The test is not elegance. The test is whether total surface area drops without making common tasks awkward.

Example: one `delete(start, end)` operation can often replace several narrow deletion functions while still keeping the common case obvious.

If the general interface requires a lot of setup for everyday use, it is too general.

## Consistency Within, Variation Between

Within a module, be aggressively consistent: similar names, parameter ordering, error handling, and data shapes.

Between modules, allow variation when the domains differ. Forcing unrelated concepts into the same abstraction shape often produces awkward APIs that fit none of them well.

## The Newspaper Test

A good interface reads like a headline. A caller should usually understand what a function does from its name and signature alone.

If the name needs a paragraph to explain the basics, it is probably wrong. If the parameters need a paragraph, there are probably too many or they are at the wrong level of abstraction.
