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
    references/          # data contracts, indexing, operations, integrations, remediation controls
    scripts/             # CSV/sitemap analysis, remediation-plan validation, and dry-run-by-default approved GSC sitemap executor
    templates/           # weekly review, site audit, indexing and remediation records
```

Each skill directory name must match the `name` field in that skill's YAML frontmatter (kebab-case). Keep `SKILL.md` lean (target ~90–150 lines). Put long procedures in `references/` and load them only when needed.

**Install recipes** (`npx skills add …`, marketplace commands) live in `README.md` / setup docs — **not** in operational `SKILL.md` files.

## Install targets

Skills install to `.agents/skills/` (cross-agent) and/or `.claude/skills/` / `.cursor/skills/` depending on the harness.

## Ownership and handoffs

### Static routing owner IDs

`tests/routing-cases.yaml` uses the following stable owner IDs. The external `copy-specialist` route is intentionally not bundled in this pack.

- `agency-creative-studio`
- `gsc-growth-operator`
- `technical-website-soundness`
- `premium-report-craft`
- `copy-specialist`

| Ask type | Owner | Boundary |
| --- | --- | --- |
| Complex multi-discipline engagement | `agency-creative-studio` | Owns shared brief, specialist routing, and integrated QA—not specialist analysis. |
| Search Console performance, indexation, sitemap/URL Inspection diagnosis, remediation plan, approved sitemap actions, and post-recrawl recheck | `gsc-growth-operator` | Owns GSC evidence and human-gated action ledger; does not invent production proof. |
| Live headers, robots/canonical verification, redirects, PageSpeed/CrUX, deploy/rollback, and launch go/no-go | `technical-website-soundness` | Owns production-surface technical proof and safe implementation checks; supports GSC remediation preflight. |
| Exact repository, Cloudflare, CMS, or deploy action | Named approved adapter owner | Executes only the approved remediation-plan payload after preflight and capability checks. |
| Decision-ready report / deck / PDF | `premium-report-craft` | Turns verified specialist input into a client narrative; does not rerun GSC or technical audits. |

For a “not indexed” request, start with **GSC Growth Operator** when Search Console/URL Inspection/coverage evidence is available or requested. Hand off live header, canonical, robots, rendering, deployment, or PageSpeed verification to **Technical Website Soundness**. For a “fix this verified indexing or sitemap issue” request, GSC Growth Operator creates one remediation plan, validates it, asks for explicit approval, then routes the exact action through the approved adapter.

Use the shared machine-readable contracts in `contracts/artifact-schemas.json` and the read-only-by-default change policy in `contracts/approval-and-change-control.md`. Every handoff carries the brief ID, finding IDs, sources, limitations, requested output, owner, and completion criteria.
