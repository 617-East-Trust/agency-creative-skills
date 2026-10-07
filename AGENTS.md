# Agency Creative Skills

This repository contains Agent Skills following https://agentskills.io/specification.

## Layout

```text
skills/
  agency-creative-studio/
    SKILL.md
    references/          # engagement-workflow, creative-review-rubric, growth-routing
  premium-report-craft/
    SKILL.md
    references/          # evidence-ledger, report-layouts, deck-narrative
  technical-website-soundness/
    SKILL.md
    references/          # audit-evidence-protocol, framework-baselines, launch-recheck
  gsc-growth-operator/
    SKILL.md
    references/          # data contracts, indexing, operations, integrations, catalog map
    scripts/             # CSV/sitemap analysis only; no bundled Google credential client
    templates/           # weekly review, site audit, indexing evidence record
```

Each skill directory name must match the `name` field in that skill's YAML frontmatter (kebab-case).

Keep `SKILL.md` lean (target ~90–150 lines). Put long procedures in `references/` and load them only when needed.

**Install recipes** (`npx skills add …`, marketplace commands) live in `README.md` / setup docs — **not** in operational `SKILL.md` files.

## Install targets

Skills install to `.agents/skills/` (cross-agent) and/or `.claude/skills/` / `.cursor/skills/` depending on the harness.

## Ownership and handoffs

| Ask type | Owner | Boundary |
| --- | --- | --- |
| Complex multi-discipline engagement | `agency-creative-studio` | Owns shared brief, specialist routing, and integrated QA—not specialist analysis. |
| Search Console query/page performance, CTR, declines, decay, cannibalization, URL Inspection, coverage, and sitemap-to-inspection correlation | `gsc-growth-operator` | Owns GSC evidence and indexation diagnosis; accepts live technical evidence from Technical Website Soundness. |
| Live HTTP headers, robots/canonical verification, redirects, PageSpeed/CrUX collection, security headers, deploy/rollback, and launch go/no-go | `technical-website-soundness` | Owns production-surface technical proof and safe implementation checks; does not interpret GSC property data. |
| Decision-ready report / deck / PDF | `premium-report-craft` | Turns verified specialist input into a client narrative; does not rerun GSC or technical audits. |

For a “not indexed” request, start with **GSC Growth Operator** when Search Console/URL Inspection/coverage evidence is available or requested. Hand off live header, canonical, robots, rendering, deployment, or PageSpeed verification to **Technical Website Soundness**. For a “slow page” request, start with **Technical Website Soundness**; GSC may supply impact context but does not collect performance evidence.

Use the shared machine-readable contracts in `contracts/artifact-schemas.json` and the read-only-by-default change policy in `contracts/approval-and-change-control.md`. Every handoff carries the brief ID, finding IDs, sources, limitations, requested output, owner, and completion criteria.
