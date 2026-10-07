# Indexing diagnostics playbook

## Incident triage

Use this route whenever a user asks why a URL/page set is not indexed, disappears from search, is excluded, has a coverage issue, or is absent from the sitemap. Treat the GSC label as a **lead**, not the root cause.

1. Confirm the exact URL, desired canonical, business intent, whether it should be indexable, and whether the issue is isolated or systemic.
2. Record live evidence: response and final redirect target; `X-Robots-Tag`; meta robots in raw/rendered HTML; canonical; robots.txt applicability; content/soft-404 signs; and sitemap/internal-link presence.
3. Obtain the latest URL Inspection result. Record the indexed version’s Google canonical, user canonical, last crawl time, fetch/robots states, and coverage/exclusion wording.
4. Compare a small cohort: one affected URL, one healthy peer from the same template, and one intended canonical. This distinguishes template/deployment faults from page-quality or duplication cases.
5. Trace the condition to an owned control (CMS field, template, CDN/header rule, redirect/canonical rule, robots deployment, sitemap build, content policy) and formulate the smallest reversible repair.

## Classification and response matrix

| Evidence / GSC state | Verify | Likely control | Safe response | Recheck |
| --- | --- | --- | --- | --- |
| `noindex` or X-Robots-Tag | HTML and response headers; intended page role | CMS setting, template, CDN/server header | Remove only accidental `noindex`; retain it for low-value/private/staging pages | live header/source → fresh inspection after recrawl |
| Blocked by robots.txt | exact user-agent rule, path, response and intended indexability | robots deployment/generator | Allow the intended crawl path; do not use robots to solve duplicate control | robots test + fetch + inspection |
| Alternate page / Google chose different canonical | content similarity, all canonical declarations, redirects, sitemap and internal links | canonical template, URL parameter/case policy, redirects | Consolidate signals around one canonical or deliberately differentiate content | crawl canonical cluster + inspection |
| Duplicate without user-selected canonical | duplicate cluster, HTTP/HTTPS/www variants, sort/filter paths | canonical/redirect policy, faceted-navigation rules | Canonicalize or control duplicate generation; avoid mass-indexing filter pages | recrawl cluster and verify selected canonical |
| Redirect / 4xx / 5xx | redirect chain, target intent, server logs if available | route/server/CDN rule | Repair server behavior; use a single permanent redirect only if the content moved | live response + sitemap/internal links |
| Soft 404 | page value, template payload, status, overlap | CMS/template/content | Restore substantial unique content or intentionally return/redirect to the correct replacement | live page + inspection after recrawl |
| Crawled – currently not indexed | canonical/robots/server clean; content quality, duplication, internal links, crawl demand | content and internal-link strategy; site quality | Improve unique utility, remove near-duplicates, strengthen relevant links; do not blindly submit repeatedly | observe crawl/index change over a later comparison window |
| Discovered – currently not indexed | sitemap, internal linking, URL volume, server health/crawl demand | sitemap/link architecture, server responsiveness, quality | Ensure desired URLs are discoverable and valuable; fix scale/quality blockers before requesting indexing | crawl/sitemap validation + later inspection |
| Sitemap status mismatch | sitemap XML, URL eligibility, lastmod, property/host, canonical | sitemap generator/build | Include only canonical 200-indexable URLs; remove redirects/noindex/duplicates | resubmit if needed; monitor sitemap report |
| Indexing API request considered | page type and Google policy eligibility | publishing flow | Use only eligible JobPosting/BroadcastEvent URLs; otherwise use normal discovery/crawl mechanisms | API response + later inspection, never a promised index date |

## Controlled remediation sequence

1. Save the before-state (headers, source snippets, inspection fields, sitemap/crawl row, timestamp).
2. Make one coherent, reversible change. Do not mix robots, canonical, content, and URL migration changes unless the root cause requires them.
3. Verify production directly: final status, canonical, robots header/meta, internal links, and sitemap entry.
4. If the user authorizes an external request/submission, show the exact URLs and submitted sitemap first; record the action and outcome.
5. Wait for recrawl/reprocessing. Re-inspect; state the date and result without claiming a guaranteed outcome.

## Never infer or promise

- A `site:` query is not an authoritative coverage test.
- An unindexed URL is not necessarily blocked or penalized.
- Sitemaps invite discovery; they do not guarantee crawling or indexing.
- Request Indexing and the Indexing API do not ensure inclusion.
- Removing a `noindex` or robots block is a production behavior change; do not apply it to staging, private, legal, search-result, or intentionally excluded pages without intent confirmation.

## Evidence record

| Field | Requirement |
| --- | --- |
| URL and intended canonical | Exact values |
| Desired outcome | Index, remain excluded, consolidate, redirect, retire |
| Observed state | GSC Inspection + live HTTP/source/crawl evidence |
| Diagnosis | Evidence-supported, with confidence |
| Root control | CMS/template/configuration/redirect/sitemap/content owner |
| Change | Smallest safe remediation and rollback |
| Verification | Exact post-release and post-recrawl checks |
| Status | Open, deployed, pending recrawl, confirmed, intentionally excluded |
