# Agency Creative Skills

Agent Skills pack for premium agency web work. Four focused skills with progressive disclosure (`SKILL.md` + `references/`).

Compatible with [Agent Skills](https://agentskills.io) / Cursor / Claude Code / Codex and similar harnesses.

## Skills

| Skill | Folder | Role |
| --- | --- | --- |
| **Agency Creative Studio** | `skills/agency-creative-studio` | Engagement **router** + shared brief + integration QA (not a monolith of specialist procedures) |
| **Premium Report Craft** | `skills/premium-report-craft` | Decision-ready reports, decks, PDFs — evidence ledger + format decision tree |
| **Technical Website Soundness** | `skills/technical-website-soundness` | Tech audits & launch readiness — passive security boundary, evidence records, calibrated scores |
| **GSC Growth Operator** | `skills/gsc-growth-operator` | Google Search Console performance, indexation diagnostics, sitemap triage, page/site SEO and operating reports |

The four folders above are bundled. GSC’s CSV/sitemap utilities run locally with the standard library; Google API access, GA4, PageSpeed/CrUX, Ahrefs/Bing, live technical checks, and rendering are optional integrations or specialist handoffs with explicit evidence states.

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
npx skills add <owner>/<repo> --skill gsc-growth-operator
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
- GSC performance, indexing/coverage, sitemap, CTR, content decay, cannibalization, organic reports → **GSC Growth Operator**
- Single headline, one component, isolated motion → specialist skills (do **not** activate ACS)

Optional companion installs (SEO/CRO, motion, etc.) belong in this README / CATALOG — never as hard requirements inside skill bodies.

## Next steps

Ship the contracts already on `main`. Do not add another skill or a Search Console API client until these are true.

1. **Enforce routing in CI.** `tests/routing-cases.yaml` is unused. `scripts/validate_pack.py` should fail if a case’s expected owner is missing from `AGENTS.md` or `ACCEPTANCE-TESTS.md`, and if a skill description lacks both a use trigger and a do-not-use trigger. This is a static check, not a model eval.
2. **Validate one artifact against the schema.** Add a fixture finding and a fixture handoff, and fail CI if they do not match `contracts/artifact-schemas.json`. Point the schema `$id` at this repository, not a GitHub Pages host that does not exist.
3. **Bring GSC templates up to that schema.** `templates/weekly-report.md` and `templates/site-audit.md` predate the contract. `references/indexing-playbook.md` needs rows for manual actions, security issues, and the links report, with an explicit `not evaluated` state. One finding ID, one owner, one evidence record.
4. **Decide [pull request #2](https://github.com/617-East-Trust/agency-creative-skills/pull/2) before more analyzer work.** `feat/gsc-remediation-controller` is the execution layer for `contracts/approval-and-change-control.md`. Merge it only if it shows the exact property and URLs, saves before-state, requires explicit approval, makes one reversible change, and records the recheck. Close it if it submits anything by default.
5. **Add two examples, not a new catalog.** One completed indexing evidence record that hands live headers to Technical Website Soundness. One Premium Report Craft handoff that consumes a finished GSC analysis and does not rerun it.

Out of this pass: topic clustering, GA4 channel setup, CrUX fetch, and a Search Console API client. Those stay agent procedures or optional integrations until the items above are enforced.

## License

MIT
