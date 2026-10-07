# Marketingskills Search Console catalog coverage

This skill **adapts the distinct capabilities** in the catalog at `https://www.marketingskills.sh/tools/search-console` into a single router and does not copy third-party skill text or code. Duplicates are intentionally consolidated. The matrix below confirms coverage of all 42 catalog entries observed on 2026-10-07.

| # | Catalog capability | Unified route |
| ---: | --- | --- |
| 1 | Google SEO APIs: GSC, PageSpeed, CrUX, Indexing API, GA4 | data acquisition; CWV; indexing guardrails |
| 2 | GSC + GA4 weekly digest | weekly report; GA4 enrichment |
| 3 | SEO reports with Ahrefs and GSC | report; optional enrichment |
| 4 | Live Ahrefs + GSC comprehensive site audit | site audit; optional enrichment |
| 5 | XML sitemap + index validation | sitemap; indexing |
| 6 | High-impression, low-CTR keywords | CTR opportunities |
| 7 | 90-day content decay | content decay |
| 8 | XML sitemap + index validation | sitemap; indexing |
| 9 | Ahrefs + GSC comprehensive audit | site audit; optional enrichment |
| 10 | 90-day content decay | content decay |
| 11 | GSC performance, indexing, CWV and SEO fixes | overview; indexing; CWV; page/site audit |
| 12 | Local-business GSC performance and quick wins | overview; CTR; local SEO |
| 13 | Blog performance: PageSpeed, CrUX, GSC, GA4, Keyword Planner, NLP | page/site audit; CWV; optional enrichment |
| 14 | Technical/on-page/content SEO audit | site audit |
| 15 | GSC performance, indexing, CWV, CTR, cannibalization | overview; indexing; CWV; CTR; cannibalization |
| 16 | SEO operations, keyword research, competitor gaps, trends | operations; new keywords; optional enrichment |
| 17 | 28-day ranking/traffic drops | drops |
| 18 | E-E-A-T, readability, AI citation readiness | content quality and AI-search readiness |
| 19 | High-impression, low-CTR keywords | CTR opportunities |
| 20 | Branded vs non-branded traffic | brand split |
| 21 | Period-over-period performance | compare |
| 22 | Indexing/coverage: robots, noindex, crawl errors | indexing |
| 23 | Keyword cannibalization | cannibalization |
| 24 | Period-over-period performance | compare |
| 25 | Ranking and traffic drops | drops |
| 26 | URL Inspection indexing diagnosis | indexing |
| 27 | Indexing status and lag detection | indexing; sitemap |
| 28 | Fix/control indexation and Indexing API | indexing guardrails; controlled remediation |
| 29 | Newly ranking keywords and topic clusters | new keywords; topic clusters |
| 30 | Single-page SEO with Ahrefs/GSC overlay | page audit; optional enrichment |
| 31 | Branded vs non-branded traffic | brand split |
| 32 | 28-day GSC dashboard | overview |
| 33 | Single-page SEO with Ahrefs/GSC overlay | page audit; optional enrichment |
| 34 | Newly ranking keywords | new keywords |
| 35 | Schema implementation/debug/validation | schema |
| 36 | GA4/GSC AI-driven traffic tracking | GA4 and AI traffic |
| 37 | Full technical/content SEO audit with GSC and Bing | site audit; optional enrichment |
| 38 | Keyword cannibalization | cannibalization |
| 39 | GSC performance overview dashboard | overview |
| 40 | SEO reports with domain, keyword, backlinks, traffic | report; optional enrichment |
| 41 | Monitor rankings, clicks, impressions, CTR | weekly monitoring |
| 42 | Universal SEO audit/orchestrator | controller workflow; site audit |

## Capability grouping

- **Performance intelligence:** overview, compare, drops, CTR, content decay, new queries, brand, cannibalization
- **Indexation intelligence:** URL Inspection, live URL controls, sitemap and coverage, lag/rechecks
- **Page/site quality:** technical/on-page/content audit, schema, CWV, E-E-A-T, local patterns
- **Measurement and operations:** GA4/AI attribution, weekly/monthly reports, optional third-party enrichment

The unified route deliberately keeps source-specific API credentials and vendor-dependent features optional. A GSC CSV export plus live public-site evidence is sufficient for the core performance and indexation workflows.
