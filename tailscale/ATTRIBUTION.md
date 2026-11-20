# Attribution

Adapted from [tailscale/tailscale-skill](https://github.com/tailscale/tailscale-skill)
at commit [`4f05d353efc56962546aa26ccc59bb08ca699ad1`](https://github.com/tailscale/tailscale-skill/tree/4f05d353efc56962546aa26ccc59bb08ca699ad1),
reviewed October 10, 2026. The requested discovery page is
[skills.sh/tailscale/tailscale-skill/tailscale](https://skills.sh/tailscale/tailscale-skill/tailscale).

Copyright (c) 2026 Tailscale Inc & contributors. The upstream BSD 3-Clause
license is retained verbatim in [LICENSE](LICENSE). This community marketplace
package does not imply Tailscale endorsement or support.

Upstream had no newer commits when re-reviewed on November 20, 2026.

Changes from upstream in 0.2.0: the entrypoint adds a docs-first retrieval
procedure, operating boundaries, Services and credential routes, and Tailscale
PAM naming. `references/border0.md` was replaced by `references/pam.md`, written
from current Tailscale PAM documentation. `references/docs-map.md`,
`references/services-and-routing.md`, and `references/identity-and-credentials.md`
are new. `references/aperture.md` gained current pages and lost a pinned model
name. Other references are upstream text with host-neutral "fetch" wording in
place of one host's tool name.

Plugin manifests, skill UI metadata, README, changelog, and the freshness check were added for this
marketplace. No upstream installer or executable is bundled.

WireGuard is a registered trademark of Jason A. Donenfeld.
