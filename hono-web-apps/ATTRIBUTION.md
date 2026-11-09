# Attribution

`hono-web-apps` is an original workflow. It does not copy the Hono documentation or ship upstream
source code. The following primary sources informed terminology, tool behavior, testing order, and
compatibility guardrails.

## Hono documentation

- Source: <https://hono.dev/docs> and the official `llms.txt`, `llms-full.txt`, and
  `llms-small.txt` files.
- Copyright: 2022-present Yusuke Wada and Hono contributors.
- License: MIT, as declared by the official documentation.

## Hono CLI

- Source: <https://github.com/honojs/cli>, reviewed at commit
  `c1b6028d8ea9bacaa1f08eed9345fb4301e9215c`.
- Authors: Yusuke Wada and Taku Amano.
- License: MIT, as declared in the package manifest and README. The reviewed repository snapshot did
  not contain a standalone `LICENSE` file.

## create-hono

- Source: <https://github.com/honojs/create-hono>, reviewed at commit
  `9574c10a9f17f93478b7e6390dab887182b323ea`.
- Copyright: 2021 Ryan Carniato; 2023-present Yusuke Wada and Hono contributors.
- License: MIT. The project notes that it is based on Create Solid, also MIT-licensed.

## Yusuke Wada's hono-skill

- Source: <https://github.com/yusukebe/hono-skill>, reviewed at commit
  `0d2e8dc6fa7e9c6e1c872abdb65db422e95e9de0`.
- Author: Yusuke Wada.
- License: MIT, as declared in the README. The reviewed repository snapshot did not contain a
  standalone `LICENSE` file.
- Adapted concepts: optional `hono-docs` MCP use, project-local Hono CLI guidance, `app.request()`
  smoke testing, `testClient`, RPC type inference, and runtime-aware verification. The procedure and
wording in this plugin were rewritten for portable Agent Plugins and the repository-first safety
boundary.

## simple-code design method

- Source: the `simple-code` Agent Skill maintained by Myles Cook.
- Adapted concepts: lead with the real requirement and dominant risk, prefer the smallest local and
  reversible change, isolate unavoidable complexity, and verify behavior at stable boundaries.
- The plugin does not require or bundle `simple-code`; its Hono-specific workflow is self-contained.
