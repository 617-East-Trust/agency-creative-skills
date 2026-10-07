# Operations reference

## Evidence and ownership

- Use **GSC Growth Operator** for property data, query/page exports, URL Inspection, coverage, and sitemap-to-inspection correlation.
- Use **Technical Website Soundness** for live headers, robots/canonicals, redirects, rendering, PageSpeed/CrUX collection, deploy/rollback, and launch evidence.
- Use **Premium Report Craft** only after the analysis is complete and needs a client/board narrative.
- Maintain one finding ID, one remediation owner, and one authoritative evidence record. Follow the pack-level approval-and-change-control contract when installed; otherwise preserve its read-only-by-default, explicit-approval, before-state, rollback, and recheck steps.

## Common ranking and traffic routines

### Overview and weekly monitoring

Label sums from detailed rows as **export totals**, not property totals. Record property, filters, aggregation grain, date window, freshness treatment, query coverage, and known truncation. Split page/query movers by absolute and relative click change. Explain whether movement is demand (impressions), position, CTR, page mix, or a data limitation; do not claim causality from the table alone.

### Period comparison and drops

Compare equal, non-overlapping windows with compatible dimensions. Return gainers and losers separately. A drop candidate must have a real absolute/relative decline; then investigate freshness, seasonality, page removals/migrations, country/device changes, property/filter mismatch, and broad technical symptoms. A widespread loss may justify a GSC indexing route and a Technical Website Soundness handoff—never a blind rewrite.

### Low-CTR screening

Require meaningful impressions and known position. Segment at minimum into positions `1–3`, `4–10`, and `11–20`; exclude missing-position records from position-normalized analysis. Without a supplied benchmark, call the output a **screening list**, not an expected-CTR opportunity. Before changing snippets, check intent, SERP features, brand effects, page health/indexation, title, and on-page message match. Do not promise a CTR uplift.

### Content decay

Use two equal 90-day complete windows. The script produces **decay candidates**, not causal findings. Confirm repeated loss, seasonality, deliberate changes, page intent, conversion context, and indexation/technical state before choosing refresh, consolidate, redirect/retire, or technical remediation.

### New keywords and topic clusters

Compare current against baseline query coverage using explicit minimum evidence thresholds. An absent query can be anonymized or omitted, not truly new. Topic clustering is an agent procedure: inspect intent and current ranking URL before proposing a new page. Preserve one primary intent/theme per target URL.

### Cannibalization

Use query × page data. Flag a query only when two or more pages earn material impressions/clicks, then distinguish harmful intent conflict from deliberate SERP diversity. Recommend consolidate, canonical/redirect, differentiate intent, internal-link hierarchy, or leave as-is. Never merge pages merely because they share a term.

### Brand split

Use user-confirmed brand terms, variants, products, misspellings, plus explicit ambiguous and excluded lists. Report branded, non-branded, ambiguous, excluded, and unclassified metrics separately. Do not silently classify competitor or generic terms as brand.

## Indexation and technical routes

### Indexing and coverage

Follow `indexing-playbook.md`. Use URL Inspection for Google-side state and preserve the exact coverage/verdict/canonical fields. Request **Technical Website Soundness** for current live status, headers, robots, canonicals, redirects, rendering, and deployment remediation. Compare property selection, sitemap data, crawl evidence, and technical proof before assigning a root cause.

### Sitemap audit

Validate supplied XML/index structure, locations, duplicates, host inconsistencies, future/invalid `lastmod`, and supplied inspection cross-references. The local utility returns `PASS`, `FAIL`, or `INCOMPLETE`; it never fetches URLs. An index remains incomplete until all child sitemaps are supplied/audited. Technical Website Soundness verifies live canonical 200 indexability.

### Page/site audits, CWV, schema, and local SEO

Use GSC performance/Inspection data to prioritize pages. Combine it with supplied technical evidence, content/intent review, schema that matches visible content, local-service context, and internal linking. Technical Website Soundness collects PageSpeed/CrUX; carry source, route, device, test date, and lab/field status with every metric. Give each issue one owner and recheck instruction.

## Reporting and governance

### GA4 and AI traffic

Create a transparent measurement plan for AI referrals: source/medium rules, named channel grouping, landing-page reporting, annotation date, and an `unclassified` bucket. It requires an authorized GA4 implementation; GSC does not expose AI-search traffic.

### Search Console health

For manual actions, security issues, and links, use an authorized Console/connector view and record property, check date, and evidence state. If the integration does not expose a report, state `not evaluated`; do not infer a clean account from absence in an export.

### Report production

Use the GSC templates for operational analysis. Hand verified output to Premium Report Craft for a client report/deck/PDF; it must not rerun the GSC or technical audit. If rendering/visual inspection is unavailable, label the artifact `generated, not visually inspected`.

## Priority rubric

| Priority | Use when | Example |
| --- | --- | --- |
| P0 | Verified sitewide or revenue-critical indexation/availability incident | Production pages receive accidental sitewide `noindex` |
| P1 | Verified issue materially suppressing a valuable page/template or urgent decline | Canonical template points money pages elsewhere |
| P2 | Evidence-backed growth or quality work | Benchmark-backed CTR candidate with confirmed intent |
| P3 | Measured experiment or investigation | Emerging topic merits a pilot brief |

Prioritize with impact, confidence, effort, risk, and reversibility—not an opaque score. State conversion/revenue assumptions separately when they are not measured.
