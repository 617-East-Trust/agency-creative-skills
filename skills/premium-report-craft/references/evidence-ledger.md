# Evidence ledger — claim / source / status process

Required whenever a report makes factual, financial, performance, customer, or research claims. Omit only for clearly labelled concept work with no factual claims.

## Status vocabulary

| Status | Meaning | May present as result? |
| --- | --- | --- |
| **Verified** | Source checked; claim matches source within stated scope | Yes |
| **Qualified** | Directionally supported; caveats required (sample, date, lab vs field) | Yes, with caveat inline |
| **Hypothesis** | Plausible claim to test; not yet evidenced | Only as hypothesis / test plan |
| **Placeholder** | Layout mock value; not real data | Only when user asked for a mock; label visibly |

## Ledger table

| ID | Claim or visual | Source / owner | Status | Location in deliverable |
| --- | --- | --- | --- | --- |
| C-01 | Conversion declined after the March release | Analytics export, 12 Sep 2026 | Verified | Executive summary, figure 2 |
| C-02 | Slow mobile LCP is a material contributor | Technical audit finding T-04 | Qualified | Recommendation 1 |
| C-03 | Revised flow will improve conversion | Experiment backlog | Hypothesis | Test plan |

## Process

1. Extract thesis → list 3–7 supporting claims  
2. For each claim, attach a source or mark unsupported  
3. Assign status before drafting body copy  
4. Place citations near the claim or under figures  
5. Re-check ledger against final PDF/deck during render inspection  
6. Ship ledger as appendix when the audience is technical or skeptical  

## Rules
- Never upgrade Hypothesis → Verified without new evidence  
- Charts inherit the status of their underlying claims  
- If source access is missing, ask once or proceed with labeled gaps — do not invent numbers  
- Technical Website Soundness findings enter as Qualified/Verified with their finding IDs
