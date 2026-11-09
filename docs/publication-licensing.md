# Publication licensing review

Reviewed November 8, 2026. Licensing applies per package and per bundled component;
the repository does not impose a new blanket license on imported material.

## Resolved source gaps

| Component | Evidence and treatment |
| --- | --- |
| Canvas Apps | Removed from the current repository at the owner's request in favor of Microsoft's released plugins. The removed reference guides matched Microsoft revision `ea8ce15c7b5f7c001c5d0107401afae65f2716ff`, whose upstream license is MIT. No Canvas Apps source or copied reference documentation remains in this snapshot. Historical copies remain private pending the approved publication-history plan. |
| Writer cleanup references | The old long guide attributed material to Wikipedia without an exact source revision or complete reuse terms. Both cleanup references were replaced with original instructions and fictional examples. The imported clear-writing MIT notice remains intact. See `writer/NOTICE.md`. |
| Writer composition references | The retained modern examples adapt general writing guidance. Project Gutenberg identifies its early William Strunk edition as public domain in the United States. This is not a claim about later Strunk and White editions or other jurisdictions. |
| Vercel Agent Skills | The pinned upstream README and both skill entrypoints explicitly declare MIT. The pinned tree has no separate license or copyright notice file. Those declarations remain in the skills, with exact source links and this limitation recorded in `frontend-react/licenses/vercel-agent-skills-NOTICE.md`. No copyright holder, year, or missing permission text was invented. |
| Fabric native executable | `fabric-mcp-server/THIRD-PARTY-NOTICES.md` indexes 420 original notice files covering all 231 registry packages in upstream v1.10.0's exact Cargo.lock. Every crate archive was checksum-verified before copying, with no crate code executed. Nested AWS-LC/ring notices and Rust 1.95.0 toolchain notices are retained. Five crates' omitted notices were retrieved at their exact archive VCS revisions. The Android-only verifier's supplemental notices use the last upstream commit before publication because its archive has no VCS identity; this limitation is recorded explicitly. |

Primary sources:

- [Microsoft LICENSE at the matching Canvas revision](https://github.com/microsoft/power-platform-skills/blob/ea8ce15c7b5f7c001c5d0107401afae65f2716ff/LICENSE)
- [Microsoft Canvas source at that revision](https://github.com/microsoft/power-platform-skills/tree/ea8ce15c7b5f7c001c5d0107401afae65f2716ff/plugins/canvas-apps)
- [Project Gutenberg's edition and copyright metadata](https://www.gutenberg.org/ebooks/37134)
- [Vercel README at the bundled revision](https://github.com/vercel-labs/agent-skills/blob/20e89cc4bb256eb7b1fcbdc68f7175284709a847/README.md)

## Other bundled notices

The package-level notice inventory retains MIT notices for the copied Frontend /
React components from shadcn/ui, UI Skills, wshobson/agents, and the local skill
source; Apache-2.0 for the Anthropic webapp-testing skill and Chrome DevTools;
BSD-3-Clause for Tailscale; and individual notices for Lawful, Inkblot, Cici,
Buzz, Thermos, and Wails fixtures. Their package attribution files describe the
sources and adaptations. This inventory is not a byte-level audit of every
historical upstream version.

Wails documents Agentation's PolyForm Shield terms separately. Those optional
dependencies are installed into consumer projects; this repository does not
bundle their full packages or grant rights beyond their own licenses.

Deneb and the retired standalone Adversarial Review source have no package-level
license grant. Their provenance identifies locally maintained material. Publishing
owned source and granting downstream reuse rights are separate decisions; no new
license was selected for them during this cleanup.

## History boundary

These changes apply to the current files. Older Writer references remain in Git
history until a separately approved history cleanup removes their earlier versions
and any earlier paths. Adding a current notice or replacement does not establish
the provenance of those older copies. The publication plan must cover every
retained branch and tag, including retired packages.
