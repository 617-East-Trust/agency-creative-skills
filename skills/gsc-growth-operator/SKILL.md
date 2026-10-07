---
name: gsc-growth-operator
description: >-
  Operate Google Search Console as an evidence-led organic-growth and indexation
  system. Use for GSC performance exports or API data; ranking, CTR, traffic,
  content-decay, cannibalization, branded-demand, and new-keyword analysis;
  indexing or sitemap troubleshooting; technical/page/content audits; Core Web
  Vitals; GA4 AI-search attribution; and recurring SEO reports. Consolidates
  the distinct workflows catalogued at marketingskills.sh/tools/search-console.
---

# GSC Growth Operator

Turn Google Search Console, optional GA4/CrUX/PageSpeed/Ahrefs/Bing data, and the site itself into **prioritized, verifiable SEO actions**. Use this skill as one routing layer instead of treating every GSC symptom as a separate skill.

## Scope and guardrails

1. **Establish the property.** Record the GSC property, canonical host, device/country/search-type filters, timezone, and the latest complete date before analysis.
2. **Respect freshness.** Exclude the most recent 3 complete days by default; compare equal-length, non-overlapping windows. State the chosen windows.
3. **Do not invent data.** Label measurements by source: GSC export/API, GA4, URL Inspection, PageSpeed/CrUX, crawl, or estimate. Missing access is `not evaluated`, not healthy.
4. **Preserve drill-down.** Analyze site total → page/query → URL/technical evidence. Do not prescribe a title change from an aggregate alone.
5. **Fix causes before symptoms.** Resolve crawlability, `noindex`, canonical, server, and sitemap defects before CTR or content rewrites.
6. **Do not misuse Google’s Indexing API.** It is not a general-purpose indexing shortcut; use it only for eligible JobPosting or BroadcastEvent pages. Request-indexing or sitemap submission is an external change: show the exact URLs and reason before executing.
7. **Keep credentials outside artifacts.** Use an already-authorized connector/API client, or request a Search Console export. Never place tokens, cookies, or service-account keys in reports or scripts.

## Routing

| User need | Run | Output |
| --- | --- | --- |
| “How is organic search doing?” | `overview`, `compare`, `weekly` | KPI and movers dashboard |
| “Where can we get clicks quickly?” | `ctr-opportunities` | position-normalized CTR backlog |
| “Traffic/rankings fell” | `drops`, then `indexing` if broad | severity-ranked recovery queue |
| “What content needs updating?” | `content-decay`, `page-audit` | refresh versus consolidate plan |
| “Do pages compete?” | `cannibalization` | query/page conflict matrix |
| “What is new or growing?” | `new-keywords`, `topic-clusters` | expansion opportunities |
| “Is brand demand growing?” | `brand-split` | branded/non-branded trend |
| “Why isn’t this URL indexed?” | `indexing` | URL evidence record and remediation/recheck |
| “Check the sitemap” | `sitemap` + `indexing` | sitemap quality and coverage gaps |
| “Audit this page/site” | `page-audit` or `site-audit` | technical, content, CWV, schema actions |
| “Track AI search” | `ai-traffic` | GA4 measurement implementation |
| “Give me an SEO report” | `report` | decision-ready weekly/monthly report |

Read `references/operations.md` for each routine, thresholds, and decision rules. Read `references/indexing-playbook.md` whenever the request includes indexation, coverage, `noindex`, robots, canonicals, sitemap, crawled-but-not-indexed, or URL Inspection. Read `references/data-contracts.md` before using files. `references/catalog-coverage.md` shows how every catalog item is represented.

## Data acquisition

Prefer direct GSC API access through an already-authorized Google connector. Otherwise accept a Search Console Performance export or CSV with `date,query,page,clicks,impressions,ctr,position`; GSC tables with fewer dimensions are also valid. Use URL Inspection results and sitemap/robots/page-source evidence for indexation work. GA4, PageSpeed/CrUX, Ahrefs, Bing, and a site crawl are **optional enrichment**, never prerequisites.

