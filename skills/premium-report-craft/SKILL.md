---
name: premium-report-craft
description: >-
  Create or revise decision-ready reports, executive briefings, board/client
  packs, and evidence-led slide narratives. Use when a written deliverable must
  persuade, inform a decision, or present findings with a clear thesis,
  traceable evidence, and polished hierarchy. Do not use for a short email,
  standalone copy edit, raw research collection, or a technical audit itself.
---

# Premium Report Craft

Build reports that look intentional, read like a sharp human wrote them, and move the audience to understand, decide, or act. Story and clarity first; visual polish second; decoration never.

## Hard rules

1. **One job per report.** Name the outcome: inform, decide, approve, buy, escalate, or align.  
2. **Evidence ledger for factual claims.** Financial, performance, customer, or research claims need a ledger entry (verified / qualified / hypothesis / placeholder). Concept mocks may omit it when clearly labeled.  
3. **Human voice.** Concrete nouns and verbs; no corporate AI filler. Acid test: would a respected peer say this out loud?  
4. **One primary decision-relevant takeaway** per page, slide, or major section. Action titles with a verb. Charts prove the takeaway — never the reverse.  
5. **Beauty with restraint.** Typography, spacing, hierarchy, one accent — not noise.

## Format decision tree

```text
Concise doc or collaborative draft?     → Markdown report (default)
Fixed-layout client/board handoff?      → PDF report; render and inspect
Live presentation / PPT/PPTX?           → Dedicated slides tooling when available;
                                          else load references/deck-narrative.md
                                          (do not invent missing Slides MCP as a hard requirement)
Both decision deck + detail?            → Hybrid: deck for the decision; appendix/report for evidence
```

## Workflow (8 steps)

1. **Brief** — Infer audience, decision, format, sources, constraints. Ask one question only if a missing answer would materially change the story or format.  
2. **Thesis + evidence ledger** — One-sentence thesis; 3–7 claims; map each to evidence or flag unsupported. Ledger fields: ID, claim/visual, source/owner, status, location. See `references/evidence-ledger.md`.  
3. **Format + scaffold** — Select report / deck / PDF / hybrid. Scaffolds: executive brief · analysis · board/QBR · client deliverable · pitch/conversion · slide narrative. Layout notes: `references/report-layouts.md`.  
4. **Outline (conditional)** — For decision-critical work with unclear direction, show a short storyline (action titles + evidence notes) before full layout. If outcome and sources are already clear, draft directly and state material assumptions.  
5. **Draft** — Cover with so-what subtitle → executive summary → body (takeaway → frame → evidence → implication) → clear ask/CTA. Separate findings, recommendations, and hypotheses.  
6. **Visual system** — One aesthetic from supplied brand materials (Nordic editorial / consulting crisp / agency premium). Do not invent brand claims.  
7. **Quality gate** — Language, citation, format checks below.  
8. **Render & inspect** — Every non-Markdown deliverable: open the artifact; check truncation, contrast, orphans, unreadable tables. If no renderer or visual-inspection surface is available, say **“generated, not visually inspected”** and list the missing check; never imply the quality gate passed.

## Quality gate

- [ ] Thesis and ask obvious on page/slide 1–2  
- [ ] Every major section title is a takeaway, not a topic  
- [ ] Every chart/table has a so-what nearby; sources noted  
- [ ] Ledger statuses honest; no fabricated metrics  
- [ ] Voice passes “say it out loud”  
- [ ] Hierarchy works in a 3-second skim  
- [ ] Length matches stakes (depth in appendix if needed)  
- [ ] Format matches decision tree; non-MD rendered and inspected  

## Deliver

Primary artifact plus when useful:
- One-paragraph TL;DR for chat
- Speaker notes (mouth-ready) for decks
- Appendix with raw tables, method notes, and the evidence ledger when the audience is skeptical
- Open questions / data gaps list

Prefer working artifacts over prose about artifacts. If PDF/HTML was rendered, mention that visual inspection passed (or list residual layout issues).

## Visual system (apply in step 6)

Pick one and execute consistently from supplied brand materials:
- **Nordic editorial** — whitespace, restrained type, thin rules, muted + one accent
- **Consulting crisp** — dense but scannable, navy/charcoal, sharp tables, action titles
- **Agency premium** — distinctive display + refined body, careful charts, still readable

KPI strips: few metrics, large numbers, tiny labels. Charts: one message, direct labels, source under figure. Page chrome: quiet header, page N/M, classification if needed.

Minimal Markdown skeleton and layout variants: `references/report-layouts.md`.

## Pairing


- Weak persuasion → copy specialist after outline  
- Weak visuals → design/polish specialist for layout  
- Weak structure / slides → `references/deck-narrative.md` or slides tooling when present  
- Technical findings as input → accept from **Technical Website Soundness**; do not re-run the audit here  
- Organic-search findings as input → accept from **GSC Growth Operator**; do not re-run performance or indexation analysis here
- Multi-discipline engagement → receive brief from **Agency Creative Studio**

## Anti-patterns

- Walls of bullets with no thesis or ask  
- Equal weight on every insight  
- Decorative gradients that fight the data  
- Fake precision; charts without units/sources  
- Building a full novel before knowing the ask  
- Claiming a Slides/PDF tool ran when it did not
