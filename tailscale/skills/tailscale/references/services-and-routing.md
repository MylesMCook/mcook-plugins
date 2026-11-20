# Tailscale Services and route selection

> Both areas are newer and moving. Fetch the matching page before giving exact
> commands, plan availability, or limits.

## Tailscale Services

A **Tailscale Service** publishes an internal resource (web app, database, API)
under a stable MagicDNS name and a virtual IP (TailVIP), decoupled from the
devices that host it. Clients connect to the Service name; Tailscale routes to an
available host. Moving, adding, or replacing hosts keeps the same address.

Stable shape:

1. **Define** the Service in the admin console (name, endpoints such as
   `tcp:443`, optional tags).
2. **Host** it on one or more **tag-identified** devices. User-owned devices
   cannot host a Service. Hosts advertise with `tailscale serve --service=svc:<name> ...`
   or a Service configuration file.
3. **Approve** the host (manually or with `autoApprovers`), and grant access to
   the Service in the policy file.

Use it for highly available internal apps, database clusters, cross-cluster
meshes, and stable names for ephemeral deployments. Plain `tailscale serve`
without `--service` shares from a single device; Services are the multi-host form.
The Kubernetes operator and tsnet can also host Services (see `containers.md`
and `tsnet.md`).

## Route selection and MagicRoute

When several connectors overlap (subnet routers advertising the same prefix, app
connectors for the same app, exit nodes, or hosts of one Service), the tailnet
**route selection** setting decides which one a client uses:

- **Active-passive failover**: default; oldest eligible connector wins, others
  are standbys.
- **Regional routing**: picks by DERP region latency (higher plans; not
  compatible with custom DERP).
- **Regional routing with in-region failover**: by support enablement.
- **MagicRoute** (beta): per-client priority score; works with custom DERP.

Subnet routers must advertise identical prefixes to fail over to each other;
longest-prefix match applies and does not fall back to a broader prefix.

## App connectors

App connectors route traffic for SaaS apps (by domain) through designated tailnet
devices, often for static egress IPs or IP allowlists. They participate in route
selection like subnet routers.

## Where to find current information

| Need | Page |
|------|------|
| Tailscale Services overview and setup | https://tailscale.com/docs/features/tailscale-services |
| Services configuration file | https://tailscale.com/docs/reference/tailscale-services-configuration-file |
| Route selection options | https://tailscale.com/docs/features/route-selection |
| MagicRoute | https://tailscale.com/docs/features/magicroute |
| High availability for subnet routers and app connectors | https://tailscale.com/docs/how-to/set-up-high-availability |
| App connectors | https://tailscale.com/docs/features/app-connectors |
| Route injection and access controls | https://tailscale.com/docs/reference/route-injection |
