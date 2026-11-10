---
name: explainer
description: Turn "how does X work?" into an interactive, step-by-step explainer page. Use when a user asks how a system, protocol, process, workflow or incident works, wants it shown visually, or wants a walkthrough of what passes between parts (apps, servers, people, services, organisations). Produces one self-contained HTML file with an animated diagram, lessons, playable steps and a message inspector that says what each message does and why.
---

# Explainer

You write one topic file (JSON). The kit checks it and builds one HTML page that plays the explanation step by step. Needs Node 18+.

If the `explainer_*` tools are available, use them instead of the commands below: `explainer_guide`, then `explainer_check` until ok, then `explainer_build`. Pass `topicPath` instead of `topic` when the topic is already a file, to avoid resending it.

**Showing a page:** `explainer_build` and `explainer_open` return `viewUrl`, a link served by a shared local viewer that is already running. Open it for the user right away (in Claude Code desktop: the browser pane). Never start your own server for explainers; the viewer starts on demand, is shared by every page and session, and stops by itself after 30 idle minutes or when the session ends. Without the tools, open the `.html` file directly.

## Changing an existing explainer

Use `explainer_list` to find it, `explainer_open` to show it, and `explainer_get` to read its topic (without the tools: read `~/Explainers/<name>.json`). Edit only what the user asked for, check, and build again. Rebuilding keeps the previous version in `~/Explainers/.history/`.

## Steps

1. Read `TOPIC-GUIDE.md` in this folder. Pick a preset and copy its example: `topics/dns.json` (system or protocol), `topics/incident.json` (something that broke and was fixed) or `topics/mcp.json` (large, with versions).
2. Gather the facts. For a real system or event, read the user's files, sessions, docs or code first. Never invent specifics.
3. Plan: 3 to 6 actors, 4 to 14 lessons in learning order (the first shows the whole loop), 2 to 5 steps per lesson, 1 to 4 messages per step.
4. Write the topic to `~/Explainers/<id>.json` unless the user names a place. Keep it; it is how the page gets revised later.
5. Edit: reread every lead, summary, step, aside, callout and message `what`/`why` as a busy reader. Cut what doesn't change the meaning; turn multi-idea paragraphs into bullet summaries. Use the `writer` skill for this pass if it is available. Keep facts, numbers and names unchanged.
6. Check: `node <this folder>/build.mjs --check <file>.json`. Fix every problem it names, then check again until it prints `ok`.
7. Build: `node <this folder>/build.mjs <file>.json` writes `<file>.html` beside it. It opens straight from disk.
8. Open the page for the user: the `viewUrl` from `explainer_build`, or the `.html` file. Say which parts are illustrative or unverified.

For a site of many explainers, put topics in `topics/` (one with `"home": true`) and run `node build.mjs`; pages land in `dist/`.

## Good explainers

- Direct text, no blobs. Lead with the point; sentences of 20 words at most.
- Bullets over paragraphs: a summary with more than one idea is 2 to 4 short points. Definitions and numbers go in `facts`.
- Write for someone smart who is new to the subject. Plain words; define a term the first time it appears.
- One idea per step. Titles are one or two words. Descriptions are one short sentence, two at most.
- Messages are concrete things that travel: a request, a file, a payment, a signal. `info` stays under 40 characters.
- Every message explains itself: `what` (the action, one sentence, verb first) and `why` (the job it does, or what breaks without it). `notes` explain only the fields a newcomer wouldn't guess. The inspector shows these; without them it is just code.
- Cut filler, hype and repetition. If a sentence restates the one before it, delete it.
- Non-technical topics work too: rename `kinds` and `labels` with everyday words.
- Lay actors out like the real thing: callers left, services right, shared parts on top.
