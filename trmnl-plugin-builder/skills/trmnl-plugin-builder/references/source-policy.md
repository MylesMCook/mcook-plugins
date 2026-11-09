# TRMNL source policy

Use this order before designing or changing a TRMNL implementation.

1. Use TRMNL's official `trmnl` agent skill for its maintained workflow and
   design guidance.
2. Verify product and API behavior in current official TRMNL docs. Start with
   [TRMNL's `llms.txt`](https://docs.trmnl.com/go/llms.txt), then open the linked
   page that owns the feature.
3. For Framework work, use the live [Framework docs](https://trmnl.com/framework/docs)
   and official [`trmnl-framework`](https://github.com/usetrmnl/trmnl-framework)
   source or releases. Query Context7 only as a secondary cross-check because
   its snapshot can lag current Framework releases.
4. Treat local notes, screenshots, previews, source snippets, and third-party
   summaries as supporting evidence, never as current authority.
5. If sources or versions conflict, stop and resolve the conflict before any
   hosted markup, settings, device, refresh, screenshot, publication, or
   deployment change.

## Current source map

| Need | Current official starting point |
| --- | --- |
| Product/docs index | [TRMNL `llms.txt`](https://docs.trmnl.com/go/llms.txt) |
| Private Plugin model and data strategies | [Private Plugins](https://help.trmnl.com/en/articles/9510536-private-plugins) |
| Plugin-type decision | [Compare custom plugin types](https://help.trmnl.com/en/articles/10546870-compare-custom-plugin-types) |
| Private editor markup | [Screen Templating](https://docs.trmnl.com/go/private-plugins/templates.md) |
| Official agent workflow and design guidance | [`usetrmnl/trmnl-agent-skills`](https://github.com/usetrmnl/trmnl-agent-skills) |
| Framework classes and behavior | Live [Framework docs](https://trmnl.com/framework/docs) and [`usetrmnl/trmnl-framework`](https://github.com/usetrmnl/trmnl-framework); Context7 as a secondary cross-check |
| Form Fields | [Custom Plugin Form Builder](https://help.trmnl.com/en/articles/10513740-custom-plugin-form-builder) |
| Webhook payloads and merge strategies | [Webhooks](https://docs.trmnl.com/go/private-plugins/webhooks.md) |
| Plugin Merge data | [Plugin Data API](https://docs.trmnl.com/go/private-api/plugin-data.md) |
| Import/export | [Importing and exporting private plugins](https://help.trmnl.com/en/articles/10542599-importing-and-exporting-private-plugins) |
| Recipes | [Plugin Recipes](https://help.trmnl.com/en/articles/10122094-plugin-recipes) |
| Third Party server flows | [Plugin marketplace docs](https://docs.trmnl.com/go/plugin-marketplace/introduction.md) |
| Self-hosted server/device work | [BYOS](https://docs.trmnl.com/go/diy/byos.md) |

## Evidence record

Before implementation, record the official pages consulted, the feature/version
being relied on, and unresolved ambiguity. Do not silently substitute remembered
class names or copied markup.

Do not hard-code quotas, field types, endpoint contracts, Framework classes,
interpolation delimiters, import schemas, or physical-device behavior from an
old source. Verify the current page/editor for the exact task.
