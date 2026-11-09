# Composition Patterns

Load this when choosing a plate structure or inventing the physical metaphor.
Pick one dominant pattern. Mixing patterns makes the image feel like a slide.

## Contents

- System portrait patterns
- Editorial patterns
- Original metaphor method

## System portrait patterns

### Plumbing cutaway

Use for a service made of a front door, running parts, stores, supervision, and
external utilities.

Draw a workshop, utility room, building section, or machine cutaway. Let the
orange primary path move through 3-6 mechanisms. Put durable state in a drawer,
reservoir, archive, or locked cabinet. Inkblot operates the decisive junction.

### Backstage counter

Use for user-facing services, agent work, and human-in-the-loop operations.

Put the user-visible action above or in front of a counter, curtain, wall, or
floor. Put hidden services and support work behind or below it. Inkblot carries
the request across the visibility boundary.

### Parcel route

Use for one request, event, file, message, or data transformation.

Follow one orange parcel, receipt, ticket, or tube through a few handoffs. Show
its state changing physically. Use a small waiting shelf for queues and a
drawer for persistence. Do not add every steady-state component.

### Relay bench

Use for agents, tool calls, approvals, retries, and orchestrated work.

Draw a workbench with a baton, spool, switchboard, or stack of task cards.
Inkblot performs the important handoff, chooses a tool, or checks returned work.
Show control and payload as different physical objects when the distinction
matters.

### Habitat portrait

Use for deployment, runtime, supervision, private networking, and persistence.

Draw nested places: a room on a host, a machine in a runtime, a locked cabinet
for state, and a door or utility line for the network boundary. Keep business
logic secondary. Inkblot watches the health bell or tends the runtime.

### Repair scene

Use for one failure, detection signal, fallback, restart, restore, or rollback.

Draw the broken part in red, the detection signal, and the safe recovery action.
Inkblot patches, swaps, restarts, or restores. Preserve the durable state and
show what remains available during repair.

### Trust checkpoint

Use for authentication, authorization, secret access, public/private
boundaries, or approval gates.

Draw one guarded hatch, pass window, key cabinet, or sealed package. Inkblot
checks or passes a credential without displaying its value. Show the boundary
and allowed action, not a generic padlock cloud.

### Feedback garden

Use for reinforcing/balancing loops, learning systems, monitoring, and gradual
improvement.

Draw a loop as a physical cycle: water wheel, garden return line, repair cart,
or receipt trail. Show delay as a waiting object and mark friction in red. Use
only when feedback, rather than sequence, changes behavior.

### Context neighborhood

Use for who the system serves and which direct external systems matter.

Draw the system as one workplace in a sparse neighborhood. Use doors, paths,
utility lines, or deliveries for direct relationships. Keep internals hidden;
they belong in the plumbing cutaway.

## Editorial patterns

### Inkblot alone

Use by default for a general Inkblot, editorial, or concept request. Draw one
Inkblot performing one legible action with no more than two essential props.
Keep every prop smaller and visually subordinate to Inkblot. Leave the rest
white. Never use an oversized prop. Add no labels unless the idea genuinely
needs words.

### Workflow machine

Use for input, transformation, and output. Draw a low-tech machine with Inkblot
operating the decisive stage.

### Before/after contrast

Use for chaos/order, manual/automated, scattered/collected, or stuck/running.
Keep both sides simple and use one orange transition.

### Character state

Use for pain, uncertainty, overload, or an awkward handoff. Draw 2-4 small
states and make Inkblot carry the state physically.

### Concept metaphor

Use for trust, quality, tradeoffs, evidence, prioritization, or alignment. Pick
one memorable low-tech object and one visible result.

### Method stack

Use for layers or capability ladders. Draw shelves, bins, workbench levels, or
stacked drawers; avoid formal pyramids.

### Curving route

Use for a journey or learning path. Draw one path with a few stations while
Inkblot pulls, repairs, or walks the route.

### Tiny comic

Use for before/during/after or repeated attempts. Keep 2-4 panels, each with
one action. Never turn it into a full comic page.

## Original metaphor method

1. State the technical truth without visual language.
2. Extract its important semantic: direction, transformation, waiting, state,
   ownership, boundary, failure, recovery, or feedback.
3. Choose one physical action: route, sort, hold, queue, guard, patch, restore,
   filter, weigh, relay, untangle, or restart.
4. Choose one or two low-tech objects that preserve that semantic.
5. Make Inkblot perform the action.
6. Check that the scene would be misleading if the direction or object changed.

Do not copy old example compositions. Reuse the visual DNA, not a conveyor,
bridge, funnel, or machine merely because it worked before.
