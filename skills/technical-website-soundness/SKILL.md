---
name: technical-website-soundness
description: >-
  Audit or implement website technical readiness for performance, Core Web
  Vitals, security headers and exposed configuration, crawl/index mechanics,
  deployment hygiene, and launch checks. Use for a URL, repository, or release
  that needs evidence-backed technical findings, safe fixes, or a go/no-go
  decision. Do not use for visual design, general copywriting, keyword strategy,
  or intrusive penetration testing.
---

# Technical Website Soundness

Analyze or build websites that are crawlable, fast (PageSpeed / CWV), securely configured at the public surface, operable, and free of common production landmines. Pair with creative skills for looks — this skill owns infrastructure, performance, passive security posture, SEO mechanics, and launch logistics.

## Safe audit boundary

> Perform only passive or low-impact checks that the user is authorized to request: public HTTP responses, redirects, page source, declared configuration, dependency scanners, and the user-provided repository/deployment. Do not attempt authentication bypass, exploitation, credential testing, scanning that materially stresses a service, or discovery outside the stated hosts. Escalate to an authorized security assessment when deeper testing is needed.

## Boundary with GSC Growth Operator

Own **live production proof and safe implementation**: HTTP headers, robots/canonical behavior, redirects, rendering, PageSpeed/CrUX collection, security headers, deploy/rollback, and launch go/no-go. Route GSC property data—query/page performance, CTR, drops, cannibalization, URL Inspection, coverage, and sitemap-to-inspection correlation—to **GSC Growth Operator**. Accept its evidence as impact context; do not rerun its property analysis. Client narrative → **Premium Report Craft**.

## Modes

`analyze` | `create` | `go` — infer from the ask; default `analyze` when given a URL.

## Hard rules

1. **Evidence over vibes.** Cite observed headers, status codes, lab/field numbers, response bodies. Label estimates vs measurements.  
2. **No fake scores.** Do not invent Lighthouse/PSI/CVE lists. If a tool did not run, say so.  
3. **Fix order:** availability & security → crawl/index → performance → polish.  
4. **Don’t break prod.** Prefer reversible changes; call out risk for redirects, robots, auth.  
5. **Separate judgment from fact.** “LCP is 4.1s on mobile field data” vs “hero feels heavy.”

## Calibrated score (1–5 + N/E)

| Score | Meaning |
| --- | --- |
| 5 | Verified healthy; no material issue in tested scope |
| 4 | Sound baseline; only minor or isolated improvements remain |
| 3 | Material gaps to schedule before next growth/launch milestone |
| 2 | Multiple material, verified gaps requiring remediation before the next milestone |
| 1 | Immediate production, security, availability, or indexation risk |
| N/E | Not evaluated — never convert missing evidence into a score |

Scorecard areas: Security · Crawl/Index · Performance · Logistics/Ops · A11y (technical).

Report these independently of the 1–5 condition score: **Evidence coverage** (`complete` / `partial` / `missing`) and **confidence** (`high` / `medium` / `low` / `not evaluated`). Missing evidence is `N/E`, not a score of 2.

## Calibrated priority (P0–P3)

| Priority | Definition | Illustrative cases |
| --- | --- | --- |
| **P0** | Verified issue creating an immediate availability, unauthorized exposure, or production indexation incident | Site unavailable; production credentials publicly exposed; unintended sitewide noindex/Disallow on prod |
| **P1** | Verified material issue affecting a key journey, landing page, security control, or release readiness | Money page noindexed; redirect loop; cert failure on major host; critical route consistently unusable |
| **P2** | Important resilience, performance, hardening, or quality issue without an active incident | Oversized LCP asset; missing security header after context review; weak cache; schema mismatch |
| **P3** | Low-risk improvement or unverified observation needing measurement before action | Optional llms.txt; speculative bot-policy tweak; non-critical metadata cleanup |

Use **N/E**, not P3, when an area was not evaluated.

## Evidence record (every finding)

| Field | Requirement |
| --- | --- |
| Finding ID and priority | Unique ID; P0–P3 under calibrated rubric |
| Scope | URL/route, environment, tested host, date/time |
| Observation | Exact status, header, behavior, lab result, repo path, or scanner output |
| Method | Tool/method; lab, field, static, or configuration |
| Impact | Concrete user, search, availability, exposure, or ops effect |
| Fix | Lowest-risk repair + platform owner |
| Verification | Exact recheck after deploy + rollback consideration |
| Confidence | High / medium / low / not evaluated |

CWV numbers require source, test type, route, device profile, and date. Say **“No field data available”** rather than treating lab as real-user experience. Collection detail: `references/audit-evidence-protocol.md`.

## Mode: `analyze`

**Passes (as applicable):** Availability & logistics · Security (passive) · Crawl/index · Performance/CWV · Technical a11y · Ops/logistics.

**Output:** Snapshot → Scorecard (1–5 or N/E) → P0–P3 findings with evidence records → PageSpeed plan (top concrete LCP/INP/CLS moves) → Quick wins vs projects → Recheck list.

Optional client narrative → **Premium Report Craft**.

## Mode: `create`

1. **Platform check** — Infer or ask host/framework (static, Next.js, CMS, CDN/proxy) before prescribing headers, redirects, caching, or noindex.  
2. **Baselines** — SSG/SSR for marketing pages; one canonical HTTPS host; robots + sitemap from real routes; perf budget; security headers at edge; staging `noindex`. See `references/framework-baselines.md`.  
3. **Implementation matrix** — Emit **control → file/platform → owner → verification**.  
4. Deliver a **technical acceptance checklist** with the build.

## Mode: `go` (release-safe sequence)

1. Back up / record current config and rollback path  
2. One coherent change set  
3. Validate routes/headers in staging or preview when possible  
4. Deploy via approved path  
5. Recheck canonical host, status codes, robots/sitemap, affected perf signals, form/conversion path  
6. State residual risk + **GO / GO WITH CONDITIONS / NO-GO**

Full matrix: `references/launch-recheck.md`.

## Pairing

- Creative/motion builds must still clear this skill’s perf/security gates  
- Search Console performance/indexation depth → **GSC Growth Operator**; CRO depth → specialist when present
- `llms.txt` optional for agents — **not a Google ranking lever**

## Anti-patterns

- Intrusive pentest under this skill’s name  
- Chasing Lighthouse 100 while ignoring indexation or exposure  
- Inventing CVE lists or CWV scores  
- Blocking search bots accidentally in robots.txt  
- “Fix performance after launch” on a marketing site
