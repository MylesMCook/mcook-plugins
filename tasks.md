# Claude marketplace compatibility

Objective: support claude.ai marketplace synchronization while preserving Codex
and Cursor packages and the private historical archive.

Implemented: explicit Claude manifests for 25 cloud-compatible packages; Fabric
remains in the Codex/Cursor catalogs and is omitted from Claude's cloud catalog.
MCP and agent definitions live in the Claude manifests. Package/catalog versions
match. The Frontend / React updater preserves those versions on later refreshes.

Verification: Claude validates the catalog and all 25 packages without warnings.
Fourteen sync/cloud-packaging regression tests pass. Portable/Codex package checks
cover all 25 changed packages. Codex/Cursor catalog identities and skill/runtime
files remain unchanged. The cloud-rule checks are offline; a live Claude sync is
the final acceptance check.

Next action: push the reviewed change and verify live Claude marketplace sync.
