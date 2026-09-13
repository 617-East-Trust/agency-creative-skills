---
name: agency-creative-studio
description: >-
  Use when building, growing, or auditing agency-grade creative work:
  brainstorm, premium websites, Framer Motion/GSAP, Three.js/R3F, conversion
  copy, SEO/CRO/CTAs/llms.txt growth, persuasive reports, or review existing
  websites and brands — routes ideate, design-web, motion, immersive-3d, copy,
  growth, report, review, full-pipeline.
---
# Agency Creative Studio

Run a full creative-agency pipeline with AI coding agents: invent the idea, lock the art direction, ship premium animated/3D web experiences, write copy that converts, grow traffic and conversions (SEO / CRO / CTAs / llms.txt), deliver reports that persuade, and **review existing websites and brands**. Route to the right mode — do not do everything on every request.

## When this applies

Use for agency-grade websites, landing pages, brand sites, motion/3D experiences, creative brainstorms, conversion copy, SEO/CRO/growth, decks, client/board reports, and audits of live sites or brand systems. If the user only wants a narrow task, stay in that mode; if they want an end-to-end build, run the pipeline in order.

## Modes (pick one primary)

| Mode | Trigger signals | Outcome |
| --- | --- | --- |
| `ideate` | stuck, concepts, “make it weirder,” creative direction | 3–7 specific concepts + recommendation |
| `design-web` | site, landing page, UI, Awwwards, premium web | Production-ready frontend with clear aesthetic |
| `motion` | Framer Motion, GSAP, scroll, microinteractions | Choreographed, performant motion |
| `immersive-3d` | Three.js, R3F, WebGL, Spline, cinematic scroll | 3D/scroll story with mobile fallbacks |
| `copy` | headlines, landing copy, CTAs, emails that convert | Persuasive human copy + CRO notes |
| `growth` | SEO, technical SEO, CRO, CTA, llms.txt, AEO/GEO, rankings, conversion rate | Growth audit and/or implementable SEO·CRO·CTA·llms.txt plan |
| `report` | briefings, PDFs, decks, client/board packs | Beautiful, decision-driving report |
| `review` | audit site, review brand, competitor teardown, “what’s wrong with this site” | Structured audit + prioritized fixes + optional redesign brief |
| `full-pipeline` | “agency site end-to-end,” launch, rebrand | Ideate → design → motion/3D → copy → growth → QA |

If unclear, ask one question: which mode — or default to `full-pipeline` only when they clearly want a complete site/campaign. Default to `review` when they paste a URL/brand pack for creative teardown. Default to `growth` when the ask is SEO, CRO, CTAs, rankings, llms.txt, or “why isn’t this converting/ranking.”

For deep PageSpeed, vulnerabilities, headers, and launch ops beyond growth marketing, hand off to **Technical Website Soundness** (`technical-website-soundness`).

---

## Global hard rules

1. **Taste before templates.** Commit to one aesthetic. Ban generic AI UI: Inter-only stacks, purple gradients, identical card grids, fade-up-everything.
2. **Human voice.** Kill corporate AI tells. Acid test: would a sharp human say this out loud to someone they respect?
3. **No fake data.** Never invent metrics, rankings, or citations. Label examples as example data. Separate **observed** facts from **judgment**.
4. **Performance & a11y.** Prefer `transform`/`opacity`; honor `prefers-reduced-motion`; degrade 3D on weak devices. Growth work must not ignore CWV.
5. **Approval gates.** For architectural or client-facing work: outline art direction / story before heavy build when stakes are high.
6. **Progressive disclosure.** Load depth only for the active mode.
7. **Reviews need evidence.** Prefer live URL fetch, screenshots, or user-supplied assets.
8. **Growth honesty.** `llms.txt` is not a Google ranking lever. Don’t sell it as one.

---

## Mode: `growth` (SEO · CRO · CTA · llms.txt)

Goal: make the site discoverable, convertible, and agent-legible — technically and persuasively.

### Sub-modes (combine as needed)

| Sub | Use when |
| --- | --- |
| `seo` | Crawl/index, on-page, IA, schema, CWV-as-SEO, search visibility |
| `cro` | Page isn’t converting; funnel/landing optimization |
| `cta` | Button/offer hierarchy and copy tests |
| `llms` | `/llms.txt`, markdown mirrors, AI/agent readability (AEO/GEO adjacent) |
| `full-growth` | End-to-end growth pass on a URL or new build |

### A. Technical + on-page SEO

Pipeline: **Crawl → Render → Index → Signals**.

