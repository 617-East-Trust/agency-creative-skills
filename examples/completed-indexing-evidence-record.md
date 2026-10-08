# Completed indexing evidence record — fictional example

> **Illustrative only.** This record demonstrates the handoff and verification shape; it is not evidence about a real property.

**Brief ID:** `ENG-EXAMPLE-021`

**Finding ID:** `GSC-EXAMPLE-021`

**Authoritative owner:** `gsc-growth-operator`

## Decision

**Desired outcome:** Consolidate a duplicate host to one indexable apex URL.

**Current recommendation:** Closed after Technical Website Soundness verified the production route and a later URL Inspection selected the apex canonical.

## Scope and evidence

| Field | Observation | Source / timestamp |
| --- | --- | --- |
| URL | `https://www.example.com/service-area/` | GSC URL Inspection · 2026-10-01 |
| Intended canonical | `https://example.com/service-area/` | Engagement brief · 2026-10-01 |
| URL Inspection coverage/verdict | Alternate page; Google selected `www` before remediation | URL Inspection · 2026-10-01 |
| Sitemap presence | Apex URL listed; `www` URL excluded | Sitemap audit · 2026-10-01 |
| Manual actions | Not evaluated; connector did not expose report | GSC capability record · 2026-10-01 |
| Security issues | Not evaluated; connector did not expose report | GSC capability record · 2026-10-01 |
| Links report | Not evaluated; connector did not expose report | GSC capability record · 2026-10-01 |

## Technical Website Soundness handoff

```json
{
  "brief_id": "ENG-EXAMPLE-021",
  "from": "gsc-growth-operator",
  "to": "technical-website-soundness",
  "finding_ids": ["GSC-EXAMPLE-021"],
  "inputs": ["URL Inspection result", "sitemap audit", "canonical-host comparison"],
  "limitations": ["No live redirect/header evidence collected by the GSC workflow"],
  "requested_output": "Exact redirect and canonical proof, rollback-ready implementation plan, and immediate verification result",
  "completion_criteria": ["Apex final route recorded", "Rollback documented", "Finding status updated"]
}
```

## Controlled remediation and closure

| Step | Owner | Evidence / result |
| ---: | --- | --- |
| 1 | Technical Website Soundness | Captured redirect matrix, headers, canonicals, form-path smoke test, and prior configuration revision. |
| 2 | Human approver | Approved one path/query-preserving `www` → apex redirect plan with a revert revision. |
| 3 | Approved deployment adapter | Deployed one focused routing change; immediate verification confirmed a one-hop apex final URL and self-referential canonical. |
| 4 | GSC Growth Operator | Later URL Inspection selected the apex canonical. The record closed without claiming a specific crawl/indexing guarantee. |

**Final status:** Confirmed canonical consolidation; ongoing performance monitoring remains separate from this indexation record.
