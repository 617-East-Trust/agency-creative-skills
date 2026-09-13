# Agency Creative Skills

Agent Skills pack for premium agency web work: creative direction, motion/3D, conversion copy, growth (SEO/CRO/CTA/llms.txt), technical soundness, brand/site review, and client-ready reports.

Compatible with [Agent Skills](https://agentskills.io) / Cursor / Claude Code / Codex and similar harnesses.

## Skills

| Skill | Folder | Use when |
| --- | --- | --- |
| **Agency Creative Studio** | `skills/agency-creative-studio` | Ideate, design-web, motion, immersive-3d, copy, **growth**, report, review, full-pipeline |
| **Premium Report Craft** | `skills/premium-report-craft` | Beautiful, human, persuasive reports & decks |
| **Technical Website Soundness** | `skills/technical-website-soundness` | PageSpeed/CWV, security, SEO plumbing, launch go/no-go |

Also see [CATALOG.md](./CATALOG.md) for curated third-party skill sources discovered while building this pack.

## Install

### npx skills (Cursor / multi-agent)

```bash
npx skills add <owner>/<repo>
# or per skill:
npx skills add <owner>/<repo> --skill agency-creative-studio
npx skills add <owner>/<repo> --skill premium-report-craft
npx skills add <owner>/<repo> --skill technical-website-soundness
```

### Manual

Copy any folder under `skills/` into:

- Cursor: `.cursor/skills/` or `.agents/skills/`
- Claude Code: `.claude/skills/` or `~/.claude/skills/`

### Claude Code plugin marketplace

```text
/plugin marketplace add <owner>/<repo>
/plugin install agency-creative-skills@agency-creative-skills
```

## Modes quick map (Agency Creative Studio)

- `ideate` · `design-web` · `motion` · `immersive-3d` · `copy`
- `growth` — SEO, CRO, CTAs, llms.txt
- `review` — existing websites & brands
- `report` — hands off to Premium Report Craft
- `full-pipeline` — end-to-end including growth before launch QA

Deep perf/security/ops: use **Technical Website Soundness** (`analyze` | `create` | `go`).

## License

MIT
