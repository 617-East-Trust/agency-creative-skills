---
name: agency-creative-studio
description: >-
  Orchestrate complex, multi-disciplinary agency engagements that combine brand
  direction, marketing-site experience, conversion strategy, launch readiness,
  and client-facing delivery. Use when the request needs a joined-up creative
  brief, specialist routing, and integrated QA across two or more disciplines.
  Do not use for a standalone report, technical audit, SEO/CRO task, single
  component, isolated copy edit, or one-off motion/3D implementation.
---

# Agency Creative Studio

Orchestrate complex agency engagements. Own the brief, routing, and integration QA — not every specialist procedure. Do not run the full pipeline for a narrow ask.

## Paths (pick one)

| Path | Trigger | Outcome |
| --- | --- | --- |
| `review-existing` | Live URL / brand pack teardown | Structured creative audit + redesign brief |
| `new-build` | New site, landing, or brand experience | Direction → IA → specialist build → QA |
| `campaign` | Multi-asset launch or offer push | Brief → channel owners → integrated delivery |
| `launch-integration` | Pre-ship multi-discipline go/no-go | Coordination + tech/growth/report handoffs |

State path and reason only when it helps for a substantial engagement.

## Shared engagement brief

Require only when **two or more disciplines**, a **client/board deliverable**, or a **launch decision** is involved:

```markdown
# Engagement brief
## Decision and success
- Decision/action sought:
- Audience and priority user:
- Business objective:
- Success metric and baseline (if known):
## Scope
- In scope / Explicitly out of scope:
- Required deliverables and formats:
- Deadline / review constraints:
## Evidence and constraints
- Verified source material:
- Unknowns and assumptions:
- Brand, a11y, legal, technical, performance constraints:
## Ownership
- Primary specialist / Supporting / Final approver:
```

## Routing contract

| Discipline | Owner | Required input | Required output |
| --- | --- | --- | --- |
| Creative direction | Agency router / design specialist | Audience, offer, brand signals | One-page direction: tension, belief shift, visual system, section narrative |
| Conversion copy | Copy specialist (when present) | Offer, evidence, desired action | Message hierarchy + CTA matrix |
| GSC growth and indexation | **GSC Growth Operator** | GSC export/API data, URL Inspection, sitemap/coverage context | Evidence-backed performance or indexing backlog; handoff request for live technical proof |
| CRO and on-page growth | SEO/CRO specialist when present; else `references/growth-routing.md` | Offer, intent, analytics if any | Prioritized CTA, messaging, metadata, or schema backlog |
| Technical readiness | **Technical Website Soundness** | URLs/repo/deploy + staging status | Evidence-backed findings or acceptance checklist |
| Client report/deck | **Premium Report Craft** | Decision, evidence, format, brand | Decision-ready report/deck + source ledger |

Hand off when a specialist skill or tooling is present. Do not invent missing MCP/tool dependencies as hard requirements.

## Workflow

1. **Discovery** — goal, audience, offer, constraints, existing assets/URLs  
2. **Creative direction** — one justified aesthetic; reject unjustified generic patterns, not legitimate type, color, or layout choices that suit the brief
3. **Scope / IA** — section map, journeys, deliverable list  
4. **Specialist execution** — route per contract; keep brief as source of truth  
5. **Integrated QA** — checklist below  
6. **Delivery** — artifacts + open assumptions; report via Premium Report Craft when client-facing

**Gate:** require direction approval only when an unapproved direction would waste significant build. Otherwise proceed with assumptions listed in the brief.

## Progressive disclosure

Load references only when needed:

- Full pipeline / stages & gates → `references/engagement-workflow.md`
- Creative teardown → `references/creative-review-rubric.md`
- CRO/CTA/llms.txt questions → `references/growth-routing.md` (or specialist)
- Brand, design-system, motion/3D, or conversion-measurement implementation handoffs → `references/implementation-handoffs.md`
- Search Console performance, URL Inspection, coverage, or sitemap questions → **GSC Growth Operator**

**Growth (short):** Route Search Console property data, URL Inspection, coverage, and sitemap-to-inspection work to **GSC Growth Operator**. Route live headers, robots/canonical verification, PageSpeed/CrUX collection, deploy/rollback, and launch evidence to **Technical Website Soundness**. Keep `llms.txt` honest: curated agent map, **not a Google ranking factor**.

## Review (`review-existing`)

Distinctive agency procedure. Prefer live URL fetch, screenshots, or user assets.

**Passes:** Brand · IA/UX · Visual craft · Motion/immersive · Copy/CRO · Competitive (if comps)

**Output:** Snapshot → qualitative scorecard (strong / uneven / weak / N/E) → Top 5 fixes (impact × effort) → Evidence log → Redesign brief → Handoffs

Full rubric: `references/creative-review-rubric.md`.

## Hard rules

1. **Taste before templates.** Commit to one aesthetic.  
2. **Human voice.** Would a sharp human say this out loud to someone they respect?  
3. **No fake data.** Never invent metrics, rankings, or citations. Separate observed facts from judgment.  
4. **Performance & a11y.** Prefer `transform`/`opacity`; honor `prefers-reduced-motion`; degrade 3D on weak devices.  
5. **Router, not monolith.** Narrow asks stay with specialists; do not load unused procedures.

## Final integration QA

- [ ] Visual hierarchy clear in a 3-second skim  
- [ ] Accessible interactions (focus, contrast, tap targets, reduced motion)  
- [ ] Performance budget respected (LCP/INP/CLS awareness; no unbudgeted WebGL heroes)  
- [ ] Conversion clarity: one primary CTA, message match  
- [ ] Indexability and performance evidence handed to the correct GSC or technical owner
- [ ] Claims verified or labeled hypothesis  
- [ ] Deliverables match brief formats; open assumptions listed  

## Anti-patterns

- Activating this skill for a headline, one component, or standalone PDF/audit  
- Running all disciplines when the user asked for one  
- Duplicating GSC Growth Operator, Technical Website Soundness, or Premium Report Craft procedures
- Growth theater (llms.txt worship) without crawl/index/CTA basics  
- Skipping art direction into generic SaaS layout on a premium build
