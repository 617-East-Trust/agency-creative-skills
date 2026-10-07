# Data contracts and reproducibility

## Performance export

Use a UTF-8 CSV/TSV with a header. The analyzer accepts case-insensitive aliases and **fails** on invalid ISO dates; missing, negative, or non-finite `clicks`/`impressions`; and invalid supplied positions. It never silently turns a missing metric into zero.

| Field | Required by | Notes |
| --- | --- | --- |
| `date` | freshness, period comparison, decay | ISO `YYYY-MM-DD`; absent dates make period validation unverified (or fail with `--strict`) |
| `query` | query, CTR, brand, cannibalization, new-keyword routines | Detailed query exports may omit anonymized terms |
| `page` | page, CTR, cannibalization routines | Preserve source URL by default; use `--normalize-urls safe` only when intentionally merging safe variants |
| `clicks` | all performance routines | Required, finite, non-negative |
| `impressions` | all performance routines | Required, finite, non-negative |
| `position` | position-aware CTR and diagnosis | Optional; blank positions are excluded from position-normalized CTR screening |
| `country`, `device`, `search_type` | compatible filtering/comparison | Preserve in metadata; passing a filter requires its matching column |

A `date × query × page` export is strongest for analysis. A query-only or page-only export is valid for a limited report but cannot reliably detect query/page cannibalization. In strict mode the analyzer rejects mixed blank/populated dimension columns and duplicate dimension rows.

## Analyzer context flags

| Flag | Purpose |
| --- | --- |
| `--property sc-domain:example.com` | Binds output to a named property; omitted property is a warning or strict-mode failure |
| `--as-of-date YYYY-MM-DD` | Makes freshness filtering reproducible; default is the local current date |
| `--freshness-days 3` | Excludes dated rows newer than `as-of − 3 days`; pass `0` only when the export is known complete |
| `--country`, `--device`, `--search-type` | Applies an explicit dimension filter and carries it into metadata |
| `--normalize-urls safe` | Lowercases scheme/host, removes a non-root trailing slash/default port, preserves path case and query string |
| `--strict` | Fails on missing property/date context, mixed aggregation grain, and duplicate dimension rows |

## Totals and coverage

`export_totals` means **the sum of rows supplied to the script**. It is not necessarily a property-level GSC KPI: detailed query/page rows can omit anonymized data or be truncated/aggregated differently. Reports must distinguish:

```text
export_totals: calculated from supplied rows
property_totals: separately supplied authoritative property-level data, or null
aggregation_type: date × query × page …
query_coverage: partial_or_unknown / not_supplied
known_truncation: source/export limitation statement
```

Do not synthesize `property_totals`. For authoritative property KPIs, acquire a separate property-level export/API response with its own scope record.

## Period design

| Use case | Default windows | Enforcement |
| --- | --- | --- |
| Weekly health / drops | latest 28 complete days vs preceding 28 | Equal, non-overlapping dated windows are required when dates exist |
| Content decay | recent 90 complete days vs preceding 90 | `decay` requires two 90-day windows by default; output is a candidate screen, not causal proof |
| Emerging terms | latest 28 complete days vs preceding 28 | Minimum evidence thresholds are explicit |
| Monthly report | calendar month vs prior month; YoY when possible | Preserve filters and day counts for the primary comparison |

Keep device/country/search type identical across windows. Search Console dates have their own reporting timezone; do not mix them with GA4 dates without disclosing it. When dates are absent, use explicit metadata or label the result `unvalidated`; strict mode fails.

## URL Inspection export

For indexing diagnosis, provide authorized API output or a CSV with one row per URL. Useful columns include:

```text
url,verdict,coverage_state,indexing_state,robots_txt_state,page_fetch_state,
last_crawl_time,google_canonical,user_canonical,sitemap,referring_urls
```

Inspection is point-in-time and scoped to a Google-selected canonical; it does not replace live HTTP/source checks. That live evidence belongs to Technical Website Soundness.

## Sitemap and crawl inputs

- Provide local sitemap XML/index files. `scripts/sitemap_audit.py` returns `PASS`, `FAIL`, or `INCOMPLETE`; use `--strict` to fail the command unless it is `PASS`.
- An index is `INCOMPLETE` until its referenced child sitemaps are also supplied/audited locally. The tool never fetches them silently.
- Pass `--expected-host` to expose host mismatches. No inspection CSV yields explicit `unknown` inspection evidence.
- For redirect, status, canonical, robots, and content proof, obtain a crawl export or Technical Website Soundness evidence. Crawl data is a snapshot.

## Reproducibility record

Include this block in every report:

```text
Property: sc-domain:example.com
Scope: Web search · United States · MOBILE
Source: GSC detailed export (date × query × page); URL Inspection export
Windows: 2026-08-31–2026-09-27 vs 2026-08-03–2026-08-30
Freshness: as-of 2026-10-01; last 3 calendar days excluded
Aggregation: export totals only; property totals not supplied
Rows: 14,281 current / 13,947 baseline after validation and filters
Known limitations: query anonymization; detailed-export truncation unknown; inspection sampled 20 URLs
```