**Crawl / index**
- `/robots.txt` at host root; don’t block CSS/JS or money pages; include `Sitemap:`
- XML sitemap = only 200, canonical, indexable URLs
- Canonical host (www/apex) + HTTPS; no redirect chains
- `noindex` via meta/X-Robots-Tag for thank-you, staging, faceted junk — not robots.txt alone for index control
- Real `<a href>` internals; avoid hash-router public content; avoid soft-404 SPAs
- Prefer SSR/SSG for critical SEO content

**On-page / IA**
- Unique title + H1; intent match; clear hierarchy
- Internal links to money pages; shallow depth for key URLs
- Image alt; descriptive URLs

**Schema**
- JSON-LD matching **visible** content: Organization/WebSite, BreadcrumbList, Service, Article, FAQ only if real

**CWV (SEO-relevant UX)**
- Field p75 targets: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1
- Fix speed before creative A/B when CWV is Poor

**AI crawlers**
- In robots.txt, separate training vs answer/search bots intentionally
- Never block Googlebot by accident when trying to limit training (e.g. Google-Extended ≠ Googlebot)

### B. CRO (LIFT-oriented)

One visitor type · one offer · one primary action.

Raise: **value proposition, relevance, clarity, urgency**  
Cut: **anxiety, distraction**

Mechanics:
1. Message match (headline ↔ ad/email/query)
2. Above-fold: what / who / outcome / primary CTA
3. Proof near claims (specific, peer-like)
4. Benefits > features; cut form fields
5. Objection handling (FAQ, process, guarantee)
6. Repeat the **same** primary CTA after proof and at bottom
7. Test order: headline → value prop → CTA → proof → form/layout
8. Don’t test copy on a broken/slow page

### C. CTAs

**Formula:** `[Action verb] + [specific outcome]`  
Strong: `Get my free audit`, `Book a 15-min intro`, `Start my free trial`  
Weak: `Submit`, `Learn more`, `Click here`

- One primary (filled, high contrast); secondary ghost/link only
- First-person often wins (`Start my…`)
- Microcopy beside button (time, cost, risk reversal)
- ≥44×44px tap targets; visible without scroll on simple offers; repeat on long pages
- Same primary label across a landing page — don’t split equal-weight CTAs

### D. llms.txt (+ agent legibility)

