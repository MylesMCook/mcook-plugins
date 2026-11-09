# Agent research system

A user asks a lead agent to research a technical question. The lead reads the
request, starts up to two read-only research workers, and keeps final synthesis
at the root. Each worker can search documentation and returns evidence to the
lead; workers cannot edit files or spawn descendants. The lead checks material
claims before writing the answer.

The task state is stored by the Codex host. The workers do not share a mutable
database. A failed worker may be retried once when the failure looks transient.
External writes, messages, pushes, and deployments remain parent-owned and
approval-gated.

Unknowns: the supplied brief does not identify the host's internal queue,
transport protocol, or persistence implementation. Those details must not be
invented.
