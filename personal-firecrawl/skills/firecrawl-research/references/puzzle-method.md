# Puzzle method

Use this for questions that pile up constraints ("a person who did X, whose
sibling did Y, in a city that Z") and for any lookup the first searches do not
crack.

## 1. Build a clue ledger

Write each clause of the question as one line: the entity it describes, the
relationship, and any date or number bound. Rank every line:

- **Distinctive**: few things match (a rare event, an exact count, a named
  award, an unusual title, a specific small place).
- **Broad**: many things match (a country, a decade, a profession, "a
  university").

Mark every **vague phrase** ("earliest run", "by-name", "moved to the U.S.",
"first") and write its plausible readings. Keep every reading open until a
fetched page settles it; a candidate that fails one reading may fit another.

Done when every clause maps to a ledger line and every vague phrase lists its
readings.

## 2. Generate candidates from the most distinctive clue

- Start from the most distinctive line. Broad lines only confirm candidates.
- Run 2-3 query variants per clue ([examples](queries.md)).
- Search where the fact would live: a journal index, a Wikipedia list, an
  obituary, an official record. Fetch list pages and scan them for candidates;
  use the [structured sources](sources.md) for papers, theses, archives and
  multi-property lookups.
- When a result names a candidate, search the candidate plus the next
  unresolved clue.
- Pivot after three variants of one clue return nothing relevant. Do not
  enumerate options one by one (each country, each year); move to the next
  distinctive clue instead.

Done when you have one or more candidates that fit the distinctive clues, or
every distinctive clue has had three variants and a pivot.

## 3. Eliminate cheaply first

Check each candidate against the ledger, cheapest check first:

1. Facts already visible in fetched pages.
2. One search on the candidate plus the clue.
3. A fetch of the candidate's main page (biography, official page, record).
4. Deep reads: long PDFs, archives, full lists.

Mark each line **supported** (with a short quote and URL), **missing**, or
**contradicted**. A contradicted distinctive clue eliminates the candidate.
A missing clue lowers confidence; it does not eliminate.

## 4. Stop

Stop when one candidate has every distinctive clue supported, no line
contradicted, and every vague phrase checked under each reading, or when
further checks stop changing the ranking. Report the best
surviving candidate in the answer format from the skill, naming any line still
missing.

## Budget

There is no hard cap, but each step should change what you know. If ten calls
in a row add nothing, change strategy (new clue, new kind of source, subagent
fan-out) rather than repeating the same pattern.
