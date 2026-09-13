---
name: technical-website-soundness
description: >-
  Use when analyzing or building technically sound websites — PageSpeed/Core Web
  Vitals, security vulnerabilities and headers, crawl/index SEO plumbing,
  robots/sitemaps/canonicals, HTTPS/host logistics, JS rendering risks, launch
  checklists, and ops hardening. For audits, fixes, or scaffolding
  production-ready technical baselines.
---
# Technical Website Soundness

Analyze or build websites that are technically and logistically sound: crawlable, fast (PageSpeed / Core Web Vitals), secure, operable, and free of common production landmines. Pair with creative/design skills for looks — this skill owns infrastructure, performance, security, SEO mechanics, and launch logistics.

## When to use

- Audit an existing site (URL, repo, or deploy)
- Harden a site before launch or redesign
- Implement technical baselines while building (Next.js, static, WordPress, etc.)
- Triage PageSpeed, CWV, vulnerabilities, crawl/index issues, or fragile ops

Modes: `analyze` | `create` | `fix` (launch readiness). Infer from the ask; default to `analyze` when given a URL.

---

## Hard rules

1. **Evidence over vibes.** Cite what you observed (headers, status codes, Lighthouse/CWV numbers, response bodies). Label estimates vs measurements.
2. **No fake scores.** Don’t invent Lighthouse/PSI numbers. If you can’t run a tool, say so and give a checklist-based review from available signals.
3. **Fix order:** availability & security → crawl/index → performance → polish. Don’t A/B CTAs on a 5xx or blocked site.
4. **Don’t break prod.** Prefer reversible changes; call out risk for redirects, robots, and auth.
5. **Separate judgment from fact.** “LCP is 4.1s on mobile field data” vs “hero feels heavy.”

---

## Mode: `analyze`

### 1. Scope
Confirm: production URL(s), staging vs prod, target locales, stack if known, goal (launch, SEO, security, speed, full health).

### 2. Passes (run all that apply)

**A. Availability & logistics**
- DNS resolves; HTTPS cert valid for host; www/apex redirect policy (one canonical host)
- Homepage and key routes return expected status (200); real 404/410 (not soft-404 SPA)
- Redirect chains/loops; HTTP→HTTPS; mixed content
- Staging/preview not indexable; auth walls behave
- Env separation: no prod secrets in client bundles; correct API bases

