# Decisions and data routing

## Choose the smallest fitting TRMNL path

| Path | Choose it when | Do not choose it when |
| --- | --- | --- |
| Private Plugin | A personal/private screen can use polling, webhook data, or Plugin Merge. | The actual need is public OAuth, author-managed user data, or self-hosting. |
| Recipe | A proven Private Plugin should be shared through TRMNL and its sanitized preview is safe to expose. | The design needs an author-operated service or the preview could reveal private data. |
| Third Party | A public, server-backed integration genuinely needs OAuth, author-managed user data/settings, or a custom management UI. | A Private Plugin or Recipe meets the requirement without new service ownership. |
| BYOS | The goal is to own the server/device relationship or run a compatible self-hosted stack. | The goal is merely to add a hosted TRMNL screen. |

Recipes are a sharing/publication path for the Private Plugin model, not a
second implementation stack. Publishing or updating one is a hosted action and
requires explicit approval.

## Pick a private data strategy

### Polling

Use polling when TRMNL can retrieve a suitable data source on the user's
behalf. Confirm the currently supported formats, URL interpolation, refresh
cadence, and single-versus-multiple-source variable shape from official docs
and the current editor before writing Liquid.

Use a public or already-approved data path. Do not add a secret field, header,
or generated configuration merely to make polling work. If the upstream needs a
credential, use a pre-existing approved secret-handling service or reconsider
the architecture; do not create a broker just for this skill.

### Webhook

Use a webhook when an external system naturally pushes screen data or stateful
updates are a better fit than polling. Verify current payload and rate limits
before committing to the design. The expected payload centers on
`merge_variables`; use the documented merge strategy only after checking the
current API page.

The per-plugin webhook URL and its identifier are sensitive configuration. Do
not put either in fields, fixtures, docs, examples, output, or source control.
A webhook POST changes hosted state and requires explicit approval.

### Plugin Merge

Use Plugin Merge when the screen should render data from another installed
TRMNL plugin. The source plugin must be connected and present on a Playlist to
refresh its data; it may be hidden. Confirm the actual merge-variable node in
the current editor before writing markup.

Do not infer merge-variable names from a local fixture. A local render cannot
prove a hosted Plugin Merge contract.

## Data-contract checklist

Before markup, write down:

1. The target screen and viewer.
2. Chosen path and data strategy, with the reason.
3. A minimal non-sensitive schema and a synthetic fixture.
4. Source ownership, refresh behavior, and the expected failure/empty state.
5. Where any required credential already lives; never include its value or
   invent a new credential surface.
6. Which hosted operations would be required to prove the contract.

Prefer small, root-level data structures. Keep examples synthetic and
non-identifying so they can safely be reviewed, rendered, and published with
the plugin source.
