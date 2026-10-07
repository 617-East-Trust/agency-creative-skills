# Sanitized end-to-end engagement example

## Brief

**Brief ID:** `ENG-EXAMPLE-001`
**Decision:** Approve a focused organic-growth release for a fictional services firm.
**Scope:** Homepage, pricing page, two service pages, and the organic-search operating report.

## Specialist sequence

1. **Agency Creative Studio** creates the shared brief and assigns GSC, technical, and reporting owners.
2. **GSC Growth Operator** analyzes a dated query × page export and URL Inspection sample. It creates finding `GSC-014`: pricing page clicks fell 34% versus an equal prior window; coverage evidence is inconclusive pending live canonical proof.
3. **Technical Website Soundness** receives a handoff for `GSC-014`, verifies a production canonical mismatch, records the before-state, proposes one template repair with rollback, and waits for explicit production approval.
4. After approval and deployment, Technical Website Soundness verifies the live canonical and GSC Growth Operator schedules a post-recrawl inspection check. No indexing date is promised.
5. **Premium Report Craft** receives the closed evidence ledger and converts it into a client report. If no renderer is available, the report says **“generated, not visually inspected”** rather than claiming visual QA passed.

## Shared handoff

```json
{
  "brief_id": "ENG-EXAMPLE-001",
  "from": "gsc-growth-operator",
  "to": "technical-website-soundness",
  "finding_ids": ["GSC-014"],
  "inputs": ["dated GSC export", "URL Inspection sample"],
  "limitations": ["No live header/canonical evidence collected by GSC workflow"],
  "requested_output": "Production canonical and redirect evidence, safe repair plan, and recheck result",
  "completion_criteria": ["final response/canonical recorded", "rollback documented", "finding state updated"]
}
```

The full contract is in `../contracts/artifact-schemas.json`; approval control is in `../contracts/approval-and-change-control.md`.