Run the bundled analyzers for deterministic calculations:

```bash
python scripts/gsc_analyze.py overview --input performance.csv
python scripts/gsc_analyze.py ctr --input performance.csv --min-impressions 100
python scripts/gsc_analyze.py compare --current current.csv --baseline prior.csv
python scripts/gsc_analyze.py cannibalization --input performance.csv --min-pages 2
python scripts/gsc_analyze.py brand --input performance.csv --brand "Acme,Acme Inc"
python scripts/sitemap_audit.py --sitemap sitemap.xml --inspection inspection.csv
```

Do not infer URL-level indexing from performance rows; a URL with no impressions can be indexed. Query URL Inspection or provide an inspection export for a definitive status.

## Controller workflow

1. **Frame the decision.** Restate the business question, scope, property, timeframe, and decision owner. Ask only for a missing choice that materially changes analysis (for example, which property or brand terms).
2. **Pick the narrowest route.** Start with the requested routine. Escalate to a full audit only if evidence suggests cross-cutting causes.
3. **Validate data.** Verify columns, dates, duplicates, aggregation grain, and missing fields. Record freshness and limitations.
4. **Calculate before interpreting.** Use the script for summaries, period deltas, low-CTR candidates, drops, decay, new queries, brand segmentation, and cannibalization. Use direct API data only when it adds required dimensions or inspection evidence.
5. **Triangulate material findings.** For each material page/query, check position, impression trend, page intent, canonical/indexation state, and relevant on-page or technical evidence. For indexing, follow the dedicated playbook.
6. **Prioritize safely.** Classify P0–P3. Give each action an owner, expected signal, verification method, and rollback/guardrail where it can change crawl or index behavior.
7. **Deliver the decision artifact.** Use the matching template under `templates/`. Separate measured facts, diagnosis, recommendation, and assumptions.

## Indexing workflow (always evidence-led)

1. **Collect URL evidence:** final HTTP status and redirect chain, canonical, robots meta/X-Robots-Tag, robots.txt rule, rendered content, internal-link reachability, sitemap presence, and URL Inspection state.
2. **Classify the blocker:** user-declared canonical, Google-selected canonical, blocked by robots, excluded by `noindex`, redirect/error/soft-404, duplicate/alternate, discovered-or-crawled-not-indexed, or no confirmed blocker.
3. **Trace the cause to a controlled asset:** page template, CMS flag, redirect rule, robots deployment, sitemap generator, server behavior, or thin/duplicate content. Never change a setting based only on a coverage label.
4. **Recommend the smallest safe remediation:** correct accidental noindex/robots blocks, canonical mistakes, sitemap omissions, redirect/server failures, or genuine content/value duplication. Preserve intentionally excluded pages.
5. **Recheck after deployment:** fetch headers/source, validate sitemap/canonical/internal links, request fresh inspection after Google has recrawled, and report the before/after evidence. Do not promise an indexing date.

Use `templates/indexing-incident.md` for the output. The detailed matrix is in `references/indexing-playbook.md`.

## Outputs

Use the selected template, then include:

- **Executive call:** what changed, why it matters, and the decision required.
- **Evidence table:** source, period/scope, metric or observation, confidence, and limitation.
- **Prioritized backlog:** P0–P3, URL/query, action, owner, expected signal, verification, and any risk.
- **Measurement plan:** next comparison window and success/failure thresholds.

## Anti-patterns

- Comparing unequal periods, including immature GSC dates, or treating average position as a single-keyword rank.
- Declaring a URL “not indexed” from zero impressions, a crawl result, or `site:` alone.
- Mass title rewrites, canonical changes, robots edits, or sitemap submissions without URL-level evidence and rollback awareness.
- Treating `Discovered – currently not indexed` as a universal technical error; investigate quality, duplication, discovery, server/crawl demand, and internal linking.
- Calling every high-impression query a CTR opportunity without normalizing for position, SERP features, intent, and brand.
- Reporting a metric without its property, filter, window, source, and aggregation grain.
