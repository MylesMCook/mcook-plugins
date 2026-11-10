# Writing an Explainer topic

An Explainer topic teaches how a system works by **playing back the messages its parts send each other**. The player shows:

- an **intro** page: a big question, a one-paragraph answer, five key terms, and a diagram that plays itself;
- a **lesson list** (left), grouped, each lesson split into numbered **steps**;
- a **diagram** (centre) of the parts ("actors") as small isometric illustrations inside labelled **zones**, with each message flying from sender to receiver; it can switch to a **sequence** view;
- a **message log** (bottom) with Play / Step / Reset;
- a **message inspector** (right): for the selected message, what it does, why it's sent, its body with field notes, and a link to the message that answers it (or that it answers). The lesson summary, facts and links sit above it under "About this lesson", collapsed.

One topic is one JSON file. `node build.mjs topic.json` turns it into one self-contained page (`topic.html`) that works opened from disk. For a site, put files in `topics/` and run `node build.mjs`: the topic with `"home": true` becomes `dist/index.html`, every other topic `dist/<id>/index.html`.

## Workflow for an agent

1. Gather the facts (see Accuracy).
2. Pick 3 to 6 actors (the parts that talk) and 4 to 14 lessons in learning order. The first lesson shows the whole loop in 4 to 6 steps.
3. Pick a preset (below) and copy its example: `topics/dns.json` for a system or protocol, `topics/incident.json` for something that broke and was fixed, `topics/mcp.json` for a large topic with versions.
4. Run `node build.mjs --check <file>.json`. Each problem names its place, for example `lessons.auth.steps[2].msgs[0]: from "srv" is not an actor in this lesson`. Fix until it prints `ok`.
5. Run `node build.mjs <file>.json` and open the `.html` it writes.

## Writing

Direct text, no blobs. The reader should get each point in one glance.

- **Lead with the point.** First words say what happens. No setup ("In this lesson…"), no recap.
- **Short sentences.** 20 words at most; most well under. One idea each.
- **Bullets over paragraphs.** Give a lesson `summary` as 2 to 4 short points when it holds more than one idea. A single sentence is fine for one idea.
- **Structure over prose.** Definitions and numbers go in `facts`, not sentences. Caveats go in a risk callout or `aside`, not the summary.
- **One idea per step.** Title: one or two words ("Connect", "Ask", "Refuse"). Desc: one short sentence, two at most.
- **Plain words.** Define a term the first time it appears, or put it in `facts`. "Use", not "utilize".
- **Say it once.** Cut any sentence that restates another. No filler ("in order to", "it is important to note") or hype ("seamless", "robust").
- **Messages are concrete things that travel** between two actors. `info` is a short label. `json` is a small, realistic body. `notes` explain the one or two fields that matter.
- **Every message explains itself.** The inspector is where readers learn, so each message needs `what` and `why` (see below).

### Writing `what`, `why` and `notes`

The reader clicks a message and asks two things: what is this, and why is it here? Answer both in plain words, as the writer skill would.

- **`what`: the action, one sentence, verb first.** Name who it acts on and the concrete thing it carries. "Asks the server to open /outbound so its files can be listed." Not "This message is the OPENDIR request." Don't repeat `info` or the method name.
- **`why`: the reason, one or two short sentences.** Say what job it does in the flow, or what would break without it. "SFTP can't list a folder in one call. The client opens it, reads entries in batches, then closes it." Don't restate `what`.
- **`notes`: only the fields a newcomer wouldn't guess.** Each note says what the value means here, not what the field is called. `["id", "Request number. The reply carries the same id so the client can match it."]`. Skip fields whose name says it all.
- **Say what you know.** If the reason is inferred, say so ("Likely…") or attach a `guess` risk. Example values stay illustrative; say so in `footer`.
- **Answers link themselves.** The inspector links a request to its answer (matching `json.id` when both have one), so `what` doesn't need "the server replies with…".
- **Lay actors out like the real system.** The canvas is 1000 × 560; keep x within 60 to 940 and y within 60 to 520. Put things that run together in one zone. Leave about 300 px between actors in a row and 260 px between rows. Phones rotate the layout automatically.
- Use your own words. Don't copy long passages from other sites.

**Editing pass, before building:** reread every lead, summary, step, aside, callout and message `what`/`why` as a busy reader. Cut words that don't change the meaning; turn any paragraph with two or more ideas into bullets. If a `writer` skill is available, use it for this pass. Never change facts, numbers or names while editing.

The checker enforces the limits that keep pages readable:

| Field | Limit |
|---|---|
| any sentence | 20 words |
| `intro.lead` | 180 characters |
| `intro.facts` | 5 terms; each value 80 characters |
| lesson `facts` | each value 80 characters |
| lesson `summary` | 160 characters, or 2 to 4 bullets of 90 |
| step `title` | 3 words |
| step `desc` | 120 characters |
| `aside` text, risk text | 140 characters |
| message `info` | 40 characters |
| message `what` | required; 120 characters; not the same as `info` |
| message `why` | required; 160 characters; not the same as `what` |
| message `notes` | each value 100 characters |
| actors in one lesson | at least 150 px apart |

