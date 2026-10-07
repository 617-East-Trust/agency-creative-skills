# Growth routing — CRO, CTA, and specialist handoffs

Keep Agency Creative Studio a router. Use this reference for **CRO, CTA hierarchy, and agent legibility** only; do not reproduce Search Console or live technical audit procedures.

## Routing boundary

| Question / evidence | Owner | Output |
| --- | --- | --- |
| GSC query/page performance, CTR, drops, decay, cannibalization, brand demand, URL Inspection, coverage, sitemap-to-inspection correlation | **GSC Growth Operator** | Evidence-led growth or indexation backlog |
| Live HTTP headers, robots/canonical behavior, redirects, rendering, PageSpeed/CrUX collection, security headers, deploy/rollback, launch go/no-go | **Technical Website Soundness** | Production-surface evidence and safe implementation/recheck |
| Client-facing narrative of either analysis | **Premium Report Craft** | Decision-ready report/deck, without rerunning source analysis |
| Conversion friction, offer, CTA hierarchy, and copy test hypotheses | This reference or a CRO/copy specialist | Prioritized conversion backlog |

A “not indexed” prompt starts with **GSC Growth Operator** when GSC/URL Inspection evidence is requested or available. It requests Technical Website Soundness only for live production verification or remediation. A “slow page” prompt starts with **Technical Website Soundness**; GSC may supply impact context but does not collect CWV evidence.

## When to load this

- An Agency Creative Studio engagement needs conversion design, CTA hierarchy, or agent-legibility work.
- A landing page needs message-match or form/offer diagnosis after technical/indexation blockers are assigned to their owners.
- A client needs a joined-up launch brief; specialist output is already available or explicitly queued.

## Honesty bar

- Never invent rankings, traffic, keyword volume, CWV, or conversion metrics.
- Do not run copy tests on a broken, slow, or unindexable page.
- **`llms.txt` is not a Google ranking factor.** It is a curated Markdown map for agents ([llmstxt.org](https://llmstxt.org/)), not a substitute for crawl/index basics.

## CRO (LIFT-oriented)

One visitor type · one offer · one primary action.

Raise: value proposition, relevance, clarity, urgency. Cut: anxiety, distraction.

1. Message match (headline ↔ ad/email/query)
2. Above-fold: what / who / outcome / primary CTA
3. Proof near claims
4. Benefits over features; cut unnecessary form fields
5. Objection handling
6. Repeat the same primary CTA after proof and at the bottom
7. Test order: headline → value proposition → CTA → proof → form/layout
8. Hand off technical/page-speed defects before testing copy

## CTA

Formula: `[Action verb] + [specific outcome]`

Strong: `Get my free audit`, `Book a 15-min intro` · Weak: `Submit`, `Learn more`

- One primary (filled, high contrast); secondary ghost/link only
- Microcopy for time/cost/risk reversal
- ≥44×44px targets; same primary label across the landing page

## Agent legibility

| File | Role |
| --- | --- |
| `robots.txt` | Crawl allow/disallow; technical owner verifies behavior |
| `sitemap.xml` | Canonical indexable URL declaration; GSC/technical owners validate evidence |
| `llms.txt` | Curated “read this first” map; grants nothing and is not a Google ranking factor |

Ship roughly 10–20 hand-curated links (services, work, process, pricing, contact, brand)—not a sitemap dump. Optional: `.md` mirrors; `rel="alternate" type="text/markdown"`.

## Output format

1. Snapshot: conversion context and supplied evidence
2. P0–P3 conversion actions with hypothesis, owner, and metric
3. CTA matrix and message hierarchy
4. Explicit specialist handoffs for GSC, technical readiness, and client reporting

## Anti-patterns

- Treating `llms.txt` as a Google ranking tactic
- Reproducing URL Inspection, sitemap, canonical, or CWV procedures owned elsewhere
- Five competing CTAs
- CRO that degrades LCP with autoplay or unbudgeted 3D
- Invented traffic, keyword, or conversion metrics
