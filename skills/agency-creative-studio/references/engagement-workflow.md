# Engagement workflow — full pipeline stages and gates

Use when Agency Creative Studio runs `new-build`, `campaign`, or `launch-integration` across multiple disciplines.

## Stages

### 1. Discovery
- Confirm decision, audience, offer, success metric, constraints
- Inventory URLs, brand assets, analytics access, competitors
- Decide whether a shared engagement brief is required (2+ disciplines, client/board pack, or launch decision)

### 2. Creative direction
- Produce a one-pager: tension, audience belief shift, visual system (type/color/motion posture), section narrative
- Ban generic AI UI patterns
- **Gate A:** If wrong direction would waste significant build (custom motion/3D, multi-page IA, client presentation), pause for approval. Otherwise list assumptions and proceed.

### 3. Scope / IA
- Page or section map; primary journeys; content inventory
- Deliverable list with owners (design, copy, growth, technical, report)
- Explicit out-of-scope list

### 4. Specialist execution
- Route per the SKILL.md routing contract
- Keep the engagement brief as the single source of truth for assumptions
- Prefer working artifacts over slideware about artifacts
- Growth: load `growth-routing.md` or a SEO/CRO specialist when present
- Technical: invoke Technical Website Soundness for `analyze` / `create` / `go`
- Report: invoke Premium Report Craft for client/board packs

### 5. Integrated QA
Run the Final integration QA checklist in SKILL.md. Do not ship creative that fails CWV/a11y basics or unverified claims.

### 6. Delivery
- Package deliverables by audience (internal vs client)
- List open assumptions and residual risks
- Optional: client narrative via Premium Report Craft; launch verdict via Technical Website Soundness `go`

## Path variants

| Path | Extra notes |
| --- | --- |
| `review-existing` | Start with creative-review-rubric; hand off redesign brief into direction stage if rebuild follows |
| `new-build` | Do not skip direction or growth plumbing on marketing launches |
| `campaign` | Lock offer + primary CTA before channel variants; keep message match |
| `launch-integration` | Technical `go` sequence is mandatory; creative polish does not override P0/P1 |

## Anti-patterns
- Parallel specialists with conflicting assumptions
- Approving nothing and rebuilding everything twice
- Calling the engagement “done” without integration QA