It also rejects common filler and hype words in all of these.

## Accuracy

Readers trust the page, so it says only what you know.

- **Read the sources first.** For a real system or event: the user's files, session transcripts, logs, docs or code. Don't fill gaps from memory.
- **Keep real numbers exact.** Counts, versions, dates, names and error text come straight from the source. If you simplify one, say so in `footer`.
- **Mark guesses.** When part of the story is inferred, add a risk such as `"guess": { "title": "Best explanation, not observed", "text": "…" }` and attach it to the message it affects. Set `riskLabel` to "Caveat" or "Still true" when the callouts aren't attacks.
- **Label made-up values.** Example `json` bodies are fine; say "values are illustrative" in `footer`.
- **Say what wasn't checked**, in a "What's still open" lesson or an `aside`.
- **No secrets.** Leave out tokens, passwords, internal IDs and URLs the reader doesn't need.

## Explaining something that happened

For an incident, a bug, or a change someone made, this order works:

1. **Overview** (intro lesson): the failure in one loop, from trigger to visible symptom.
2. **How it normally works**: the healthy path, so the failure has something to contrast with.
3. **The cause**, then **why now**: what was wrong, and what changed to expose it.
4. **The proof**: how the cause was confirmed, including attempts that failed.
5. **The fix**: what was changed, in order, with before/after numbers.
6. **Is anything else affected?** and **What's still open**.

Include the people or tools that did the work (for example an investigator as a `person` or `laptop` actor). Use `facts` for version numbers, counts and dates so the reader can check them.

## Presets

A preset fixes the words a kind of explainer uses, so every explainer of that kind reads the same. Set `"preset"` and leave `kinds`, `labels`, `riskLabel` and `groups` out unless you need to change one; your values win over the preset's.

| Preset | Use for | Message kinds become | Log heading | Callouts | Lesson groups |
|---|---|---|---|---|---|
| `protocol` | systems, protocols, APIs | Request, Response, Error, Notice, Network, Internal | Message flow | Attack surface | yours |
| `incident` | something that broke and was fixed | Request, Result, Failure, Notice, Storage, Inside | What happened, in order | Caveat | What happened · Proving and fixing it · After the fix (ids `cause`, `fix`, `after`) |
| `process` | business or everyday processes | Ask, Reply, Problem, Notice, Hand-off, Inside | What happens, in order | Watch out | yours |

## Template rules

The look is fixed by the kit, not the topic: icons, buttons, fonts, colours and layout come from `src/`. A topic can only choose from these:

- **Icons:** the 11 listed under Icons below.
- **Message kinds:** the 6 listed under Message kinds below.
- **Zone styles:** `solid` (default), `dashed`, `accent`.
- **Fields:** only those in `topic.schema.json`. The checker reports any other field by name, so typos don't vanish silently. Add `"$schema": "<kit folder>/topic.schema.json"` at the top of a topic for autocomplete in editors.

Every built page records the kit version that made it (`<meta name="generator">`).

## Spatial stability

Nothing the reader clicks moves, and nothing moves because something else changed. The player guarantees its part: Play, Step, Reset, the view and Before/After toggles, theme buttons and lessons stay exactly where they are through every state change, and the diagram never shifts while stepping (the lesson list always shows every step, and the caption reserves room for its longest step). The topic's part:

- **An actor shared by a lesson's variants or versions stays at the same x and y in each.** The checker enforces this, so toggling Before/After only changes what differs.
- **Keep a recurring actor in roughly the same place across lessons** when the layout allows it (callers left, services right). Readers build a map; don't redraw it without a reason.
- **Keep step descriptions similar in length within a lesson.** The caption reserves the longest one, so a single long step leaves extra space under the short ones.

## File format

