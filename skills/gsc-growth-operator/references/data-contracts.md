# Data contracts and reproducibility

## Performance export

Use a UTF-8 CSV/TSV with a header. The analyzer accepts case-insensitive aliases and parses CTR values such as `0.032` or `3.2%`.

| Field | Required by | Notes |
| --- | --- | --- |
| `date` | period windowing, decay | ISO `YYYY-MM-DD`; use the GSC-reported date, not export time |
| `query` | query, CTR, brand, cannibalization, new-keyword routines | May be absent for page-only exports |
| `page` | page, CTR, cannibalization routines | Use canonical/landing-page URL as exported; do not silently merge URLs |
| `clicks` | all performance routines | Non-negative number |
| `impressions` | all performance routines | Non-negative number |
| `ctr` | optional | Recalculated as clicks/impressions after grouping when available |
| `position` | opportunity, drops, page/query diagnosis | Impression-weighted when grouped |
| `country`, `device`, `search_type` | optional segmenting | Export filter context if rows do not include these fields |

**Grain matters.** A `date × query × page` export is strongest for analysis. A query-only or page-only export is valid for a limited report but cannot reliably detect query/page cannibalization. The Search Console UI may omit anonymized queries and cap rows; disclose that limitation.

## Period design

| Use case | Default windows | Notes |
| --- | --- | --- |
| Weekly health | latest 28 complete days vs preceding 28 | Exclude the last 3 days by default |
| Ranking/traffic drop | latest 28 complete days vs preceding 28 | Confirm seasonality, releases, and data lag |
| Content decay | recent 90 complete days vs preceding 90 | Require repeated decline, not one weak week |
| Emerging terms | latest 28 complete days vs preceding 28 | Treat terms absent from baseline as new only within available export coverage |
| Monthly report | calendar month vs prior calendar month and YoY when possible | Use equal day counts for the primary comparison |

Keep device/country/search type identical across comparison windows. Search Console performance dates have their own reporting timezone; do not mix them with GA4 date ranges without disclosing the difference.

## URL Inspection export

For indexing diagnosis, provide direct API output or a CSV with one row per URL. Useful columns include:

```text
url,verdict,coverage_state,indexing_state,robots_txt_state,page_fetch_state,
last_crawl_time,google_canonical,user_canonical,sitemap,referring_urls
```

Column names vary by API/client. Preserve raw values in an appendix; normalize only for classification. Inspection is point-in-time and scoped to a Google-selected canonical, so it does not replace live HTTP/source checks.

## Sitemap and crawl inputs

- Provide a sitemap XML file or sitemap-index XML file. Use `scripts/sitemap_audit.py` for XML validity, duplicate locs, URL scheme/host anomalies, lastmod checks, and optional inspection cross-reference.
- For redirect, status, canonical, robots, and content checks, collect a crawl export with `url,final_url,status,robots,canonical,title,word_count,inlinks` when available.
- Crawl results are a snapshot. Validate deployment changes directly after release.

## Optional enrichment sources

| Source | Use | Never use it to replace |
| --- | --- | --- |
| GA4 | landing-page engagement/conversions, AI referral attribution | GSC query/click/impression truth |
| PageSpeed/CrUX | lab and field CWV evidence | URL Inspection index status |
| Ahrefs/Bing | backlink, competitor, Bing visibility context | Google-specific GSC metrics |
| Site analytics/CMS | conversion value, release dates, publication state | live HTTP/canonical/robots inspection |

## Reproducibility record

Include this block in every report:

```text
Property: sc-domain:example.com
Scope: Web search · United States · All devices
Source: GSC performance export (date × query × page), URL Inspection export
Windows: 2026-08-31–2026-09-27 vs 2026-08-03–2026-08-30
Freshness buffer: last 3 calendar days excluded
Rows: 14,281 current / 13,947 baseline
Known limitations: query anonymization; no conversion data; inspection sampled 20 URLs
```
