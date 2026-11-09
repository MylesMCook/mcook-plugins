# Markup, Form Fields, and artifacts

## Liquid and Framework guardrails

1. Complete the [source-policy](source-policy.md) check first. Use the official
   `trmnl` skill and current Framework documentation for syntax and design.
2. Identify the rendering surface before writing anything:
   - **Private Plugin editor:** follow the current editor/template guidance.
     Do not copy public-plugin `view` wrappers into the editor.
   - **Third Party response:** verify the current required layout nodes and
     response contract from the official Third Party screen-generation docs.
3. Use only variables demonstrated by the current data contract or current
   hosted editor. Treat every default, loop, condition, and data path as a
   contract decision, not a visual guess.
4. Prefer the current Framework's documented classes over custom CSS, but do
   not invent class names from memory. Keep markup simple and e-ink appropriate.
5. Native-source markup may use a different templating language. Translate its
   data bindings deliberately; do not paste it into Liquid unchanged.

If the official support/docs sources show different interpolation syntax, check
the current editor and resolve the difference before proceeding. Never convert
an ambiguous example into a hosted change.

## Form Fields YAML

Use Form Fields only for non-sensitive preferences and identifiers. Do not emit
or recommend `password`, API-key, credential, webhook-URL, or remote-select
designs that transmit a secret.

For a direct Form Fields editor request, return a bare YAML list, not a wrapper:

```yaml
- keyname: display_label
  field_type: string
  name: Display label
  default: Example Metrics
```

Use a wrapper such as `custom_fields` only after verifying the current complete
import/export schema and only when the user explicitly needs an archive. Keep
the field list small and explain how each value changes the screen.

## Import/export artifacts

The current Private Plugin import format uses a flat ZIP with `settings.yml`
and optional viewport Liquid files. Re-check the live import/export guide before
creating or uploading an archive because the schema and supported fields can
change.

Build import archives from the current documented schema and a clean temporary
directory. Do not claim that this companion ships a starter archive or fixture
bundle. Uploading, importing, and saving remain approval-gated.
