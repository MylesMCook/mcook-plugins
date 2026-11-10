# Changelog

## 1.6.0 - 2026-11-10

- The right panel explains each message: what it does and why it's sent, above its body and field notes.
- A request links to the message that answers it, and a response links back to its request.
- The lesson summary, facts and links move into a collapsed "About this lesson" section above the message.
- Every message now needs `what` and `why`; the checker reports any that are missing. Older topics must add them before they rebuild.
- The writing guide covers how to write `what`, `why` and field notes, and the checker catches more filler words.

## 1.5.3 - 2026-11-08

- Add an explicit Claude manifest for claude.ai marketplace synchronization.

## 1.5.2 - 2026-11-05

- Stronger viewer checks: sessions reuse only the owner's recorded port, the proof is bound to that port, the signing key never appears in links, and secrets are replaced whenever a viewer stops.

## 1.5.1 - 2026-11-05

- The viewer is private: links carry a token, requests without it are refused, and sessions reuse a running viewer only after it proves it holds the token.

## 1.5.0 - 2026-11-05

- Pages open without anyone starting a server: building or opening an explainer returns a local link from one shared viewer.
- The viewer is reused by every page and session, stops after 30 idle minutes and with its session, and serves only explainer pages to this machine.
- New tool `explainer_open` shows a saved explainer.

## 1.4.0 - 2026-11-05

- Direct text, no blobs: lesson summaries can be 2 to 4 bullet points, sentences are 20 words max, and leads, summaries, steps, asides, callouts and facts have tighter limits.
- Agents do an editing pass before building, using the writer skill when it is installed.

## 1.3.2 - 2026-11-05

- Phone playback bar: the Log button no longer spills into the next-lesson button on narrow phones.
- Command-line builds keep the replaced page in `.history`, like `explainer_build`.

## 1.3.1 - 2026-11-05

- Every scrolling panel reserves room for its scrollbar, so text no longer shifts when a panel starts to scroll.

## 1.3.0 - 2026-11-05

- Spatial stability: controls, lessons, toggles and the diagram never move when something changes, at desktop, laptop and phone sizes.
- The lesson list shows every step of every lesson; any step is clickable.
- At 1024 px, lessons with a Before/After toggle no longer collapse the diagram.
- The checker rejects an actor that moves between a lesson's variants or versions.

## 1.2.1 - 2026-11-05

- `topicPath` only reads topics inside the explainers folder; paths or symlinks leading out are refused.

## 1.2.0 - 2026-11-05

- New tools `explainer_list` and `explainer_get` to find and revise saved explainers.
- `explainer_check` and `explainer_build` accept `topicPath` (a saved `.json`) instead of the whole topic.
- Rebuilding keeps the replaced page and topic in `~/Explainers/.history/`; an identical rebuild changes nothing.
- Every tool has a "Use this when" description, a closed input schema checked at runtime, full annotations, an output schema and structured results.
- Lesson list: no double divider above a separated lesson group.

## 1.1.0 - 2026-11-05

- First marketplace release, from explainer-kit 1.1.0.
- Skill plus bundled stdio MCP server (`explainer_guide`, `explainer_check`, `explainer_build`).
- Checker enforces the topic schema, presets, length limits, actor spacing and plain wording.
- Built pages save their topic JSON beside them for later revision.