```jsonc
{
  "id": "dns",                       // lowercase, used in the page address
  "preset": "protocol",              // optional: protocol, incident or process (see Presets)
  "home": false,                     // only for sites: exactly one topic in topics/ is true
  "title": "DNS Explained",          // header title
  "byline": "Your team",             // optional "by …" in the header
  "pageTitle": "DNS Explained · how names become addresses",
  "description": "One-line description for search engines",
  "subject": "Domain Name System",   // heading above the lesson list

  "intro": {
    "lesson": "overview",            // lesson played on the intro page (not listed on the left)
    "kicker": "Domain Name System",
    "heading": "What is DNS?",
    "lead": "One or two short sentences, 180 characters max.",
    "facts": [["Resolver", "the server that does the looking up"], ["…", "…"]],   // 3 to 5
    "start": "queries",              // lesson the big button opens
    "startLabel": "Start the lessons",
    "jump": [["Caching", "#caching"], ["Break it", "#spoofing"]]   // links to lessons: "#<lesson id>"
  },

  "groups": [                        // lesson groups, in order
    { "id": "basics", "title": "Basics" },
    { "id": "attacks", "title": "Break it", "separate": true }   // separate = divider line above
  ],

  "actors": {                        // the catalogue; lessons place them
    "browser":  { "label": "Browser",  "sub": "asks for a name", "icon": "browser" },
    "resolver": { "label": "Resolver", "sub": "your ISP",        "icon": "server" },
    "root":     { "label": "Root server", "sub": ".",            "icon": "tile", "mono": "." }
  },

  "kinds": { "req": "Query", "res": "Answer" },   // optional: rename message kinds in the inspector
  "labels": { "flow": "Message flow", "message": "Message", "method": "Action", "info": "Info" },  // optional: rename the log and inspector headings
  "risks": {                                       // optional warning callouts
    "spoof": { "title": "Cache poisoning", "text": "Two sentences on the attack.", "lesson": "spoofing" }
  },
  "riskLabel": "Attack surface",                   // optional label for those callouts
  "versions": {                                    // optional timeline; omit if the topic has no versions
    "label": "Spec version", "prefix": "Spec ", "current": "2025",
    "list": [{ "id": "2019", "short": "2019" }, { "id": "2025", "short": "2025" }]
  },
  "whatsNextTitle": "What's next",
  "whatsNext": [["RFC 1034", "The original design", "https://…"]],   // web links open in a new tab; "#lesson" or relative links ("../") stay
  "footer": "Short footer line.",

  "lessons": [
    {
      "id": "overview",
      "code": "What is DNS?",        // short title (list, overview heading)
      "name": "One lookup, start to finish",   // one-line subtitle
      "group": "basics",             // not needed for the intro lesson
      "summary": ["2 to 4 short points", "or one short sentence as a string"],
      "facts": [["Port", "53"], ["Transport", "UDP, TCP for big answers"]],
      "links": [["RFC 1035", "https://…"]], "linksLabel": "Read more",
      "aside": { "tag": "Not in the standard", "text": "Optional side note." },
      "boxes": [{ "title": "What changes next", "items": ["…"], "link": ["Changelog", "https://…"] }],

      "actors": [                    // which catalogue actors appear, and where
        { "id": "browser",  "x": 175, "y": 420 },
        { "id": "resolver", "x": 500, "y": 420, "sub": "override the subtitle here" },
        { "id": "root",     "x": 830, "y": 140 }
      ],
      "zones": [                     // labelled boxes around actors; style: solid (default), dashed, accent
        { "label": "Your network", "sub": "home", "ids": ["browser", "resolver"] },
        { "label": "Internet", "ids": ["root"], "style": "dashed" }
      ],
      "wires": { "browser|resolver": "UDP 53" },   // optional pill label on a connection

      "steps": [
        { "title": "Ask", "desc": "The browser asks the resolver for an address.", "msgs": [
          { "from": "browser", "to": "resolver", "kind": "req", "info": "example.com?",
            "what": "Asks the resolver for the IPv4 address of example.com.",   // required: the action, verb first
            "why": "The browser can't connect to a name, only to an address.",  // required: the reason it's sent
            "method": "A query",                    // optional; otherwise taken from json.method etc.
            "json": { "question": { "name": "example.com", "type": "A" } },
            "notes": [["type A", "Asks for an IPv4 address."]],
            "risk": "spoof" }                        // optional, a key from "risks"
        ] }
      ],

      "variants": [ { "id": "cached", "label": "Cached", "hint": "…", "steps": [ … ] } ],  // optional toggle; each variant replaces steps (and may replace actors/zones)
      "since": "2019",                              // optional: lesson greyed out before this version
      "atVersion": { "2019": { "diff": ["What was different"], "steps": [ … ] } }   // optional per-version override
    }
  ]
}
```

### Message kinds

Every message goes between two different actors. For work done inside one part (a check, a calculation), send a `host` message to the part it affects, or say it in the step's `desc`.

Default names in the inspector: Request, Response, Error, Notice, Network, Internal (rename them with `kinds`).

| kind | drawn as | use for |
|------|----------|---------|
| `req`  | solid dot | a request that expects an answer |
| `res`  | hollow dot | the answer |
| `err`  | amber dot | an error answer |
| `note` | dashed dot | a one-way notice, no answer |
| `http` | grey square | the transport or network layer underneath |
| `host` | dotted, dotted line | something inside one program, not on the wire |

The **Method** column shows `method` if you set it, else `json.method`, else `result` / `error` for answers, the first word of `json.request` or `json.status` for `http`, and `json.type` or `json.host` for `host`.

### Icons

`server`, `tile` (two slabs with a short `mono` label on top, good for named services), `laptop`, `chip` (a model or processor), `person`, `browser`, `vault` (keys, auth), `database`, `gateway` (a hub or proxy), `code` (a sandbox or script), `phone`.
