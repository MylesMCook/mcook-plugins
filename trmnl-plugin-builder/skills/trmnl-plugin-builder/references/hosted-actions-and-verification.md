# Hosted-action gates and verification

## Approval gate

Drafting local files and synthetic fixtures is safe to do by default. Ask for
explicit approval before each class of hosted action, naming the exact target
and expected effect.

| Action | Rule |
| --- | --- |
| Edit or save hosted markup, settings, fields, strategy, or Plugin Merge wiring | Approval required. |
| Import a Private Plugin archive or call a hosted write API | Approval required. |
| POST a webhook | Approval required; it changes hosted merge data. |
| Force Refresh, a hosted render, screenshot, or preview capture | Approval required. |
| Publish, unlist, update, deploy, or run a remote CLI push | Approval required. |
| Enable Debug Logs | Approval required; keep sensitive values out of logs. |
| Query a display endpoint that advances a Playlist | Treat as side-effecting; approval required. |
| Physical-device check | Approval required; state the device and expected change. |

Do not treat a user asking for implementation as blanket approval for any of
these actions. If approval names only one action, do only that action.

## What each check proves

| Check | Can establish | Cannot establish |
| --- | --- | --- |
| Synthetic local render | The local fixture maps to the drafted Liquid and the layout is plausible. | Hosted variables, hosted refresh, Plugin Merge data, screenshot output, or device behavior. |
| Approved hosted preview/render | The current hosted plugin can render the checked data path. | Physical-device wake/render behavior or a different user's data contract. |
| Approved refresh or webhook post | The checked hosted update path accepted the submitted data. | Long-term polling behavior, quota headroom, or device rendering. |
| Approved physical-device check | The named device rendered during the observed cycle. | Other devices, future refreshes, or untested screen states. |

Report the narrowest true claim. Say which data was synthetic, which was
hosted, and what remains unverified. Never use an offline preview to claim that
hosted merge variables or a physical TRMNL device work.

## Safe closeout checklist

- Current official skill/docs and Framework version recorded; any Context7
  cross-check is identified as secondary evidence.
- No secrets in artifacts, preview data, logs, or response text.
- The exact hosted operation was approved before it happened.
- The verification claim matches the evidence obtained.
- Publication previews use sanitized data; a Recipe's latest screen can become
  its visible preview.
