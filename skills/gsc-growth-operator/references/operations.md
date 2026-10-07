# Operations reference

## Common ranking and traffic routines

### Overview and weekly monitoring

Aggregate clicks, impressions, CTR, and impression-weighted position for the latest complete 28 days. Split page/query movers by absolute click change and percentage change. Explain whether the movement is demand (impressions), SERP/rank (position), CTR, page mix, or a data artifact. Add GA4 conversions only when the landing-page mapping and dates are compatible.

### Period comparison and drops

Compare equal windows. Surface pages and queries by lost clicks, lost impressions, position deterioration, and CTR change. Label a drop **critical** only after excluding freshness, seasonality, page removals/migrations, country/device changes, and property/filter mismatches. If losses spread across many URLs or templates, route to indexing/technical checks before rewriting content.

### Low-CTR opportunities

Require meaningful impressions and position context. Segment at minimum into positions `1–3`, `4–10`, and `11–20`. Prioritize pages where stable/rising impressions plus a material CTR gap coexist with relevant intent and an indexable, healthy canonical. Check titles, snippet eligibility, page intent, SERP features, and brand effects before recommending a rewrite. Do not promise a CTR uplift.

### Content decay

Use recent 90 complete days vs preceding 90. Prioritize recurring losses in clicks/impressions after accounting for seasonality and intentional changes. Separate: refresh (still aligned intent), consolidate (near-duplicate/cannibalizing), redirect/retire (obsolete), and technical fix (indexation/template/release issue). Assign severity using absolute lost clicks, trend consistency, conversion value if supplied, and recovery feasibility.

### New keywords and topic clusters

Compare current against baseline query coverage. Find newly visible terms and strong improvers, then group semantically only after checking page intent and current ranking URL. Propose expansion when the site lacks a suitable page; improve an existing page when a clear URL already owns the intent. Preserve one primary intent/theme per target URL.

### Cannibalization

Use query × page data. Flag a query only when two or more pages earn material impressions/clicks over the same period, then inspect whether overlap is genuine intent conflict versus deliberate SERP diversity. Recommend one of: consolidate, canonical/redirect, differentiate intent, internal-link hierarchy, or leave as-is. Never merge pages merely because they share a term.

### Brand split

Use user-confirmed brand terms, common variants, products, and misspellings. Put queries into branded, non-branded, ambiguous, and excluded buckets; expose the regex/list. Report clicks, impressions, CTR, and position over time. Do not silently classify competitor or generic terms as brand.

## Technical and indexing routines

### Indexing and coverage

Follow `indexing-playbook.md`. Sample problem URLs across affected templates and statuses. Use URL Inspection for authoritative Google-side signals; live checks for current production behavior. For broad coverage changes, compare sitemap URLs, crawl results, live indexability, and property selection.

### Sitemap audit

Validate sitemap XML/index structure, parseable URL locations, duplicates, HTTP/HTTPS or host inconsistencies, future/invalid `lastmod`, and only intended canonical 200 indexable URLs. Cross-reference inspection/crawl inputs when provided. A sitemap is a declaration of indexable canonical URLs, not a catalog of every route.

### Page and site audits

For a target URL, inspect final status/redirects, title/meta/headings, canonical, robots, content/intent, schema, internal links, images, CWV evidence, and optional GSC performance. For a site audit, sample templates and integrate technical, on-page, content, link, indexation, and performance evidence. Give implementation location/owner and recheck instruction for each issue.

### Core Web Vitals

Clearly distinguish lab PageSpeed from CrUX field data. Route/page, device, test date, and metric must travel with every number. Address LCP, INP, CLS after resolving availability/indexation blockers. Never present a laboratory score as user experience.

### Schema

Validate that structured data represents content actually visible on the page and follows the page type. Use Organization/LocalBusiness where factual, Article/BlogPosting for editorial pages, Product/Offer for genuine product pages, and BreadcrumbList for navigational hierarchy. Never add FAQ or review markup simply to seek rich results.

## Growth and reporting routines

### E-E-A-T, content quality, and AI-search readiness

Assess demonstrated expertise, first-hand evidence, author/about context, sourcing, completeness for intent, readability, recency, and unique utility. Use ranking/performance data to identify candidate pages, not as proof of quality. Treat “AI readiness” as citation-friendly clarity and evidence; do not promise inclusion in any model or answer engine.

### Local SEO

Combine local GSC patterns with location pages, service-area intent, NAP consistency, local schema, Google Business Profile data only if supplied/authorized, and conversion evidence. Separate local pack/Maps issues from organic web indexing and ranking issues.

### GA4 and AI traffic

Create a transparent GA4 measurement plan for AI referrals: source/medium rules, a named channel grouping, landing-page reporting, and an annotation date. Preserve an `unclassified` bucket and test with real referrals. Do not claim that GSC exposes AI-search traffic; it remains Google web-search data.

### Report production

Use `templates/weekly-report.md` for operating cadence, `templates/site-audit.md` for an audit, and `templates/indexing-incident.md` for a URL/coverage issue. Make the executive summary a decision, not a metric dump. Save exports, inputs, and assumptions separately from published client reports.

## Prioritization rubric

| Priority | Use when | Example |
| --- | --- | --- |
| P0 | Verified sitewide or revenue-critical indexation/availability incident | Production pages receive accidental sitewide `noindex` |
| P1 | Verified issue materially suppressing a valuable page/template or urgent decline | Canonical template points money pages elsewhere |
| P2 | Evidence-backed growth or quality work | High-impression page with confirmed intent/CTR gap |
| P3 | Measured experiment or investigation | Emerging topic merits a pilot brief |

Prioritize with impact, confidence, effort, risk, and reversibility—not an opaque score. State conversion/revenue assumptions separately when they are not measured.
