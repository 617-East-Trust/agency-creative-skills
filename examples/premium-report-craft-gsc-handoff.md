# Premium Report Craft handoff — completed GSC analysis example

> **Illustrative only.** This handoff shows how a finished GSC analysis becomes a client-facing report without rerunning the analysis.

## Handoff

```json
{
  "brief_id": "ENG-EXAMPLE-022",
  "from": "gsc-growth-operator",
  "to": "premium-report-craft",
  "finding_ids": ["GSC-EXAMPLE-022", "GSC-EXAMPLE-023"],
  "inputs": ["finalized 28-day GSC comparison", "URL Inspection cohort", "approved finding ledger"],
  "limitations": ["Detailed query/page totals are not property totals", "Manual actions and security reports were not evaluated"],
  "requested_output": "Decision-ready monthly organic-search client report with evidence ledger and action backlog",
  "completion_criteria": ["No GSC or technical audit rerun", "Claims retain source/status caveats", "Decision and owner are explicit"]
}
```

## Inputs already verified by GSC Growth Operator

| Finding ID | Claim | Evidence status | Report treatment |
| --- | --- | --- | --- |
| GSC-EXAMPLE-022 | Property-level clicks increased in the finalized comparison window. | Verified | Use in KPI section with window/filter notes. |
| GSC-EXAMPLE-023 | A URL is discovered but not indexed. | Qualified | Present as an indexation finding with the Technical Website Soundness handoff and recheck condition. |

## Premium Report Craft scope

1. Build the report’s thesis, action-oriented hierarchy, and evidence ledger from the verified inputs.
2. Preserve the original finding IDs, source dates, confidence, limitations, owners, and action-verification fields.
3. Separate verified measurement from hypotheses and recommendations.
4. Do **not** rerun Search Analytics, URL Inspection, live technical checks, or produce a new root-cause claim.
5. If rendered as a PDF or deck, render and inspect the artifact; otherwise state that visual inspection was not performed.

## Example report decision

**Decision:** Approve one technical preflight for the indexation finding and one measured content/CTR experiment; monitor property-level KPIs in the next finalized 28-day window.

The reporting skill owns communication and hierarchy. GSC Growth Operator remains the authoritative owner of property data and indexation evidence.
