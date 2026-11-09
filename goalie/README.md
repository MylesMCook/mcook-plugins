# Goalie

Goalie turns rough long-running work into paste-ready Codex Goal text. Its optional,
quiet Stop hook sends a brrr notification when a Goal is blocked or needs input.

## What It Does

- `$goalie` turns rough long-run work into paste-ready Goal text under 4000 characters.
- The bundled Stop hook first checks the transcript for actual Goal tool activity, then inspects the final Codex message for blocked Goal evidence.
- When attention is needed, it posts a brrr webhook payload with title, subtitle, thread grouping, sound, interruption level, app link, and Codex image.

The hook is intentionally quiet. Normal successful turns do not notify.
Notification taps open the ChatGPT app through `chatgpt://` by default.

## Cross-machine behavior

- The Goalie skill works anywhere Codex loads marketplace plugins.
- The notification hook uses standard-library Python: `python3` on macOS/Linux and
  `py -3` on Windows.
- Goal drafting never requires a webhook. Without `BRRR_WEBHOOK_URL`, the hook exits
  successfully without sending anything.

## Setup

1. Install this plugin from `Myles Codex Plugins` in Codex.
2. Enable `Goalie` for its notification hook.
3. Set the brrr webhook in the environment Codex inherits:

```sh
export BRRR_WEBHOOK_URL='<your brrr webhook URL from brrr.now>'
```

4. Restart Codex.
5. When Codex shows the plugin hook trust review, inspect and trust the command for
your platform:

```text
macOS/Linux: python3 "${PLUGIN_ROOT}/hooks/goalie_notify.py"
Windows:     py -3 "%PLUGIN_ROOT%\hooks\goalie_notify.py"
```

The webhook URL is read only from `BRRR_WEBHOOK_URL`. Do not commit it.

To use a different tap target or image, set:

```sh
export GOALIE_OPEN_URL='https://chatgpt.com/'
export GOALIE_IMAGE_URL='https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/light/codex-color.png'
```

Optional brrr tuning:

```sh
export GOALIE_SOUND='brrr'
export GOALIE_INTERRUPTION_LEVEL='time-sensitive'
export GOALIE_FILTER_CRITERIA='work'
export GOALIE_EXPIRATION_MINUTES='360'
```

## Migration from a home-scoped skill

This plugin now owns the Goalie skill. If a machine still has an older
`~/.agents/skills/goalie` copy, keep it until the marketplace plugin works in a
new task, then remove the older copy. Do not load both versions long-term.

## Hook Behavior

The hook runs on Codex `Stop`. Codex does not currently expose a dedicated Goal-status hook, and `Stop` matchers cannot filter by Goal state, so the script does the Goal gating itself.

It sends a notification only when one of these is true:

- transcript evidence of `update_goal` with `status: "blocked"`
- transcript evidence of Goal tool activity plus final assistant text with a manual checkpoint
- transcript evidence of Goal tool activity plus final assistant text saying Codex needs input or cannot proceed
- transcript evidence of Goal tool activity plus final assistant text naming a remaining blocker
- final assistant text explicitly saying the Goal is blocked

Ordinary chats that happen to say "manual checkpoint", "blocked", or "needs input" do not notify.

If `BRRR_WEBHOOK_URL` is missing, invalid, or brrr is unreachable, the hook exits successfully and writes a short diagnostic to stderr. It should never block the Codex turn.

## Validation

```sh
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py goalie
python3 -m unittest discover -s goalie/tests
```
