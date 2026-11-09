# IV. A Few Matters of Form

Use this file when formatting choices affect readability.

## Headings

Use headings to show the reader where they are. Prefer sentence case.

Good:
```markdown
## How retries work
```

Avoid stacked headings with no substance underneath.

## Bullets

Use bullets when the items are parallel and scannable. Do not turn every answer into bullets.

Good bullets:
- start with the same part of speech
- keep roughly similar length
- avoid nested lists unless the hierarchy matters

If a bullet needs more than two sentences, consider a paragraph.

## Numbered steps

Use numbers for ordered instructions. Each step should start with a verb.

1. Install dependencies.
2. Run the migration.
3. Verify the output.

## Tables

Use tables for comparison, not decoration. Keep columns few and labels short.

Good table columns:
- Option
- Best for
- Tradeoff

## Code and commands

Use code formatting for exact commands, file paths, identifiers, variables, and literal strings.

- `npm test`
- `src/api/users.ts`
- `DATABASE_URL`

Do not code-format ordinary emphasis.

## Quotes

Use block quotes only when preserving exact wording matters. For edits, put the original in a quote only if comparison helps.

## Links and citations

Make the surrounding sentence carry meaning. Do not write “click here.” In sourced work, attach citations to the claim they support.

## Screenshots and images

When describing visuals, explain what the reader should notice. Do not say “see image below” without context.

## Length

Short is not automatically clear. Use the length the reader needs:
- UI text: shortest useful action
- Slack: one screen when possible
- email: ask first, context second
- docs: complete enough to unblock the task
