# Postel's Law

Source concept: https://lawsofux.com/postels-law/

## When to load

Load this reference when forms, search, validation, uploads, address/phone/date input, error handling, APIs exposed through UI, or flexible user entry.

## Lens

Interfaces should accept reasonable variation in user input while responding with clear, reliable output.

## Look for in the design

- strict input formats that reject understandable entries
- errors that blame the user rather than translating input
- outputs that are ambiguous, inconsistent, or overly loose

## Critique moves

- Accept common input variations and normalize them silently when meaning is clear.
- State constraints before submission and give precise corrective feedback.
- Keep the system's response consistent and conservative even when inputs vary.

## Watch-out

Do not accept ambiguous input if it could produce harmful or irreversible outcomes; ask for clarification there.

## Pairs well with

Mental Model, Jakob's Law, Tesler's Law
