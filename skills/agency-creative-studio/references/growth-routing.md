# Growth routing — SEO / CRO / CTA / llms.txt

Condensed growth guidance for Agency Creative Studio. Prefer a dedicated SEO/CRO specialist skill when present; otherwise use this reference. Do not treat missing MCP tools as hard requirements.

## When to load this
- Engagement needs discoverability, conversion rate, CTA hierarchy, or agent-legibility work
- Landing page “not ranking” or “not converting” inside a broader agency engagement
- Marketing launch plumbing before Technical Website Soundness `go`

## Honesty bar
- Never invent rankings, traffic, or keyword volumes
- Fix crawl/index and CWV basics before creative A/B tests on a broken page
- **`llms.txt` is not a Google ranking factor.** It is a curated Markdown map for agents ([llmstxt.org](https://llmstxt.org/)). Do not sell it as a ranking hack.

## Sub-areas

| Sub | Use when |
| --- | --- |
| `seo` | Crawl/index, on-page, IA, schema, CWV-as-SEO |
| `cro` | Funnel/landing conversion |
| `cta` | Button/offer hierarchy and copy tests |
| `llms` | `/llms.txt`, markdown mirrors, agent readability |
| `full-growth` | End-to-end growth pass |

## A. Technical + on-page SEO (summary)

Pipeline: **Crawl → Render → Index → Signals**.

- `/robots.txt` at host root; don’t block CSS/JS or money pages; include `Sitemap:`
- XML sitemap = only 200, canonical, indexable URLs
- One canonical host + HTTPS; no redirect chains
- `noindex` via meta/X-Robots-Tag for thank-you/staging/faceted junk
- Real `<a href>` internals; avoid hash-router public content; prefer SSR/SSG for critical SEO content
- Unique title + H1; internal links to money pages
- JSON-LD matching **visible** content only
- Field p75 targets: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1
- AI crawlers: separate training vs answer bots intentionally; never block Googlebot by accident (e.g. Google-Extended ≠ Googlebot)

Deep headers/perf/security → **Technical Website Soundness**.

## B. CRO (LIFT-oriented)

One visitor type · one offer · one primary action.

Raise: value proposition, relevance, clarity, urgency. Cut: anxiety, distraction.

1. Message match (headline ↔ ad/email/query)  
2. Above-fold: what / who / outcome / primary CTA  
3. Proof near claims  
4. Benefits > features; cut form fields  
5. Objection handling  
6. Repeat the **same** primary CTA after proof and at bottom  
7. Test order: headline → value prop → CTA → proof → form/layout  
8. Don’t test copy on a broken/slow page  

## C. CTAs

Formula: `[Action verb] + [specific outcome]`  
Strong: `Get my free audit`, `Book a 15-min intro` · Weak: `Submit`, `Learn more`

- One primary (filled, high contrast); secondary ghost/link only  
- Microcopy for time/cost/risk reversal  
- ≥44×44px targets; same primary label across the landing page  

## D. llms.txt

| File | Role |
| --- | --- |
| `robots.txt` | Crawl allow/disallow |
| `sitemap.xml` | Full indexable URL list |
| `llms.txt` | Curated “read this first” map — grants nothing; **not a Google ranking factor** |

Format: `#` H1 → optional `>` summary → `##` sections with `- [Name](url): notes` → optional `## Optional`.

Ship ~10–20 hand-curated links (services, work, process, pricing, contact, brand) — not a sitemap dump. Optional: `.md` mirrors; `rel="alternate" type="text/markdown"`.

## Growth output format

1. Snapshot (discoverability + convertibility)  
2. Scorecard 1–5 or N/E: Technical SEO, On-page/IA, CRO, CTA clarity, Agent legibility  
3. P0/P1/P2 actions with evidence, fix, effort  
4. Artifacts: robots/sitemap diffs, title/H1 map, CTA matrix, `/llms.txt` draft, schema  
5. Test backlog (hypothesis + metric)  
6. Handoffs: copy, design/motion, Technical Website Soundness, Premium Report Craft  

## Anti-patterns
- llms.txt as a Google hack  
- Ranking advice without crawl/index basics  
- Five competing CTAs  
- CRO that trashes LCP (autoplay, unbudgeted 3D above the fold)  
- Invented traffic/keyword metrics
