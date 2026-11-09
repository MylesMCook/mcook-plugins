# Structured sources

The web search misses much of the long tail: papers, theses, old newspapers,
forum posts and list pages. When a clue names that kind of thing, `fetch` a
structured source directly instead of rephrasing the search. Quote what it
returns like any other page.

| Fact | Fetch |
| --- | --- |
| Wikipedia article on a topic | `https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=KEYWORDS` |
| People, works or places matching several properties | `https://query.wikidata.org/sparql?format=json&query=URL-ENCODED-SPARQL` |
| Papers, authors, theses | `https://api.openalex.org/works?search=KEYWORDS` or `https://api.crossref.org/works?rows=10&query=KEYWORDS` |
| Scanned books, newspapers, old sites | `https://archive.org/advancedsearch.php?output=json&rows=20&fl[]=identifier&fl[]=title&q=KEYWORDS`, then an item's full text |
| A page that fails or has changed | `https://web.archive.org/web/2023/ORIGINAL-URL` |
| Lists and categories (episodes, award winners, alumni) | the Wikipedia list or category page, read whole |

Reddit's JSON endpoints return 403 through Firecrawl; use the search tool for
forum posts instead.
