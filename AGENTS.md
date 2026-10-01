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
```

Each skill directory name must match the `name` field in that skill's YAML frontmatter (kebab-case).

Keep `SKILL.md` lean (target ~90–150 lines). Put long procedures in `references/` and load them only when needed.

**Install recipes** (`npx skills add …`, marketplace commands) live in `README.md` / setup docs — **not** in operational `SKILL.md` files.

## Install targets

Skills install to `.agents/skills/` (cross-agent) and/or `.claude/skills/` / `.cursor/skills/` depending on the harness.

## Ownership

| Ask type | Owner |
| --- | --- |
| Complex multi-discipline engagement | `agency-creative-studio` |
| Decision-ready report / deck / PDF | `premium-report-craft` |
| Technical audit / create baselines / launch go | `technical-website-soundness` |