Spec: [llmstxt.org](https://llmstxt.org/). Proposal for a curated Markdown map for agents at inference time.

| File | Role |
| --- | --- |
| `robots.txt` | Crawl allow/disallow |
| `sitemap.xml` | Full indexable URL list |
| `llms.txt` | Curated “read this first” map — **grants nothing; not a Google ranking factor** |

Format order: `#` H1 (required) → optional `>` summary → optional prose → `##` sections with `- [Name](url): notes` → optional `## Optional` skippable links.

Also useful: clean `.md` mirrors of key pages; `rel="alternate" type="text/markdown"`; `rel="describedby"` → llms.txt.

Ship a short hand-curated `/llms.txt` (≈10–20 links: services, work, process, pricing, contact, brand) — not a dump of the sitemap.

**Example skeleton:**
```markdown
# Site Name

> One-line what you do and for whom.

## Core

- [Services](https://example.com/services.md): …
- [Work](https://example.com/work.md): …
- [Contact](https://example.com/contact.md): …

## Optional

- [Blog](https://example.com/blog): …
```

### Growth output format

1. **Snapshot** — discoverability + convertibility in 3–5 sentences  
2. **Scorecard (1–5)** — Technical SEO, On-page/IA, CRO, CTA clarity, Agent legibility (llms.txt)  
3. **P0 / P1 / P2 actions** — evidence, fix, effort  
4. **Artifacts to ship** — e.g. robots.txt diff, sitemap rules, title/H1 map, CTA matrix, `/llms.txt` draft, schema JSON-LD  
5. **Test backlog** — ordered experiments (hypothesis + metric)  
6. **Handoffs** — `copy` for rewrites; `design-web`/`motion` if layout blocks conversion; **Technical Website Soundness** for deep perf/security; `report` for client delivery  

### Growth anti-patterns

- Selling llms.txt as a Google hack  
- Ranking advice without crawl/index basics  
- Five competing CTAs  
- CRO recommendations that trash LCP (autoplay video, heavy 3D above the fold with no budget)  
- Invented traffic/keyword metrics  

Companion installs:
```bash
npx skills add coreyhaines31/marketingskills --skill seo-audit
npx skills add coreyhaines31/marketingskills --skill ai-seo
npx skills add coreyhaines31/marketingskills --skill schema-markup
npx skills add coreyhaines31/marketingskills --skill site-architecture
npx skills add coreyhaines31/marketingskills --skill page-cro
npx skills add coreyhaines31/marketingskills --skill copywriting
npx skills add coreyhaines31/marketingskills --skill ab-testing
```

---

## Mode: `review` (websites & brands)

Goal: agency-grade teardown of an existing site and/or brand — honest, specific, prioritized, actionable.

### Inputs
- Primary URL(s) and key pages; brand assets; competitors; review goal; audience/offer

### Passes
**A. Brand** · **B. IA/UX** · **C. Visual craft** · **D. Motion/immersive** · **E. Copy/CRO** · **F. Competitive** (if comps)

### Output
1. Snapshot  
2. Scorecard (Brand, UX, Visual, Motion, Copy/CRO, Consistency)  
3. Top 5 fixes (impact × effort)  
4. Evidence log  
5. Redesign brief  
6. Next-mode handoff (`ideate`, `design-web`, `growth`, `copy`, etc.)

If the ask is primarily rankings/conversions/llms.txt, prefer **`growth`** (or run `review` then `growth`).

---

## Mode: `ideate`

Non-obvious concepts via SCAMPER / first principles / Six Hats / lateral provocations / multi-expert debate. Refuse first obvious slop ideas. Deliver named concepts + recommendation; hand off after user picks.

---

## Mode: `design-web`

Art direction → type/color/spacing system → production UI. Anti-AI-slop. Implement working code. QA skim/contrast/focus/states.

---

## Mode: `motion`

Motion/react or Framer for UI; GSAP+ScrollTrigger(+Lenis) for scroll stories; CSS when enough. Orchestrate; respect reduced motion; LazyMotion when bundle matters.

---

## Mode: `immersive-3d`

CSS pseudo-3D vs R3F/Three vs Spline. Scroll/mouse via refs/`useFrame`/GSAP. Compressed assets; mobile fallbacks; perf budget.

---

## Mode: `copy`

Awareness diagnosis → structure → frameworks on demand → CTA formula → humanize → optional CRO notes. Pairs tightly with `growth` CTA/CRO work.

---

## Mode: `report`

Delegate to **Premium Report Craft** (`premium-report-craft`). Use after `review` or `growth` for client-ready PDF/deck.

---

## Mode: `full-pipeline`

1. Optional **`review`** if a current site/brand exists  
2. **Ideate** → **art direction one-pager** (approve if client-facing)  
3. **IA + section map**  
4. **design-web** → **motion** / **immersive-3d** → **copy**  
5. **`growth`** — robots/sitemap/canonicals, titles, schema, CTA hierarchy, CWV sanity, `/llms.txt`  
6. Optional **Technical Website Soundness** `fix` for launch  
7. **QA** — visual, a11y, perf, reduced-motion, mobile 3D, CTA clarity, indexability  
8. Optional **report**

Do not skip art direction on premium builds; do not skip growth plumbing on marketing launches.

---

## Suggested install bundles (reference)

**Agency motion**
```bash
npx skills add anthropics/skills --skill frontend-design -a cursor
npx skills add Leonxlnx/taste-skill --skill design-taste-frontend -a cursor
npx skills add pbakaus/impeccable -a cursor
npx skills add https://github.com/greensock/gsap-skills -a cursor
npx skills add AThevon/genjutsu -a cursor
npx skills add https://github.com/DevMartinese/awwwards-animations-skill --skill awwwards-animations -a cursor
```

**Ideation**
```bash
npx skills add https://github.com/obra/superpowers --skill brainstorming -a cursor
npx skills add bastien-gallay/bfw
```

**Copy + growth**
```bash
npx skills add coreyhaines31/marketingskills --skill copywriting
npx skills add coreyhaines31/marketingskills --skill copy-editing
npx skills add coreyhaines31/marketingskills --skill page-cro
npx skills add coreyhaines31/marketingskills --skill seo-audit
npx skills add coreyhaines31/marketingskills --skill ai-seo
npx skills add coreyhaines31/marketingskills --skill schema-markup
npx skills add coreyhaines31/marketingskills --skill ab-testing
```

---

## Output expectations

- Lead with the mode you chose in one line  
- Prefer working artifacts (code, robots/llms.txt drafts, CTA matrices, title maps)  
- For `review`: Top 5 fixes + redesign brief unless opted out  
- For `growth`: P0/P1/P2 + shippable artifacts + test backlog  
- End premium builds with a short QA checklist  

## Anti-patterns

- Running all modes when the user asked for a headline  
- “Make it pop” motion with no hierarchy  
- 3D that bricks mobile or CWV  
- Pretty report with no ask  
- Review without evidence  
- Growth theater (llms.txt worship, keyword stuffing) without crawl/index/CTA basics  
- Skipping art direction into generic SaaS layout
