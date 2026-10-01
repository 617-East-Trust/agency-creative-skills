# Agency Creative Skills

Agent Skills pack for premium agency web work. Three focused skills with progressive disclosure (`SKILL.md` + `references/`).

Compatible with [Agent Skills](https://agentskills.io) / Cursor / Claude Code / Codex and similar harnesses.

## Skills

| Skill | Folder | Role |
| --- | --- | --- |
| **Agency Creative Studio** | `skills/agency-creative-studio` | Engagement **router** + shared brief + integration QA (not a monolith of specialist procedures) |
| **Premium Report Craft** | `skills/premium-report-craft` | Decision-ready reports, decks, PDFs — evidence ledger + format decision tree |
| **Technical Website Soundness** | `skills/technical-website-soundness` | Tech audits & launch readiness — passive security boundary, evidence records, calibrated scores |

Also see [CATALOG.md](./CATALOG.md) for curated third-party skill sources, and [ACCEPTANCE-TESTS.md](./ACCEPTANCE-TESTS.md) for routing acceptance prompts.

## Structure

```text
skills/<skill-name>/
  SKILL.md              # Lean operational skill (~90–150 lines)
  references/           # Long procedures (load only when needed)
```

Install recipes live **here in the README** (and setup docs) — not inside operational `SKILL.md` files.

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

## Routing quick map

- Multi-discipline brand/site/campaign/launch → **Agency Creative Studio**
- Standalone report/deck/PDF → **Premium Report Craft**
- PageSpeed/headers/crawl/security hygiene/launch go-no-go → **Technical Website Soundness**
- Single headline, one component, isolated motion → specialist skills (do **not** activate ACS)

Optional companion installs (SEO/CRO, motion, etc.) belong in this README / CATALOG — never as hard requirements inside skill bodies.

## License

MIT
