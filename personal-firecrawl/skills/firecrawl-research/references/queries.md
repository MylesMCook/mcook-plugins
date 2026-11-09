# Query examples

The search engine (Ceramic) matches keywords. Name one subject and one
relationship with specific words; add context words when a short query returns
few results.

| Instead of | Search |
| --- | --- |
| `who was the architect that designed the opera house in Sydney?` | `Sydney Opera House architect` |
| `"best practices" for MCP tool design / naming` | `MCP tool naming guidelines` |
| `site:python.org asyncio TaskGroup` | `site:docs.python.org asyncio TaskGroup` (site matches one exact host) |
| `book called The Overstory by Powers` | `"The Overstory" Richard Powers` |
| `colour or color film restoration` | `(colour OR color) film restoration` |
| `footballer who scored in a cup final and later became a coach in Asia` | `cup final goalscorer later manager Japan`, then a variant per country |
| `paper about bees and roundabouts from around 2010` | `honeybee navigation traffic roundabout study` and `bee foraging route optimisation 2010` |

## Variants

For a hard clue, run 2-3 variants before giving up on it:

1. Name the entity type and the relationship: `novelist Booker shortlist debut`.
2. Use words the answer page itself would contain: `shortlisted debut novel
   Booker Prize announced`.
3. Swap synonyms: `writer`, `author`, `novelist`; `died`, `obituary`, `passed
   away`; `founded`, `established`, `incorporated`.

## Where facts live

Search for the page that would hold the fact, not only the clue words:

- People: obituary, university profile, alumni magazine, Wikipedia
  biography, national biography dictionary.
- Works: journal issue index, publisher catalogue, ISBN record, award
  shortlist page, conference proceedings.
- Lists: Wikipedia "List of ..." pages, league season pages, census tables.
- Organisations and products: official site, registry filing, press release,
  release notes. Name the site or pass its domain as `site`; third-party
  write-ups often outrank the official page.
