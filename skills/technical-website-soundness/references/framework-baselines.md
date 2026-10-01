# Framework baselines — static, Next.js, CMS, CDN

Before prescribing controls, identify the platform. Same control often lives in different places.

## Platform check questions
1. Static host, Node/SSR framework, CMS, or hybrid?  
2. CDN / reverse proxy in front (Cloudflare, Fastly, Vercel Edge, nginx)?  
3. Where are headers set today (app, host config, CDN)?  
4. Preview/staging URL policy?  

## Implementation matrix template

| Control | File / platform surface | Owner | Verification |
| --- | --- | --- | --- |
| Canonical HTTPS host redirect | CDN / host rules | Infra | `curl -I` http + www variants |
| Security headers | CDN or `next.config` / middleware | Web eng | Header inspect on home + app shell |
| robots.txt | `/public/robots.txt` or route handler | Web eng | 200 at host root; Sitemap line |
| sitemap | Build script / CMS plugin | Web eng | Only 200 canonical URLs |
| noindex previews | Host preview settings + meta | Web eng | Preview fetch shows noindex |
| LCP image policy | Component + image pipeline | Front-end | Dimensions reserved; compressed |

## Static sites
- Headers at CDN; hashed assets + long cache; HTML shorter cache  
- Generate sitemap from real routes at build time  

## Next.js (and similar SSR/SSG)
- Prefer static/SSG for marketing routes; islands of hydration  
- `headers()` / middleware / host config — pick one source of truth  
- `robots.ts` / `sitemap.ts` from actual route inventory  
- Secrets server-only; no `NEXT_PUBLIC_` for sensitive values  

## CMS (WordPress, etc.)
- Canonical plugins carefully; avoid duplicate sitemaps  
- Lock admin surface; keep XML-RPC/auth attack surface in mind at **policy** level only (passive)  
- Caching layer (page cache + CDN) documented for purge/rollback  

## CDN / proxy
- HSTS, compression, TLS version, redirect rules often belong here  
- Preview protections (`noindex`, auth) at the edge when possible  

## Performance budget (marketing)
- Predetermined LCP image; width/height or aspect-ratio  
- Defer chat/widgets; lazy motion/3D; honor reduced motion  
- No unconditioned third-party scripts in `<head>` without review
