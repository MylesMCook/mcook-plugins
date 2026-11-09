# System Portrait Method

Load this when mapping a real software, service, agent, automation, homelab, or
operational system.

## Contents

- Start with a factual system brief
- Choose one abstraction level
- Separate visible and hidden work
- Keep a truth ledger
- Turn topology into a physical explanation
- Control complexity
- Pick a system set

## Start with a factual system brief

Inspect the smallest useful evidence set. Prefer source-of-truth artifacts over
prose summaries:

- entry points, routes, commands, and client-facing URLs
- manifests, service definitions, container or deployment config
- process supervision, health checks, and current status when available
- applications, workers, data stores, queues, files, and caches
- external providers, APIs, tools, connectors, or human handoffs
- credentials and trust boundaries without exposing secret values
- failure signals, retries, recovery paths, backups, and rollback

Do not equate a configured path with a currently healthy path. Record whether a
claim came from static configuration, runtime evidence, logs, documentation, or
inference.

Declare the portrait's evidence mode:

- **Runtime-grounded:** current runtime state or client-facing behavior was
  observed in addition to static source or configuration.
- **Configuration-grounded:** supplied or inspected source or configuration
  supports the topology, but current health was not observed.
- **Conceptual:** the user supplied an idea or desired behavior, not evidence of
  a real deployed topology.

Do not call a configuration-grounded portrait runtime-grounded. Do not call a
source-supported portrait conceptual merely because current health is unknown.

## Choose one abstraction level

Borrow the discipline of C4 without inheriting its visual appearance.

| Zoom | Question | Show | Usually omit |
|---|---|---|---|
| Landscape/context | Where does this system fit? | people, system boundary, direct external systems | internal modules, protocols |
| Plumbing/container | What running parts make it work? | apps, workers, stores, supervisors, direct relationships | code-level classes |
| Moment/dynamic | What happens for this one request or event? | ordered handoffs, state changes, retries | unrelated steady-state topology |
| Habitat/deployment | Where does it run and persist? | host, runtime, proxy, process supervisor, storage, network boundary | internal business logic |
| Failure/recovery | What breaks, how is it detected, and how does it recover? | one failure, signal, fallback, repair, durable state | the happy path unless needed |

Use only levels that add value. Start with the single plate that answers the
user's main question. Add another only when it answers a different question.

## Separate visible and hidden work

For service or human-in-the-loop systems, use a line of visibility:

1. User action or visible outcome.
2. Frontstage interface or response.
3. Backstage services, agents, and transformations.
4. Support processes, supervision, storage, and recovery.

Render this as a cutaway building, counter, stage, workshop, or floor section,
not as horizontal swim lanes.

## Keep a truth ledger

Use three confidence classes outside the image:

- **Verified:** directly observed in source, configuration, runtime state, log,
  or current authoritative documentation.
- **Inferred:** a likely relationship supported by multiple clues but not
  directly observed.
- **Unknown:** missing, contradictory, stale, or outside the inspected scope.

For every material connection, record:

```text
origin -> destination: action or payload; protocol/mechanism; evidence
```

Example:

```text
browser -> reverse proxy: sends HTTPS request; TCP 443; verified in proxy config
proxy -> app: forwards HTTP request; 127.0.0.1:8484; verified in proxy config
app -> backup job: relationship not observed; unknown
```

Never put secret values, private tokens, or unnecessary private hostnames in an
image prompt. Generalize sensitive labels while keeping exact private facts in
the user's local notes when appropriate.

## Turn topology into a physical explanation

Map technical semantics to physical behavior:

| System fact | Visual treatment |
|---|---|
| request or payload | parcel, note, receipt, tube, tray |
| synchronous call | handoff through a door, counter, or speaking tube |
| queue or delayed work | shelf, inbox, hopper, waiting cart |
| database or durable state | labeled drawer, reservoir, archive, ledger |
| cache | small ready shelf or warming tray |
| supervisor | night watch, bell board, restart crank |
| proxy or router | switchboard, mail slot, rail switch |
| trust boundary | checkpoint, locked hatch, guarded threshold |
| retry | returned parcel, second pull, looped ticket |
| backup and restore | spare drawer, sealed copy, repair kit |
| external dependency | neighboring building, utility line, rented machine |
| unknown link | covered hatch, broken-off blue cable, question tag |

The physical object is not decoration. It must preserve direction, ownership,
state, delay, or failure semantics from the brief.

## Control complexity

- Keep 3-6 named elements on one plate.
- Show one primary route. Move secondary routes to another plate or the truth
  ledger.
- Keep a store visible when persistence changes the system's meaning.
- Show a trust boundary or supervisor only when it matters to the question.
- Prefer an inset detail or second plate over shrinking everything.
- Keep labels beside their objects. Do not make the viewer chase a remote key.

## Pick a system set

Start with one of these and add another only when needed:

1. **Context portrait:** who approaches the system, what value comes out, and
   which external neighbors matter.
2. **Plumbing cutaway:** the few running parts, stateful stores, and decisive
   handoffs that make the value happen.
3. **Focus plate(s):** only the interesting request path, trust boundary,
   failure/recovery path, or feedback loop.

Do not create a component-level plate just because the source contains many
components. Detail is earned by a question.
