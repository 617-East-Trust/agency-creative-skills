# Marketingskills Search Console catalog map

This skill adapts the **intent** of the catalog at `https://www.marketingskills.sh/tools/search-console` into one router. It does not copy third-party text/code, and it does not claim that every catalog entry is a bundled executable. The observed catalog contains 42 entries; duplicates are intentionally grouped below.

| Catalog capability group | Unified route | Delivery mode |
| --- | --- | --- |
| GSC performance dashboard, weekly monitoring, period comparison | `overview`, `compare`, `weekly` | Local CSV analysis for export-level metrics; agent interpretation |
| Ranking/traffic drops | `drops` | Local candidate screen; agent diagnosis with release/seasonality/indexation evidence |
| 90-day content decay | `decay` | Local 90-vs-90 candidate screen; agent refresh/consolidation decision |
| High-impression / low-CTR | `ctr` | Local position-filtered screen; numeric click gap only with supplied benchmark |
| Newly ranking keywords / topic clusters | `new-keywords`, topic clustering | Local new-term screen; clustering is an agent procedure |
| Branded vs non-branded | `brand` | Local configurable brand/ambiguous/excluded split |
| Cannibalization | `cannibalization` | Local query × page candidate screen; agent intent review |
| URL Inspection, coverage, indexing lag, sitemap validation | `indexing`, `sitemap` | Local sitemap/inspection cross-reference plus authorized GSC/technical evidence |
| Fix/control indexation and Indexing API | `indexing` | Agent procedure with explicit approval; no general-purpose API submission client |
| Page/site/technical audit, schema, E-E-A-T, local SEO | `page-audit`, `site-audit` | Agent procedure; live technical proof → Technical Website Soundness |
| PageSpeed/CrUX, GA4 AI traffic, Ahrefs/Bing/Keyword Planner | enrichment | Optional authorized integration; no bundled fetch/config client |
| Reports | `report` | GSC analysis templates; client narrative → Premium Report Craft |
| Universal SEO orchestrator | controller workflow | Router and handoffs, not a 44-script clone |

## What the local code actually runs

| Script | Deterministic output | Not established by the script |
| --- | --- | --- |
| `gsc_analyze.py` | Validated export summaries, compare gainers/losers, decline/decay candidates, CTR screen, brand buckets, new terms, cannibalization | Property totals, indexation, complete query coverage, causal explanation, CWV, GA4, topic clusters |
| `sitemap_audit.py` | Local XML quality, duplicate/missing locations, host/lastmod checks, supplied inspection cross-reference | Live URL health, Google indexation, child-sitemap fetches, sitemap submission |

## Catalog governance

Treat third-party listings as **discovered**, not automatically reviewed or tested. Record source, revision, license, last review date, intended harness, and tested-harness result before recommending a dependency for client work.