**B. Security (high-signal)**
- HTTPS everywhere; HSTS present/sensible
- Security headers where appropriate: `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, frame protections
- Cookies: `Secure` / `HttpOnly` / `SameSite` on session cookies
- No obvious secret leakage (keys in JS, public `.env`, open directory listings)
- Dependency/supply chain: flag known risky patterns; recommend `npm audit` / Dependabot / lockfiles — don’t claim CVEs without running scanners
- Forms: CSRF strategy, spam protection, rate limits (note presence/absence)
- Admin/login paths not trivially exposed; directory listing off
- Third-party scripts: inventory; minimize; note XSS/supply risk from tag managers

**C. Crawl & index (technical SEO)**
- `/robots.txt` at host root, 200, not blocking CSS/JS or money pages; `Sitemap:` line
- XML sitemap: only canonical, 200, indexable URLs; submitted in GSC when relevant
- Canonicals consistent; no conflicting noindex on key pages
- Titles/H1 unique; primary content in HTML or reliably SSR/SSG (not client-only for critical SEO)
- Internal links are real `<a href>`; no hash-router SEO trap for public content
- Structured data JSON-LD matches visible content (if present)
- AI bot policy intentional (training vs answer crawlers) — document, don’t guess business intent
- Optional: `/llms.txt` curated map — **not a Google ranking lever**; nice for agents

**D. Performance / PageSpeed / CWV**
Field targets (p75): **LCP ≤ 2.5s**, **INP ≤ 200ms**, **CLS ≤ 0.1**
- Hero/LCP element: image sizing, priority hints, compression (AVIF/WebP), no giant unoptimized PNG
- Fonts: subset, `font-display`, avoid layout shift
- JS: main-thread cost, hydration weight, code-split, defer non-critical
- CSS: critical path; avoid huge unused frameworks on landing pages
- Caching: CDN, cache headers, hashed assets
- Third parties: analytics/chat/embeds impact on LCP/INP
- Motion/3D: dynamic import; degrade on mobile; don’t block LCP for WebGL
- If tools available: run Lighthouse/PSI lab + note field CrUX when present; separate lab vs field

**E. Accessibility & quality gates (technical)**
- Focus states, tap targets, contrast on critical UI
- Images with alt when meaningful; form labels
- `prefers-reduced-motion` respected if motion-heavy

**F. Ops & logistics**
- Error monitoring / uptime (presence)
- Backups / rollback path for CMS or content
- Analytics & conversion events firing without breaking CSP
- Legal pages linked; cookie consent doesn’t wreck CWV or block crawl of content incorrectly
- Deploy preview URLs `noindex`
- Ownership: DNS, cert renewal, domain lock, who can deploy

### 3. Output format (always for analyze)

1. **Snapshot** — one paragraph health read  
2. **Scorecard (1–5)** — Security, Crawl/Index, Performance, Logistics/Ops, A11y (one-line each)  
3. **P0 / P1 / P2 findings** — each with evidence, impact, fix, effort  
4. **PageSpeed plan** — top 5 concrete changes expected to move LCP/INP/CLS  
5. **Quick wins vs projects**  
6. **Recheck list** — what to re-measure after fixes  

Optional: hand off narrative to Premium Report Craft for a client PDF.

---

## Mode: `create` (build technically sound)

When implementing or scaffolding, bake in:

### Baseline architecture
- Prefer **SSG/SSR** for marketing pages; hydrate islands sparingly
- One canonical host + HTTPS redirects from day one
- Trailing-slash policy chosen and enforced
- Env-based config; secrets server-only

### SEO plumbing (ship with the site)
- `robots.txt` + `sitemap.xml` (generated from real routes)
- Per-route title/description/canonical
- `noindex` on thank-you, search, faceted junk, previews
- Organization/WebSite JSON-LD as appropriate
- Optional curated `/llms.txt` + markdown mirrors for key pages

### Performance budget (marketing sites)
- LCP image predetermined; width/height or aspect-ratio reserved
- No unconditioned third-party scripts in `<head>` without review
- Route-level code splitting; defer chat/widgets until idle or interaction
- Animation libraries: lazy / feature subsets; respect reduced motion
- 3D/WebGL behind dynamic import + device capability check

### Security defaults
- Security headers at CDN/host
- Dependency lockfile + automated audit in CI
- Forms behind server validation + spam controls
- CSP planned before dumping GTM

### Logistics
- Staging `noindex` + auth if needed
- 404/500 pages with correct status codes
- Health check route; basic monitoring recommendation
- Deploy docs: env vars, domains, rollback

Deliver a **technical acceptance checklist** with the build.

---

## Mode: `fix` (pre-launch)

Go/no-go against:

- [ ] Single HTTPS canonical host; cert OK  
- [ ] robots.txt + sitemap sane; staging not indexed  
- [ ] Key templates: 200, canonical, unique titles, real 404  
- [ ] CWV plan: field/lab checked on home + top landing templates  
- [ ] Security headers + cookie flags reviewed  
- [ ] No secrets in client bundle  
- [ ] Forms work on mobile; errors clear; spam protection on  
- [ ] Analytics/conversions verified once  
- [ ] Backups/rollback known  
- [ ] Legal/consent doesn’t break UX or crawl  

Output: **GO / GO WITH CONDITIONS / NO-GO** + condition list.

---

## Priority matrix (use when triaging)

| Priority | Examples |
| --- | --- |
| **P0** | Site down, invalid cert, open admin, secrets leaked, ransomware-level misconfig, entire site `Disallow: /` in prod |
| **P1** | Money pages noindexed, CWV Poor on key URLs, mixed content, redirect loops, soft-404, missing HTTPS redirect |
| **P2** | Schema gaps, llms.txt missing, header hardening, image weight, third-party trim |
| **P3** | Nice-to-have audits, copy-level SEO, speculative bot policy tweaks |

---

## Companion skills / tools

- Install when deeper marketing SEO/CRO needed: `seo-audit`, `ai-seo`, `schema-markup`, `page-cro` from coreyhaines31/marketingskills  
- Creative/motion sites: still enforce this skill’s perf/security gates (Agency Creative Studio builds must not skip CWV)  
- Reports: Premium Report Craft for client-facing audit PDFs  

Tools to use when available: PageSpeed Insights, Lighthouse, WebFetch/curl headers, SSL checkers, GSC (user-provided), `npm audit`, header inspectors. Never claim a scan you didn’t run.

---

## Anti-patterns

- Chasing Lighthouse 100 while ignoring indexation or XSS  
- Blocking AI/search bots accidentally in robots.txt  
- Shipping WebGL heroes with unoptimized 5MB textures on mobile  
- Putting `noindex` in initial HTML and removing it only via client JS  
- “We’ll fix performance after launch” on a marketing site  
- Inventing vulnerability CVE lists without a scanner output
