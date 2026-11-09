# Tufte Critic Rulebook v0

Opinionated rules for reviewing dashboards and analytical displays. Tufte supplies the philosophy and the voice; Cleveland & McGill, Few, Munzner, Brewer, WCAG and the empirical literature fill the gaps where Tufte is silent (interaction, screens, accessibility) or contested.

The rules target what a stock LLM gets wrong when it builds or reviews a dashboard. Each rule names that default ("LLM default") so the critic knows what to look for first.

Version 0.4, 2026-11-09. Draft. v0.3 added G7 (word budgets) after the owner's blind review found rulebook pages too verbose; v0.4 adds minimum type sizes (G6) and C9 (nothing clipped) after v0.3 pages shrank type and clipped panels to fit. Citations carry a verification status; see the legend. Open: Tufte `[B]` page checks, 5 `[K]` items, 2 `[P]` rules.

---

## Legend

**Severity**
- **Blocker**: the display misleads or misstates the data. Always reported.
- **Major**: the reader cannot get to the comparison or decision the display exists for.
- **Minor**: ink, polish, or efficiency. Reported only if there is room.

**Context** (after Few's dashboard roles)
- **operational**: monitored repeatedly, read at a glance, acts on now.
- **analytical**: explored to find causes and patterns.
- **strategic**: summary for leaders, read periodically.
- **all**: applies regardless.

**Detect via**: `S` screenshot, `C` web code (HTML/SVG/React/D3/Recharts/Vega-Lite), `P` Power BI PBIR or Deneb spec, `L` live page in a browser. A rule detected only from `S` must be reported with its confidence.

**Citation status**
- `[V]` verified online: title, venue and the cited finding were checked against the paper, publisher page, standard, or author's site.
- `[V*]` verified through secondary sources (reviews, course slides, mirrors, abstracts), not the primary text. Good enough to cite; check the primary before quoting.
- `[B]` Tufte book claim, needs a page check against your copy.
- `[K]` from model knowledge, not yet verified. Treat as a lead, not a citation.
- `[P]` practitioner rule with no published source yet. The critic must present it as judgment, not as literature.

---

## Review protocol

The critic runs these steps in order. Steps 1 and 2 are mandatory: no rule is applied before the task is named.

1. **Name the thinking task.** Who reads this, what decision or question it serves, how often. Tufte's first question for dashboards is what thinking tasks the display should help with (edwardtufte.com, "Executive dashboards") `[V]`. Munzner's task abstraction gives the vocabulary: actions (analyze, search, query: identify, compare, summarize) paired with targets (trends, outliers, distributions, correlations) (*Visualization Analysis & Design*, "Why: Task Abstraction") `[V*]` (author's course slides; chapter number unverified). If the task cannot be inferred, say so and state the assumption. Naming the task is for you; do not print the audience and question on the page (G7).
2. **Classify the context**: operational, analytical, or strategic (Few, *Information Dashboard Design*, ch. 2, which ranks role first among ways to categorize dashboards because it most affects design) `[V*]`. Several rules change severity by context.
3. **Integrity pass**: every rule in section A. Blockers first.
4. **"Compared to what?" pass**: section B.
5. **Density, encoding, color, words, interaction, documentation**: sections C to I.
6. **Report** at most 7 findings by default: every Blocker, then Majors ranked by how much they block the task, then Minors. Each finding gives rule ID, evidence (what was seen, where), the fix (with a Power BI path when relevant), and the source.
7. **Keep list**: up to 2 things the display does well and a redesign must preserve.
8. **Check the contested list** (section J) before issuing any finding that depends on a contested rule, and soften or drop it when the context matches the exception.

---

## A. Integrity

### A1. Visual size is proportional to the number
- **Severity**: Blocker · **Context**: all · **Detect via**: S C P L
- **Rule**: The size of an effect shown in the graphic must match the size of the effect in the data. Tufte's lie factor is shown effect divided by data effect; he treats values outside roughly 0.95 to 1.05 as substantial distortion.
- **LLM default**: bubbles and icons scaled by radius or height instead of area; pictograms that grow in two dimensions for one-dimensional data; "progress rings" whose arc length does not map linearly.
- **Check**: for every area encoding, confirm area is proportional to value (radius uses a square-root scale). Compute the lie factor for any visibly suspicious comparison.
- **Fix**: switch to position or length (bar, dot). If area is kept: `d3.scaleSqrt`, Vega-Lite `size` channel (area-based by default). Power BI: avoid area encodings for the key comparison.
- **Sources**: Tufte, VDQI ch. 2 "Graphical Integrity" (lie factor, tolerance) `[B]`.

### A2. Bars start at zero; lines show the variation
- **Severity**: Blocker for bars and areas · Major for lines · **Context**: all · **Detect via**: S C P L
- **Rule**: Bars and filled areas encode value by length, so their axis starts at zero. Line charts may use a non-zero domain to show variation, but the axis must be labelled and the domain must not manufacture drama.
- **LLM default**: one axis policy copied to every chart: auto-ranged bars that exaggerate small differences, or zero-based lines that flatten real movement into a horizontal stripe.
- **Check**: bar or area value axis minimum. For lines, whether the domain makes a small change look like a collapse.
- **Fix**: bars at zero, or switch to a dot plot when zero is meaningless. Lines: domain from the data with clear tick labels. Power BI: set value axis Start = 0 on bar/column; leave Auto on lines and check it.
- **Sources**: Correll, Bertini & Franconeri, "Truncating the Y-Axis: Threat or Menace?", CHI 2020 `[V]`: truncation consistently exaggerates perceived effect size, even when the design visibly signals truncation.

### A3. Comparable units: deflate money, normalize counts
- **Severity**: Major (Blocker when nominal growth is presented as real growth) · **Context**: analytical, strategic · **Detect via**: S C P L
- **Rule**: Money over multi-year spans is shown in deflated (real) units. Counts across groups of different size are shown as rates per a stated denominator.
- **LLM default**: nominal revenue trends across years; maps and bars of raw counts by region, which mostly show population.
- **Check**: time span of money series; whether groups differ in size; whether a denominator is stated.
- **Fix**: real terms with base year stated; per-capita, per-store, per-customer, or per-1,000 rates. State units in the axis title.
- **Sources**: Tufte, VDQI ch. 2, principles of graphical integrity (deflated and standardized units) `[B]`.

### A4. No more dimensions than the data has
- **Severity**: Blocker for 3D charts · Minor for pseudo-depth (bevels, shadows on marks) · **Context**: all · **Detect via**: S C P L
- **Rule**: The number of information-carrying dimensions in the graphic does not exceed the number in the data. No 3D bars, 3D pies, or extruded maps for two-dimensional data.
- **LLM default**: rare as true 3D now; common as gradient fills, bevels and drop shadows on bars inherited from themes.
- **Fix**: flat marks, solid fills.
- **Sources**: Tufte, VDQI ch. 2 `[B]`. Cleveland & McGill (1984) rank volume among the least accurate encodings `[V]`.

### A5. Do not quote data out of context
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: Show enough history, or enough peers, for the reader to judge whether the current value is unusual.
- **LLM default**: "last 7 days" or "this month vs last month" as the only view; a KPI delta versus yesterday with no sense of normal variation.
- **Check**: time window length relative to the cycle of the measure (weekly seasonality needs weeks; yearly needs years).
- **Fix**: longer default window, same-period-last-year, sparkline of the full history beside the headline number.
- **Sources**: Tufte, VDQI ch. 2 (graphics must not quote data out of context) `[B]`. Tufte on sparklines reducing recency bias in decision-making (edwardtufte.com, "Executive dashboards") `[V]`.

### A6. Show data quality, partial periods and gaps
- **Severity**: Blocker when an incomplete period is drawn as complete · Major otherwise · **Context**: all · **Detect via**: S C P L
- **Rule**: Incomplete periods, missing data, small samples, restatements and definition changes are marked on the display.
- **LLM default**: the current partial month plotted as a normal bar, so it looks like a crash; nulls drawn as zeros; lines interpolated through gaps.
- **Check**: the last period's completeness; how nulls render; sample sizes behind rates.
- **Fix**: exclude or visually distinguish the partial period (hollow or lighter mark, a short "MTD" or "month to date" label, not a sentence); break lines at gaps; show n beside rates.
- **Sources**: Tufte, "Executive dashboards": build in systematic checks of data quality, beware "sampling to please" `[V]`. Tufte, *Beautiful Evidence* ch. 5, principle 5 (thoroughly describe the evidence) `[V]`.

### A7. No dual value axes
- **Severity**: Major (Blocker when scales are chosen so the lines cross or track) · **Context**: all · **Detect via**: S C P L
- **Rule**: Two measures with different units are not plotted against two y-axes on one chart. The apparent crossing points and correlation are artifacts of the arbitrary scale choice.
- **LLM default**: column-plus-line combo with a secondary axis, especially in Power BI.
- **Check**: two value axes on one plot area. Power BI: "Line and stacked column" and "Line and clustered column" combo charts create a secondary y-axis as soon as a line value is added `[V]`; Microsoft's own docs present this as the way to compare sales with margin %. PBIR `visualType` identifiers (`lineClusteredColumnComboChart`, `lineStackedColumnComboChart`) `[K]`: confirm against a real PBIR export.
- **Fix**: two charts stacked with a shared x-axis, or index both series to 100 at a base period and plot on one axis. Power BI: when both measures share units, sync the axes (secondary y-axis range to Auto, values off) so both use one scale `[V]`.
- **Exception**: see J8 (expert audiences reading co-movement).
- **Sources**: Few, "Dual-Scaled Axes in Graphs: Are They Ever the Best Solution?", Visual Business Intelligence Newsletter, Perceptual Edge, March 2008 `[V*]`: Few could not think of a case that warrants them given better alternatives.

---

## B. "Compared to what?"

### B1. Every headline number has a reference
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: No number stands alone. Each headline value is shown against a target, a prior period, the same period last year, a peer, or its own distribution.
- **LLM default**: the KPI tile: large number, small green arrow, "+3.2%" with no stated base, no target, no absolute prior value.
- **Check**: for every KPI, what the reader is meant to compare it with, and whether that comparison is on the page.
- **Fix**: bullet graph (value, target, qualitative ranges) or number + sparkline + explicit comparison text ("4.2M, target 4.0M, last year 3.9M"). Power BI: no native bullet graph; use a bar with a target line, a Deneb bullet graph, or Microsoft's open-source Bullet chart visual (microsoft/powerbi-visuals-bulletchart) if your org allows custom visuals `[V]`.
- **Sources**: Tufte, *Beautiful Evidence* ch. 5, principle 1 (show comparisons, contrasts, differences) `[V]`. Few, "Common Pitfalls in Dashboard Design" (2006), pitfall 2 "Supplying inadequate context for the data" `[V]`.

### B2. Plot the difference when the difference is the point
- **Severity**: Major · **Context**: analytical, operational · **Detect via**: S C P L
- **Rule**: If the question is the gap (actual vs plan, this year vs last), show the gap directly instead of two series the reader must subtract by eye.
- **LLM default**: two overlaid lines, actual and target, and a title about the variance.
- **Fix**: a variance chart: target as a 0% reference line, variance plotted above and below it as percentages. Or keep the two lines and add the plotted difference beneath.
- **Sources**: Few, pitfall 4 "Expressing measures indirectly", whose example is exactly this: revenue vs plan redrawn as % variance around a 0% plan line `[V*]`. Cleveland, *The Elements of Graphing Data*: readers judge the gap between two curves by the nearest (perpendicular) distance, not the vertical one, so curves appear to converge when they do not; his remedy is to plot the difference `[V*]` (book page unverified).

### B3. Compared things share a scale and a baseline
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: Panels meant to be compared use the same axis range and are aligned so their baselines line up.
- **LLM default**: small multiples or a card grid where every chart auto-scales independently, so every panel looks equally volatile and equally large.
- **Check**: axis ranges across sibling charts.
- **Fix**: shared domains (Vega-Lite `resolve: {scale: {y: "shared"}}`, the default for facets; Power BI native small multiples share the y-axis by default ("Shared y-axis" under Y-axis > Range) `[V]`; separate visuals never do). Free scales only when shape matters more than level, and then label it loudly. In Power BI, flag "Shared y-axis" turned off.
- **Sources**: Cleveland & McGill (1984): position along a common scale is read most accurately `[V]`; replicated by Heer & Bostock, "Crowdsourcing Graphical Perception", CHI 2010 `[V]`.

### B4. Show normal variation
- **Severity**: Major for operational · Minor otherwise · **Context**: operational, strategic · **Detect via**: S C P L
- **Rule**: Readers need to tell signal from noise. Show the normal range (historical band, interquartile band, control limits) behind a monitored series.
- **LLM default**: a bare line, or red/green deltas on every wiggle, which trains readers to react to noise.
- **Fix**: a gray normal-range band behind the line or sparkline; process-behaviour chart limits for operational metrics.
- **Sources**: Tufte, *Beautiful Evidence* ch. 2 "Sparklines" (normal-range band) `[B]`. Wheeler, *Understanding Variation: The Key to Managing Chaos* (1993; 2nd ed. 2000): process behaviour charts with natural process limits computed from baseline variation separate signal from noise `[V*]`.

### B5. Show the distribution behind an average
- **Severity**: Major when a decision rests on the mean · **Context**: analytical · **Detect via**: S C P L
- **Rule**: Means and totals hide the shape. When a decision depends on a central value, show the spread (dots, strip plot, quartile plot, histogram).
- **LLM default**: average handle time, average order value, average score: one number or one bar per group.
- **Fix**: dot or strip plots with the mean marked; Tufte's quartile plot (redesigned box plot).
- **Sources**: Tufte, VDQI ch. 6 (quartile plot) `[V via public notes; B for wording]`. Anscombe's quartet as reproduced in VDQI `[B]`.

### B6. Annotate the events that explain the data
- **Severity**: Major · **Context**: analytical, strategic · **Detect via**: S C P L
- **Rule**: Known causes (price changes, outages, releases, campaigns, definition changes) are marked on the time axis where they happened, with a label of 8 words or fewer.
- **LLM default**: no annotations; explanations, if any, in a separate text box or not at all.
- **Fix**: event markers with short labels on the chart; a vertical rule plus one line of text.
- **Sources**: Tufte, *Beautiful Evidence* ch. 5, principle 2 (show causality, mechanism, explanation) `[V]`. Kim, Setlur & Agrawala, CHI 2021: annotations that make the key feature prominent help readers take away the intended message `[V]`.

---

## C. Density and layout

### C1. More data per square inch
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: Increase data density. A dashboard screen is expensive real estate; a large tile holding one number wastes it.
- **LLM default**: a row of 4 to 6 large KPI cards, each one number, plus two charts with a dozen points each.
- **Check**: rough count of data values on screen versus screen area taken by chrome and whitespace.
- **Fix**: a compact table of KPIs, each row with value, comparison and sparkline (Tufte's "supertable" approach). Shrink charts; they still read when small.
- **Sources**: Tufte, VDQI ch. 8 "High-Resolution Data Graphics" (data density, shrink principle) `[B]`. Tufte, "Executive dashboards" (simple designs showing high-resolution data; supertable, VDQI p. 179) `[V]`.

### C2. Small multiples instead of filters, toggles or animation
- **Severity**: Major · **Context**: analytical, strategic · **Detect via**: S C P L
- **Rule**: When the reader's question is a comparison across categories or periods, show all of them at once in small multiples. A slicer or tab shows one at a time and leaves the comparison to memory.
- **LLM default**: one chart plus a region dropdown or a "select metric" toggle.
- **Fix**: grid of identical small charts, shared scales (B3), ordered meaningfully (C8). Power BI: native small multiples on line, bar and column charts.
- **Exception**: more than roughly 20 to 30 categories; use an overview plus filter.
- **Sources**: Tufte, VDQI ch. 8 and *Envisioning Information* ch. 4 "Small Multiples" `[B]`.

### C3. Sparklines carry trend context
- **Severity**: Minor (Major when no trend context exists anywhere) · **Context**: all · **Detect via**: S C P L
- **Rule**: Word-sized trend lines next to numbers in tables and KPI rows give history at almost no space cost.
- **LLM default**: none, or a full-size chart per metric.
- **Fix**: sparklines with the last value marked and, where useful, a normal-range band. Power BI: native sparklines in table and matrix.
- **Sources**: Tufte, *Beautiful Evidence* ch. 2 "Sparklines" `[V]`; "Executive dashboards" `[V]`.

### C4. Operational dashboards fit one screen
- **Severity**: Major for operational · **Context**: operational · **Detect via**: S L
- **Rule**: A monitoring display shows everything needed at a glance on one screen, without scrolling or paging. Fit by cutting content, never by shrinking type below G6 or clipping panels (C9).
- **LLM default**: long scrolling page of stacked sections.
- **Sources**: Few, pitfall 1 "Exceeding the boundaries of a single screen" `[V]`.

### C9. Nothing clipped, overlapping or off-screen
- **Severity**: Major · **Context**: all · **Detect via**: S C L
- **Rule**: At the target viewport, every label, value and panel is fully visible: no horizontal page scroll, no text or chart cut off by its container, no labels drawn over each other or over marks.
- **LLM default**: fixed-height panels and grids that clip their content once the page is compacted; end labels on lines that collide; wide grids that run past the right edge.
- **Check**: render at the target viewport; look for truncated text, clipped charts, overlapping labels, and a page wider than the window.
- **Fix**: let content set panel height, wrap or stack columns, thin or offset colliding labels, drop the least important element rather than squeezing.
- **Sources**: `[P]`. v0.3 builds clipped panels and misaligned grids when compacting (`evals/authoring/runs/2026-11-06-terse-v03/REPORT.md`).

### C5. Tables are graphics; design them
- **Severity**: Minor (Major when a table is the main display) · **Context**: all · **Detect via**: S C P L
- **Rule**: Use a table when readers look up exact values. Right-align numbers, use tabular figures, keep decimals consistent per column, minimize rules, group with whitespace, sort meaningfully.
- **LLM default**: zebra stripes plus full gridlines, centered numbers, proportional figures, mixed precision.
- **Fix**: CSS `font-variant-numeric: tabular-nums`; right-aligned numeric columns; light rules only between groups.
- **Sources**: Tufte, VDQI ch. 9 (tables) `[B]`. Few, *Show Me the Numbers* `[K]`.

### C6. Size and position follow importance
- **Severity**: Major · **Context**: all · **Detect via**: S L
- **Rule**: The most important information gets the most prominent position (top left in left-to-right reading) and the most space. Uniform grids imply equal importance.
- **LLM default**: identical card grid, every chart the same size, order arbitrary.
- **Sources**: Few, pitfalls 9 "Arranging the data poorly" and 10 "Ineffectively highlighting what's important" `[V]`.

### C7. Aspect ratio shows the trend
- **Severity**: Minor (Major when the shape hides the trend) · **Context**: all · **Detect via**: S C P L
- **Rule**: Choose line-chart proportions so the slopes that matter are near 45 degrees. Avoid long flat strips that hide change and tall narrow charts that exaggerate it.
- **LLM default**: every chart stretched to the container width at a fixed short height.
- **Sources**: Cleveland, McGill & McGill, "The Shape Parameter of a Two-Variable Graph", JASA 83, 1988, banking to 45 degrees `[V]`. Heer & Agrawala, "Multi-Scale Banking to 45 Degrees", IEEE TVCG 2006 `[V title/venue]`. Talbot, Gerth & Hanrahan, "Arc Length-Based Aspect Ratio Selection", InfoVis 2011 `[V title/venue]`. Tufte, VDQI ch. 9 (graphics tend to be wider than tall) `[B]`.

### C8. Order by meaning, not by accident
- **Severity**: Minor (Major when ranking is the question) · **Context**: all · **Detect via**: S C P L
- **Rule**: Sort categories by value, or by a natural order (time, process step, geography). Never alphabetically or in source order by default.
- **LLM default**: alphabetical or database order.
- **Sources**: Few, pitfall 9 `[V title]`. Cleveland, "Graphical Methods for Data Presentation: Full Scale Breaks, Dot Charts, and Multibased Logging", *The American Statistician* 38(4), 1984, introduces dot charts as a more effective replacement for bar charts `[V*]`; sorting by value as the default `[K]`.

---

## D. Encoding and chart choice

### D1. Encode key comparisons with position or length
- **Severity**: Major when the main comparison uses angle, area or color intensity · **Context**: all · **Detect via**: S C P L
- **Rule**: Accuracy ranking: position along a common scale; position along non-aligned scales; length, direction and angle; area; volume and curvature; shading and color saturation. Put the comparison that matters highest on that list.
- **LLM default**: treemaps, bubble charts, donuts and filled maps for comparisons that a sorted bar would answer.
- **Fix**: sorted bar or dot plot.
- **Sources**: Cleveland & McGill, "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods", JASA 79(387), 1984 `[V]`. The full ordering was proposed as a hypothesis; their experiments tested position vs length and position vs angle. Heer & Bostock, CHI 2010, replicated the tested tasks `[V]`.

### D2. Pies and donuts: parts of a whole, few parts
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: A pie or donut is acceptable only for 2 or 3 parts of one whole, when the question is "roughly what share". For more parts, or comparing across groups, use bars.
- **LLM default**: donut with 6 to 10 slices, a legend, and a total in the hole.
- **Note**: the problem is slice count and task, not the hole. Donuts are read about as accurately as pies.
- **Sources**: Skau & Kosara, "Arcs, Angles, or Areas: Individual Data Encodings in Pie and Donut Charts", EuroVis 2016 `[V]`.

### D3. No gauges, dials, speedometers or traffic lights
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: Gauges spend large area on decoration to show one number poorly. Traffic lights encode status by hue only.
- **LLM default**: gauge visuals for KPIs, red/amber/green circles.
- **Check**: Power BI `visualType` = `gauge` `[K]`.
- **Fix**: bullet graph; value plus target plus sparkline. Per Few's spec, draw the featured measure as a bar, or as a dot when the scale does not start at zero; variants exist for lower-is-better measures.
- **Sources**: Few, pitfall 7 "Using poorly designed display media" `[V title]`; Few, "Bullet Graph Design Specification", Perceptual Edge, rev. 2013, designed as a replacement for gauges and meters `[V*]`. Tufte, "Executive dashboards": avoid "heavy-breathing metaphors" such as cockpits and mission control `[V]`.

### D4. Stacked charts: only the bottom and the total are readable
- **Severity**: Major when components must be compared · **Context**: all · **Detect via**: S C P L
- **Rule**: In stacked bars and areas, only the bottom segment and the total sit on a common baseline. Middle segments cannot be compared.
- **LLM default**: stacked area with 5 or more categories over time.
- **Fix**: small multiples per component, or grouped bars or lines; keep stacking only when the total is the point.
- **Sources**: Cleveland & McGill (1984): position along non-aligned scales ranks below a common scale `[V]`.

### D5. Slopegraphs for two-point comparisons
- **Severity**: Minor (suggestion) · **Context**: analytical, strategic · **Detect via**: S C P L
- **Rule**: When many categories are compared at two times, a slopegraph shows both rank and change in one view.
- **LLM default**: clustered bars for before/after across many categories.
- **Sources**: Tufte, "Slopegraphs for comparing gradients: Slopegraph theory and practice", edwardtufte.com `[V title]`.

### D6. Log scales for rates of change and wide ranges
- **Severity**: Minor · **Context**: analytical · **Detect via**: S C P L
- **Rule**: When growth rates matter, or values span orders of magnitude, use a log scale and label it.
- **Sources**: Tufte, "Taking logarithms in statistical data", edwardtufte.com `[V title]`.

---

## E. Data-ink and chrome

### E1. Erase the chrome
- **Severity**: Minor per instance · Major when chrome visibly outweighs data · **Context**: all · **Detect via**: S C P L
- **Rule**: Card borders, drop shadows, panel backgrounds, gradients, decorative icons, rounded containers and heavy headers are non-data ink. Remove them unless they do work (grouping, for example, can usually be done with whitespace).
- **LLM default**: the strongest default of all. Component-library cards with border, radius, shadow and an icon in every corner.
- **Check**: Power BI Format visual > General > Effects: Background, Visual border (with rounded corners), Shadow `[V]`. These are often set report-wide by the theme, so fix them in the theme.
- **Sources**: Tufte, VDQI ch. 4 "Data-Ink and Graphical Redesign" `[B]`. Few, pitfall 11 "Cluttering the screen with useless decoration" `[V]`.

### E2. Mute or remove gridlines
- **Severity**: Minor · **Context**: all · **Detect via**: S C P L
- **Rule**: Gridlines, if needed at all, are faint and fewer. Often direct value labels or a few reference lines at meaningful values do the job better.
- **LLM default**: library-default gridlines at every tick, often dark.
- **Sources**: Tufte, VDQI ch. 5 "Chartjunk: Vibrations, Grids, and Ducks" `[V title]`; ch. 7 on the data-based grid `[V via public notes]`.

### E3. Say it once
- **Severity**: Minor · **Context**: all · **Detect via**: S C P L
- **Rule**: The same number appearing in title, data label, axis, tooltip and legend is redundant ink. Keep the one that serves the reader.
- **Sources**: Tufte, VDQI ch. 4 (erase redundant data-ink) `[B]`.

### E4. Economical axes
- **Severity**: Minor · **Context**: all · **Detect via**: S C P L
- **Rule**: Axes carry information: range-frames (axis lines spanning only the data range), ticks at meaningful values (min, max, latest, target), no box around the plot.
- **Sources**: Tufte, VDQI ch. 6 (range-frame, dot-dash-plot) `[V via public notes]`.

---

## F. Color

### F1. Gray by default, one accent for what matters
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: Use the smallest effective difference. Context is gray; color is reserved for the series, point or status that needs attention.
- **LLM default**: a categorical palette applied to every series on every chart; brand color on everything, so nothing stands out.
- **Sources**: Tufte, *Visual Explanations* ch. 4 "The Smallest Effective Difference" `[B]`; *Envisioning Information* ch. 5 "Color and Information" `[B]`. Few, pitfall 12 "Misusing or overusing color" `[V]`.

### F2. Palette type matches the data
- **Severity**: Major · **Context**: all · **Detect via**: S C P
- **Rule**: Sequential palettes for ordered magnitude; diverging only around a meaningful midpoint (zero, target, average); categorical for unordered groups, about 7 at most. No rainbow scales for ordered data.
- **LLM default**: diverging red-green for data with no midpoint; rainbow heatmaps; categorical colors on an ordered variable.
- **Sources**: Harrower & Brewer, "ColorBrewer.org: An Online Tool for Selecting Colour Schemes for Maps", *The Cartographic Journal* 40(1), 2003: schemes chosen by number of classes, data type and display environment `[V*]`. Borland & Taylor, "Rainbow Color Map (Still) Considered Harmful", IEEE CG&A 2007 `[V]`. See J5 for the counterpoint.

### F3. Never rely on red versus green alone
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: Status and direction are carried by sign, position, shape or text as well as hue. Red/green is the most common color-vision deficiency confusion.
- **LLM default**: green up arrows and red down arrows as the only signal; red/green conditional formatting.
- **Fix**: signed numbers, arrows plus text, blue/orange as the hue pair.
- **Sources**: WCAG 2.2 SC 1.4.1 "Use of Color" (Level A): color is not the only visual means of conveying information `[V]`. Tufte, VDQI ch. 9, design for color-deficient viewers `[B]`.

### F4. One color, one meaning, everywhere
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: A category or measure keeps the same color across every chart, and the accent color never means two things on one page.
- **LLM default**: each chart assigns palette colors independently, so "West" is blue on one chart and orange on the next.
- **Sources**: Few, pitfall 12 `[V title]`. The cross-chart consistency principle itself is `[P]`.

### F5. Contrast that passes
- **Severity**: Major · **Context**: all · **Detect via**: C P L (S approximate)
- **Rule**: Text, including text inside charts, at least 4.5:1 against its background (3:1 for large text). Graphical objects needed to understand the chart (data lines, bars, pie slices, essential gridlines) at least 3:1 against adjacent colors. Series lines need not contrast with each other when they do not overlap much. Gridlines count only if removing them would change the information.
- **LLM default**: light gray axis labels and pale pastel series that fail contrast.
- **Sources**: WCAG 2.2 SC 1.4.3 "Contrast (Minimum)" (AA) and SC 1.4.11 "Non-text Contrast" (AA), with W3C's Understanding 1.4.11 chart examples and technique G209 for adjoining slice colors `[V]`.

---

## G. Words and numbers

### G1. Titles state the finding, and the chart must show it
- **Severity**: Major · **Context**: analytical, strategic · **Detect via**: S C P L
- **Rule**: The title says what the reader should take away ("Churn doubled after the March price change"), in 14 words or fewer, and that feature must be the most visually prominent thing in the chart. A finding title over a chart that emphasizes something else will be overridden by the chart.
- **LLM default**: topic titles ("Churn by Month").
- **Exception**: operational views whose finding changes daily: title states the question and the scope, or uses a computed narrative.
- **Guard**: a title that overstates or slants what the data shows is an integrity problem (see J6).
- **Sources**: Kim, Setlur & Agrawala, "Towards Understanding How Readers Integrate Charts and Captions", CHI 2021 `[V]`: when the caption names a low-prominence feature, readers take away the chart's prominent feature instead. Kong, Liu & Karahalios, "Frames and Slants in Titles of Visualizations on Controversial Topics", CHI 2018: titles stating the main message were recalled; generic titles were not; slanted titles steered what readers remembered `[V*]`.

### G2. Label directly; drop the legend
- **Severity**: Minor (Major when the legend has more than 4 entries) · **Context**: all · **Detect via**: S C P L
- **Rule**: Put series names at the end of lines and on or beside bars. A legend forces the eye to travel back and forth and to match colors from memory.
- **LLM default**: legend on every chart, often at the top or right.
- **Sources**: Tufte, VDQI ch. 9 (friendly graphics label directly, without legends) `[B]`. Tufte, *Beautiful Evidence* ch. 5, principle 4 (integrate words, numbers, images) `[V]`.

### G3. Words and graphics in one place
- **Severity**: Major · **Context**: analytical, strategic · **Detect via**: S C P L
- **Rule**: Explanations, definitions, targets and thresholds sit on or next to the chart they explain, not in a separate panel, page or tooltip. Integrate words as short labels and annotations, never as paragraphs beside the chart (G7).
- **LLM default**: a "Key insights" text card disconnected from the charts it describes.
- **Sources**: Tufte, *Beautiful Evidence* ch. 4 and ch. 5, principle 4 `[V]`.

### G4. Precision fits the decision
- **Severity**: Minor · **Context**: all · **Detect via**: S C P L
- **Rule**: Two or three significant figures on a dashboard. $3.8M, not $3,848,305.93. Consistent units and abbreviations across the page.
- **LLM default**: raw database precision; mixed K/M/full numbers; percentages to two decimals.
- **Sources**: Few, pitfall 3 "Displaying excessive detail or precision" (uses the $3,848,305.93 example) `[V]`.

### G5. Every number has a unit, a period and a definition
- **Severity**: Major · **Context**: all · **Detect via**: S C P L
- **Rule**: Units, time period and metric definitions are visible or one step away. "Active users" means nothing without the definition. Put units in axis titles and labels; spell out a definition only where a reader would otherwise misread the number, in the footer line (G7).
- **Sources**: Tufte, *Beautiful Evidence* ch. 5, principle 5 `[V]`.

### G6. Readable type
- **Severity**: Major when text is below the minimum for its viewing distance · Minor otherwise · **Context**: all · **Detect via**: S C P L
- **Rule**: No rotated axis labels (switch to horizontal bars), no all-caps titles, labels written in words not codes, and no text below these minimums at the target viewport:
  - Desktop page, read at arm's length (about 1440 px wide): tick labels and footers at least 11 px, other labels and body at least 13 px, headline at least 20 px.
  - Wall screen, read across a room (1920 x 1080): nothing under 18 px, labels at least 22 px, the key figures at least 48 px.
- **LLM default**: 45-degree rotated category labels on vertical bars; database field names as labels; shrinking type to make a page fit one screen.
- **Fix**: cut content until the page fits at these sizes (G7, C4); never shrink type to fit.
- **Sources**: Tufte, VDQI ch. 9 (friendly graphics: words spelled out, read left to right, upper and lower case) `[B]`. Minimum sizes are `[P]`: v0.3 builds shrank wall-screen type below legibility to meet word and one-screen budgets (`evals/authoring/runs/2026-11-06-terse-v03/REPORT.md`).

---

### G7. Every word earns its place
- **Severity**: Major when prose competes with the data (the reader must read paragraphs to get the answer) · Minor otherwise · **Context**: all · **Detect via**: S C P L
- **Rule**: The page answers in its headline and its graphics, not in paragraphs. Word budgets for a dashboard:
  - One headline, at most 14 words, stating the finding.
  - Chart titles at most 10 words; at most one subtitle line per chart, 20 words or fewer.
  - Annotations at most 8 words each.
  - Documentation in one footer of at most two lines: source, refresh time, scope, owner, and only the definitions a reader would otherwise get wrong.
  - Total prose (sentences outside tables, axes and labels) under about 120 words for a one-screen dashboard, 200 for a longer report page.
  - No intro paragraph, "key insights" block, methods section, caveat list, or printed restatement of the audience and question.
  Say in words only what the graphic cannot: the cause, the action, or a caveat that changes a decision. Never restate a number the chart already labels.
- **LLM default (with this rulebook loaded)**: satisfying G1, G5, I1 and A6 by adding sentences: a subtitle that restates who the page is for and what it answers, a paragraph under every chart, a methods-and-limits section. Rulebook v0.2 builds carried about 50% more words than plain builds (median 454 vs 300).
- **Check**: count prose words against the budgets; flag any paragraph over two sentences and any sentence that repeats a labelled value.
- **Fix**: cut to headline plus labels; put units and definitions in axis titles; fold source, refresh, scope and owner into one footer line; delete restatements. Budgets never justify smaller type or tighter panels: cut content instead (G6, C9). Power BI: titles and subtitles in the visual header, one text box footer, no narrative text boxes.
- **Sources**: Tufte, VDQI ch. 4 (erase redundant data-ink; the same discipline applies to words) `[B]`. Few, "Common Pitfalls in Dashboard Design", pitfall 3 "Displaying excessive detail or precision" `[V title]`. Owner blind review, 2026-11-06: rulebook pages preferred 15 to 5, but 4 of 6 notes called them too verbose (`evals/authoring/review/RESULTS.md`) `[P]`.

---

## H. Interaction (live pages and Power BI)

### H1. Tooltips hold details, not the answer
- **Severity**: Major · **Context**: all · **Detect via**: C P L
- **Rule**: Anything needed to answer the display's main question is visible without hovering. Hover has no equivalent on touch screens or in a screenshot, export, or printout.
- **LLM default**: values only in tooltips; no data labels anywhere.
- **Sources**: Shneiderman, "The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations", IEEE Symposium on Visual Languages, 1996: "overview first, zoom and filter, then details-on-demand" `[V]`. The overview carries the answer; details are on demand.

### H2. The default view answers the main question; filters are visible
- **Severity**: Major · **Context**: all · **Detect via**: P L
- **Rule**: On open, the display shows the most useful state (latest complete period, full population). Active filters are stated on the canvas so screenshots and exports carry them.
- **LLM default**: slicers default to everything or to a stale saved selection; filter state invisible.
- **Sources**: `[P]`.

### H3. No animation for comparison
- **Severity**: Minor (Major if the comparison only exists in the animation) · **Context**: analytical · **Detect via**: C L
- **Rule**: Animated transitions and play-axis animations make the reader compare frames from memory. Use small multiples or a static trace.
- **Exception**: animation can work in a narrated presentation; the study found it least effective for analysis, not for telling a story.
- **Sources**: Robertson, Fernandez, Fisher, Lee & Stasko, "Effectiveness of Animation in Trend Visualization", IEEE TVCG 14(6), 2008: animation was the least effective form for analysis; static traces and small multiples were faster, and small multiples more accurate `[V]`.

---

## I. Documentation

### I1. Source, freshness, scope and owner on the page
- **Severity**: Major for decision dashboards · Minor otherwise · **Context**: all · **Detect via**: S C P L
- **Rule**: Data source, last refresh time, coverage (which entities, which period) and the owner are visible on the page, in one footer line or two at most (G7). Documentation is a footnote, not a section.
- **LLM default**: none.
- **Sources**: Tufte, *Beautiful Evidence* ch. 5, principle 5 (document sources, authors, measurement scales) `[V]`.

---

## J. Contested and nuanced

The critic must check these before issuing findings that rest on them.

- **J1. Decoration and memory.** Bateman et al., "Useful Junk?", CHI 2010 `[V]`: embellished charts were interpreted no less accurately and remembered better after 2 to 3 weeks. Borkin et al., "What Makes a Visualization Memorable?", IEEE TVCG 2013: color and human-recognizable objects raise memorability, and unusual chart types beat common ones; the authors caution that memorable is not the same as comprehensible `[V]`. Ruling: for a dashboard read repeatedly, memorability is not the goal and E1 stands. For a one-off presentation or public graphic, downgrade decoration findings to Minor and flag only decoration that competes with the data.
- **J2. Minimalism taken literally.** Tufte qualifies data-ink maximization with "within reason" `[B]`. Inbar, Tractinsky & Meyer (ECCE 2007) showed participants a minimal and a non-minimal bar chart, both from Tufte's own book; participants clearly preferred the non-minimal one `[V*]`. Ruling: never recommend removing axes, labels or reference lines the reader needs to read values.
- **J3. Pies.** Skau & Kosara 2016 `[V]`: donuts are not worse than pies, and readers use arc length and area as much as angle. Ruling: D2 is about slice count and task, not the hole.
- **J4. Line baselines.** Correll et al. 2020 `[V]` show truncation exaggerates perceived effect. Ruling: lines may use a non-zero domain, but if the title or decision depends on effect size, show the magnitude explicitly (percent change, absolute change).
- **J5. Rainbows.** Borland & Taylor 2007 `[V]` vs Ware, Stone & Szafir, "Rainbow Colormaps Are Not All Bad", IEEE CG&A 43(3), 2023, who argue rainbows have strengths current conventions overlook `[V]`. Also Reda, "Rainbow Colormaps: What are they good and bad for?", IEEE TVCG `[V* exists]`. Ruling: rainbow is still wrong for ordered magnitude on business dashboards; do not flag it in expert scientific displays without asking about the task.
- **J6. Finding titles can slant.** Kong et al. 2018 `[V*]`: readers rated slanted-title charts as neutral and recalled the slanted message. Ruling: G1 applies only when the title is supported by the chart's most prominent feature and the data; otherwise use a neutral question title. A finding title that the data does not support is an integrity finding, not a style one.
- **J7. Tufte on dashboards at all.** Tufte's books are about print. Screen density, interaction and accessibility rules here (C4, F5, H1 to H3) come from Few, WCAG and HCI research, not Tufte. The critic must not attribute them to Tufte.
- **J9. Integrating words vs. glanceability.** Tufte asks for words, numbers and images together (*Beautiful Evidence* ch. 5, principle 4) `[V]`, and readers of dashboards scan rather than read (G7). Ruling: integrate words at the point of need as short labels and annotations; never as paragraphs. When G3 or I1 and G7 pull against each other, G7's budgets win.
- **J8. Dual axes for experts.** Brath, Hagerman & Sorenson (IV 2020 presentation, "Why Two Y-Axes?") argue dual axes are common and useful among financial experts reading when two series move together or apart `[V* exists; not peer-review-checked]`. Ruling: keep A7 as Major for general business audiences. For expert audiences whose task is co-movement, downgrade to Minor if both axes are clearly labelled and colored to match their series, and suggest the indexed alternative.

---

## Sources

Status in brackets. Tufte book chapters marked `[B]` are verified against the book; titles of VDQI chapters 4 to 8 were confirmed from the table of contents.

**Tufte**
- *The Visual Display of Quantitative Information*, 2nd ed., Graphics Press, 2001 (VDQI). Chapters: 4 Data-Ink and Graphical Redesign (p. 91), 5 Chartjunk: Vibrations, Grids, and Ducks (p. 107), 6 Data-Ink Maximization and Graphical Design (p. 123), 7 Multifunctioning Graphical Elements (p. 139), 8 High-Resolution Data Graphics (p. 160) `[V]`. Chapters 1 to 3 and 9 titles `[B]`.
- *Envisioning Information*, 1990. Chapters include Escaping Flatland, Micro/Macro Readings, Layering and Separation, Small Multiples, Color and Information, Narratives of Space and Time `[V via secondary listing]`.
- *Visual Explanations*, 1997. Includes "The Smallest Effective Difference" `[B]`.
- *Beautiful Evidence*, 2006. Chapters include Mapped Pictures, Sparklines, Links and Causal Arrows, Words/Numbers/Images Together, The Fundamental Principles of Analytical Design (six principles), Corrupt Techniques in Evidence Presentations, The Cognitive Style of PowerPoint `[V via review and publisher pages]`.
- *Seeing with Fresh Eyes: Meaning, Space, Data, Truth*, 2020 `[V exists; contents not yet mined]`.
- edwardtufte.com notebook: "Executive dashboards"; "Sparkline theory and practice"; "Slopegraphs for comparing gradients"; "Taking logarithms in statistical data" `[V]`.

**Perception and charts**
- Cleveland & McGill, "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods", JASA 79(387), 531-554, 1984, doi:10.1080/01621459.1984.10478080 `[V]`.
- Cleveland, "Graphical Methods for Data Presentation: Full Scale Breaks, Dot Charts, and Multibased Logging", *The American Statistician* 38(4), 270-280, 1984 `[V*]`.
- Cleveland, *The Elements of Graphing Data*, 1985/1994 `[V* exists; passages unverified]` (recommended purchase).
- Cleveland, McGill & McGill, "The Shape Parameter of a Two-Variable Graph", JASA 83, 289-300, 1988 `[V]`.
- Heer & Bostock, "Crowdsourcing Graphical Perception: Using Mechanical Turk to Assess Visualization Design", CHI 2010 `[V]`.
- Heer & Agrawala, "Multi-Scale Banking to 45 Degrees", IEEE TVCG 12(5), 2006 `[V]`.
- Talbot, Gerth & Hanrahan, "Arc Length-Based Aspect Ratio Selection", IEEE InfoVis 2011 `[V]`.
- Skau & Kosara, "Arcs, Angles, or Areas: Individual Data Encodings in Pie and Donut Charts", EuroVis 2016 `[V]`.
- Correll, Bertini & Franconeri, "Truncating the Y-Axis: Threat or Menace?", CHI 2020 `[V]`.
- Isenberg, Bezerianos, Dragicevic & Fekete, "A Study on Dual-Scale Data Charts", IEEE TVCG 17(12), 2011 `[V]`. Studies two data resolutions on one axis (magnified focus plus condensed context), not two y-axes for different measures. Do not cite it for A7. Useful if a rule on scale breaks is added: cut-out charts with collocated full context performed best; superimposed focus and context should be avoided.
- Robertson, Fernandez, Fisher, Lee & Stasko, "Effectiveness of Animation in Trend Visualization", IEEE TVCG 14(6), 1325-1332, 2008 `[V]`.

**Words, titles, memory**
- Kim, Setlur & Agrawala, "Towards Understanding How Readers Integrate Charts and Captions: A Case Study with Line Charts", CHI 2021 `[V]`.
- Kong, Liu & Karahalios, "Frames and Slants in Titles of Visualizations on Controversial Topics", CHI 2018 `[V]`.
- Bateman et al., "Useful Junk? The Effects of Visual Embellishment on Comprehension and Memorability of Charts", CHI 2010 `[V]`.
- Borkin et al., "What Makes a Visualization Memorable?", IEEE TVCG 2013; "Beyond Memorability: Visualization Recognition and Recall", IEEE TVCG 2016 `[V]`.
- Inbar, Tractinsky & Meyer, "Minimalism in Information Visualization: Attitudes towards Maximizing the Data-Ink Ratio", ECCE 2007, London, pp. 185-188 `[V*]`.

**Dashboards**
- Few, *Information Dashboard Design*, 2nd ed., 2013 `[V* via reviews]` (recommended purchase).
- Few, "Common Pitfalls in Dashboard Design", Perceptual Edge white paper, 2006 (13 pitfalls) `[V]`.
- Few, "Bullet Graph Design Specification", Perceptual Edge, rev. 2013 `[V*]`.
- Few, "Dual-Scaled Axes in Graphs: Are They Ever the Best Solution?", Visual Business Intelligence Newsletter, March 2008 `[V*]`.
- Few, *Show Me the Numbers* `[K]`.
- Wheeler, *Understanding Variation: The Key to Managing Chaos*, 1993 (2nd ed. 2000) `[V*]`.
- Brath, Hagerman & Sorenson, "Why Two Y-Axes?", IV 2020 presentation `[V* exists]`.
- Microsoft Learn, Power BI docs: combo charts, small multiples, line charts, Format pane General tab `[V]`. Microsoft, powerbi-visuals-bulletchart (GitHub) `[V]`.

**Color and accessibility**
- Harrower & Brewer, "ColorBrewer.org: An Online Tool for Selecting Colour Schemes for Maps", *The Cartographic Journal* 40(1), 27-37, 2003, doi:10.1179/000870403235002042 `[V*]`.
- Borland & Taylor, "Rainbow Color Map (Still) Considered Harmful", IEEE CG&A 27(2), 2007 `[V]`.
- Ware, Stone & Szafir, "Rainbow Colormaps Are Not All Bad", IEEE CG&A 43(3), 88-93, 2023, doi:10.1109/MCG.2023.3246111 `[V]`.
- Reda, "Rainbow Colormaps: What are they good and bad for?", IEEE TVCG `[V* exists]`.
- W3C, WCAG 2.2, SC 1.4.1 Use of Color (A), 1.4.3 Contrast (Minimum) (AA), 1.4.11 Non-text Contrast (AA), and Understanding 1.4.11 `[V]`.

**Frameworks**
- Munzner, *Visualization Analysis & Design*, CRC Press, 2014 `[V*]` (recommended purchase).
- Shneiderman, "The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations", IEEE Symposium on Visual Languages, 336-343, 1996, doi:10.1109/VL.1996.545307 `[V]`.

**Prior art**
- aref-vc/tufte-claude-skill (GitHub, MIT): a chart-creation skill distilling ten principles from three Tufte books. This rulebook differs by being a cited critic for dashboards, drawing on Few and the empirical literature, naming LLM defaults, and covering Power BI.
