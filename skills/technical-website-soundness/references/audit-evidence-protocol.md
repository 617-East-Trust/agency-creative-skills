# Audit evidence protocol — collection and records

Companion to Technical Website Soundness. Keep passive/authorized scope from the parent skill.

## Minimum record
Every finding must include the evidence-record fields in SKILL.md (ID, priority, scope, observation, method, impact, fix, verification, confidence).

## Suggested passive methods (when available)

| Area | Examples (non-exhaustive) |
| --- | --- |
| Availability | DNS resolve; HTTPS cert validity; status codes on key routes; redirect chain length |
| Headers | Fetch response headers: CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, cookies flags |
| Crawl/index | `/robots.txt`, sitemap URLs, canonical link tags, meta robots, SSR vs client-only content check |
| Performance | PSI/Lighthouse **lab** (label as lab); CrUX/field when present; note route + device + date |
| Dependencies | Lockfile present; `npm audit` / equivalent only when repo access exists — never invent CVEs |
| Repo/config | Env usage, `noindex` in previews, secret patterns in client bundles (static review) |

## Recording CWV
- Always state **lab vs field**  
- Include route, device profile, date/time, tool  
- If no field data: write **“No field data available”**  
- Do not treat a single lab run as production truth  

## Confidence guide
- **High** — Direct observation on stated host with reproducible method  
- **Medium** — Indirect or partial signal (e.g. lab only, single locale)  
- **Low** — Heuristic from source patterns without runtime proof  
- **N/E** — Not run; leave score N/E  

## What not to do
- Auth bypass, credential stuffing, exploit PoCs, stress/load abuse  
- Scanning hosts outside the stated scope  
- Claiming scanner output you do not have  

## Finding ID convention
`T-##` technical findings; map to P0–P3. Recheck IDs stay stable across `go` revalidation.
