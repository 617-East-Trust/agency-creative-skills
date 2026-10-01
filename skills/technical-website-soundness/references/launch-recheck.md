# Launch recheck — post-change and pre-release matrix

Use with Technical Website Soundness `go` mode.

## Release-safe sequence (mandatory)
1. Record current config + rollback path  
2. One coherent change set  
3. Validate in staging/preview when possible  
4. Deploy via approved path  
5. Recheck production signals below  
6. Issue **GO / GO WITH CONDITIONS / NO-GO** + residual risk  

## Recheck matrix

| Check | Pass criteria | Evidence |
| --- | --- | --- |
| Canonical host | Single HTTPS host; www/apex policy correct | `curl -I` chain |
| Certificate | Valid for served hostnames | TLS observe date |
| Key routes | Expected 200; real 404/410 | Status codes |
| robots.txt | 200; not blocking money pages/CSS/JS; Sitemap line | Body fetch |
| Sitemap | Canonical indexable URLs only | Sample URLs |
| noindex | Staging/previews noindex; money pages indexable | Meta / X-Robots |
| Security headers | Agreed set present on key templates | Header dump |
| Secrets | No prod secrets in client bundle | Build/repo review |
| CWV plan | Lab/field noted on home + top landing | Tool + date |
| Forms | Mobile submit path works; spam controls on | Manual/staging test |
| Analytics | Primary conversion event fires once | Tag debug / network |
| Rollback | Owner knows how to revert redirects/headers/release | Written note |

## Go vocabulary
- **GO** — No open P0/P1; residual P2/P3 scheduled  
- **GO WITH CONDITIONS** — Launch allowed with explicit time-bound mitigations  
- **NO-GO** — Open P0 or unresolved P1 on a key journey  

## After launch
Re-run affected rows within 24–72h; compare to pre-change evidence IDs (`T-##`).
