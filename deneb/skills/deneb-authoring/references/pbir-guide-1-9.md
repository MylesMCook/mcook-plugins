# Deneb PBIR Guide 1.9

Purpose: Stable, version-pinned PBIR guidance for creating or editing Deneb visuals in report JSON.

## Stable rules

- For stable guidance, use the Deneb 1.9 PBIR docs instead of canary guidance.
- The AppSource Deneb visual type GUID is `deneb7E15AEF80B9E4D4F8E12924291ECE89A`.
- Persist the spec in `visual.objects.vega[0].properties.jsonSpec` as a stringified JSON or JSONC string.
- Persist config in `visual.objects.vega[0].properties.jsonConfig`, usually as `"'{}'"` for a minimal config.
- Use Power BI literal conventions correctly: text wrapped in single quotes, integers with `D`, booleans as literals.
- Treat `visual.query.queryState.dataset` as the source of Values-well field mapping for Deneb.

## Common failure modes

- Using the wrong visual GUID for the edition being targeted.
- Double-escaping or malformed stringification of `jsonSpec`.
- Forgetting Power BI literal rules for text, booleans, or integer values.
- Assuming Deneb-managed state objects must be hand-authored when they are internal.
- Writing PBIR against model field names without considering display names and sanitization in the resulting dataset.

## Safe defaults

- Start from the minimal Deneb visual definition, then add dataset projections and the smallest working spec.
- Keep `jsonConfig` empty unless there is a clear need for configuration.
- Let Deneb manage internal state-management properties where possible.
- Validate the spec in the editor before industrializing PBIR generation logic.

## Version caveats

- This file is intentionally pinned to stable Deneb 1.9 PBIR guidance.
- Earlier Deneb lines may need more manual stepping through the create/import dialog for new visuals.

## Source URLs

- https://deneb.guide/docs/pbir-guide

## Verified version/date

- Deneb PBIR guide version 1.9 checked 2026-03-26.
