---
name: premium-report-craft
description: >-
  Use when creating, rewriting, or polishing reports, briefings, decks, or PDFs
  that must look premium, sound human, persuade or convert, and drive a clear
  decision — executive summaries, board packs, client deliverables, analysis
  writeups, pitch-style reports.
---
# Premium Report Craft

Build reports that look intentional, read like a sharp human wrote them, and move the audience to understand, decide, or act. Story and clarity first; visual polish second; decoration never.

## Hard rules

1. **One job per report.** Name the primary outcome: inform, decide, approve, buy, escalate, or align. Design every section toward that outcome.
2. **No implementation theater.** Do not invent metrics, quotes, citations, or chart values. If data is missing, mark gaps clearly and ask or proceed with labeled placeholders only when the user wants a layout mock.
3. **Human voice is mandatory.** Ban corporate AI filler (`leverage`, `comprehensive solution`, `in today's rapidly evolving landscape`, `delve`, `landscape`, `robust`, empty parallel bullet triples). Acid test: would a respected peer say this out loud in a room?
4. **One takeaway per page/section.** Action titles with a verb (sentence case). Charts prove the takeaway — never the reverse.
5. **Beauty with restraint.** Prefer typography, spacing, hierarchy, and one accent system over noise, gradients-for-gradients, and stock illustration clutter.

## Workflow (follow in order)

### 1. Brief (ask only what you lack)

Capture or confirm:
- Audience and what they already believe
- Decision or action required by the end
- Source material (docs, data, notes, screenshots)
- Format: markdown memo, HTML review deck, PDF report, or slide outline
- Tone: board / client / internal / sales
- Constraints: length, brand colors/fonts, confidential marking, due date

If a product or brand context file exists in the project, read it first.

### 2. Diagnose the story

Before drafting:
- Extract the **thesis** in one sentence
- List 3–7 **claims** that must be true for the thesis to hold
- Map each claim to **evidence** (metric, quote, screenshot, table) or flag as unsupported
- Choose a scaffold:
  - **Executive brief** — situation → insight → options → recommendation → ask
  - **Analysis report** — question → method → findings → implications → next steps
  - **Board / QBR** — outcomes vs plan → drivers → risks → decisions needed
  - **Client deliverable** — goal → what we did → results → proof → recommended next move
  - **Pitch / conversion report** — problem → stakes → solution → proof → offer / CTA
  - **Slide narrative** — one thesis per slide, ≤3 evidence points, spoken transitions

### 3. Outline for approval (when stakes are high)

For board, client, or sales-critical work, present a short outline (section titles as action takeaways + evidence notes) and get a quick yes before full draft. For low-stakes internal notes, draft directly.

### 4. Write the content

**Voice**
- Concrete nouns and verbs; short sentences mixed with longer ones
- Specific numbers and names over abstractions
- Benefits and decisions over feature dumps
- Cut throat-clearing openers; start with the point

**Structure**
- Cover / title block: sharp title + subtitle that states the so-what
- Executive summary first: findings as cards or bullets + numbered recommendations with severity when useful
- Body sections: action headline → 1 short framing paragraph → evidence (KPI strip, table, chart, quote) → implication
- Close with a clear **ask**, decision list, or CTA — never a vague “happy to discuss”

**Conversion / persuasion (when the report must sell or secure approval)**
- Lead with audience awareness and desired belief shift
- Prefer PAS / problem–stakes–solution hybrids over generic brochure copy
- Put risk reversal, proof, and next step near the end — not buried
- CTAs: `[Action verb] + [specific outcome]`

### 5. Visual system

Pick one aesthetic and execute consistently:
- **Nordic editorial** — lots of whitespace, restrained type, thin rules, muted palette + one accent
- **Consulting crisp** — dense but scannable, navy/charcoal, sharp tables, action titles
- **Agency premium** — distinctive display + refined body type, careful photography/charts, cinematic section openers (still readable)

Apply:
- Clear type hierarchy (display / H1 / H2 / body / caption)
- Consistent spacing scale; align columns; avoid orphan labels
- KPI strips: few metrics, large numbers, tiny labels, trend or context under each
- Charts: one message each; label directly; no chartjunk; cite source under figure
- Tables: scannable; highlight the cell that matters
- Page chrome: quiet header rule, page N / M footer, classification if needed
- Dark or light theme — commit; do not mix casually

**Motion / web reports only:** subtle entrance or scroll reveals if the deliverable is HTML; respect `prefers-reduced-motion`; animate only transform/opacity.

### 6. Humanize pass (always)

Scan and rewrite:
- AI-parallel bullet stacks → uneven, spoken rhythm
- Hedging piles → one clear claim + confidence note if needed
- Synonym salad → plain words
- Identical sentence lengths → vary
- Slide/report “topic labels” → declarative takeaways

### 7. Quality gate before delivery

Check:
- [ ] Thesis and ask are obvious on page 1 / slide 1–2
- [ ] Every section title is a takeaway, not a topic
- [ ] Every chart/table has a so-what nearby
- [ ] No fabricated data; sources noted where claims need them
- [ ] Voice passes the “say it out loud” test
- [ ] Visual hierarchy works in a 3-second skim
- [ ] Length matches stakes (brief for execs; depth in appendix if needed)
- [ ] Format matches handoff (md / HTML / PDF / pptx outline)

### 8. Deliver

Ship the primary artifact plus, when useful:
- One-paragraph TL;DR for chat
- Speaker notes (mouth-ready) for decks
- Appendix with raw tables or method notes
- Open questions / data gaps list

## Output formats (pick one primary)

| Format | Use when |
| --- | --- |
| Markdown report | Docs, Notion, GitHub, quick share |
| HTML review deck / report | Visual polish before export |
| PDF executive report | Client/board handoff |
| Slide outline (+ optional pptx) | Live presentation; story before design |

If rendering PDF/HTML/PPTX, prefer existing project templates or simple clean CSS; do not invent fake brand systems. Keep CSS restrained: system or distinctive fonts the environment supports, consistent spacing tokens, one accent color.

## Anti-patterns

- Walls of bullet points with no thesis
- Decorative 3D/gradients that fight the data
- Every insight given equal weight
- “Summary of everything we found” with no recommendation
- Stock AI enthusiasm and fake precision
- Charts without units, sources, or takeaways
- Writing the full novel before knowing the ask

## Pairing hints

- Weak persuasion → lean on conversion-copy / marketing copywriting skills after the outline
- Weak visuals → frontend-design / impeccable polish skills for layout pass
- Weak structure → presentation-writing / deck.md narrative scaffolds
- Missing brainstorm → clarify thesis with a brainstorming skill before drafting

## Minimal starter skeleton

```markdown
# [Action-oriented title]
**Subtitle:** [So-what in one line]
**Audience / date / classification**

## Executive summary
- Finding…
- Finding…
### Recommendations
1. …
2. …

## [Takeaway section title]
Framing paragraph.

| KPI | Value | Context |
| --- | --- | --- |

**Implication:** …

## Decision / ask
- [ ] …
```

Adapt length and visuals to the chosen format; keep the skeleton’s logic.
