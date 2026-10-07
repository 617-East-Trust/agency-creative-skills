# Report layouts — memo, board pack, client report

Pick one aesthetic and one scaffold; execute consistently.

## Scaffolds

| Scaffold | Arc |
| --- | --- |
| Executive brief | Situation → insight → options → recommendation → ask |
| Analysis report | Question → method → findings → implications → next steps |
| Board / QBR | Outcomes vs plan → drivers → risks → decisions needed |
| Client deliverable | Goal → what we did → results → proof → recommended next move |
| Pitch / conversion | Problem → stakes → solution → proof → offer / CTA |

## Aesthetics

- **Nordic editorial** — whitespace, restrained type, thin rules, muted palette + one accent  
- **Consulting crisp** — dense but scannable, navy/charcoal, sharp tables, action titles  
- **Agency premium** — distinctive display + refined body, careful charts, cinematic but readable section openers  

Use supplied brand fonts/colors when provided. Do not invent a fake brand system.

## Page anatomy

1. Cover / title: sharp title + so-what subtitle; audience / date / classification  
2. Executive summary: findings + numbered recommendations (severity when useful)  
3. Body section: **takeaway headline** → short frame → evidence (KPI strip, table, chart, quote) → **Implication**  
4. Close: decision checklist, ask, or CTA — never vague “happy to discuss”  
5. Appendix: method, raw tables, evidence ledger  

## Visual rules
- Type hierarchy: display / H1 / H2 / body / caption  
- KPI strips: few metrics, large numbers, tiny labels, context under each  
- Charts: one message; label directly; no chartjunk; cite source  
- Tables: highlight the cell that matters  
- Chrome: quiet header rule, page N/M, classification if needed  
- Commit to light or dark — do not mix casually  

## Markdown default skeleton

```markdown
# [Action-oriented title]
**Subtitle:** [So-what in one line]
**Audience / date / classification**

## Executive summary
- Finding…
### Recommendations
1. …

## [Takeaway section title]
Framing paragraph.

| KPI | Value | Context |
| --- | --- | --- |

**Implication:** …

## Decision / ask
- [ ] …
```

## PDF notes
- Prefer existing project templates or restrained CSS  
- After render: inspect for truncation, contrast, orphans, overflow tables  
- Keep depth in appendix; exec pages stay scannable
- If a renderer or image-inspection surface is unavailable, deliver the source artifact with the explicit status **“generated, not visually inspected”**; do not mark visual QA complete.
