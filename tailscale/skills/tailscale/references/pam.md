# Tailscale PAM (formerly Border0)

Tailscale PAM is Tailscale's privileged access management product. It was
called **Border0** (and "Border0 by Tailscale"); the old `/docs/border0/` pages
are marked deprecated. Use the PAM name and the
`/docs/privileged-access-management/` pages. Some identifiers keep the old name,
such as the auto-created `tag:border0-managed` tag and "Border connectors".

> **PAM is in beta and changes often.** Treat this file as orientation. Fetch the
> matching page below before giving setup steps, requirements, or UI paths.

## Mental model (stable)

PAM uses the same identity layer and WireGuard encryption as the rest of
Tailscale. What it adds on top of tailnet reachability:

- **Application-aware access.** Policy answers "can this person run this SSH
  command, query this database, or use this Kubernetes resource", not "can this
  IP reach this host".
- **No shared or static credentials.** PAM holds upstream credentials; users
  authenticate with their Tailscale identity on every connection.
- **Just-in-time, time-bound access** instead of standing privilege.
- **Session evidence.** Session logs, approvals, and recordings where applicable.
- **Two ways in.** The Tailscale client, or a browser client with nothing installed.

Core pieces: a **PAM connector** (Linux, AWS EC2, Docker, or Kubernetes) joins the
tailnet and proxies sessions; **PAM services** (SSH, databases, Kubernetes, RDP,
HTTP, and others) are defined in the admin console and reached through a connector.

Enabling PAM auto-creates a tag, an `autoApprovers` rule, an initial PAM grant for
admins, and an OIDC trust credential. Warn users not to delete those unless they
are replacing that configuration.

## PAM vs. tsrecorder

- **tsrecorder** (see `session-recording.md`) records Tailscale SSH sessions and
  Kubernetes API server proxy sessions. It is self-hosted and part of core Tailscale.
- **PAM** covers more session types (SSH, Kubernetes, RDP, VNC, databases, HTTP)
  with command- or query-level visibility, plus JIT access and credential
  elimination. It is a separate, gated product.

Pick tsrecorder for "record SSH or kubectl sessions". Pick PAM for "govern
privileged access", "no shared database passwords", or "audit what admins ran".

## Access

PAM is enabled per tailnet from the admin console PAM settings page by an Owner,
Admin, or IT admin. Availability is gated (waitlist or sales). Fetch the
get-started page for the current flow; do not assert UI steps from memory.

## Where to find current information

| Need | Page |
|------|------|
| Overview and use cases | https://tailscale.com/docs/privileged-access-management/what-is-tailscale-pam |
| Architecture and concepts | https://tailscale.com/docs/privileged-access-management/architecture-and-concepts |
| Enable and first service | https://tailscale.com/docs/privileged-access-management/get-started |
| Connectors | https://tailscale.com/docs/privileged-access-management/connectors |
| Services | https://tailscale.com/docs/privileged-access-management/services |
| How-to guides (SSH, database, HTTP, Kubernetes) | https://tailscale.com/docs/privileged-access-management/how-to |
| Service accounts and API | https://tailscale.com/docs/privileged-access-management/service-accounts |
| Session logs | https://tailscale.com/docs/privileged-access-management/session-logs |
| Reference | https://tailscale.com/docs/privileged-access-management/reference |
| Section hub | https://tailscale.com/docs/privileged-access-management |

## Answering pattern

1. Decide whether the user needs PAM or core Tailscale (grants, Tailscale SSH,
   tsrecorder). Many "lock down access" questions are answered by grants alone.
2. For PAM setup, connectors, or services, fetch the matching page and quote
   steps and requirements from it.
3. If the user says "Border0", answer with the PAM pages and mention the rename once.
