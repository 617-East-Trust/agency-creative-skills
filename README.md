# Agency Creative Skills

Agent Skills pack for premium agency web work. Four focused skills with progressive disclosure (`SKILL.md` + `references/`).

Compatible with [Agent Skills](https://agentskills.io) / Cursor / Claude Code / Codex and similar harnesses.

## Skills

| Skill | Folder | Role |
| --- | --- | --- |
| **Agency Creative Studio** | `skills/agency-creative-studio` | Engagement **router** + shared brief + integration QA (not a monolith of specialist procedures) |
| **Premium Report Craft** | `skills/premium-report-craft` | Decision-ready reports, decks, PDFs — evidence ledger + format decision tree |
| **Technical Website Soundness** | `skills/technical-website-soundness` | Tech audits & launch readiness — passive security boundary, evidence records, calibrated scores |
| **GSC Growth Operator** | `skills/gsc-growth-operator` | GSC performance/indexation diagnosis plus human-gated remediation plans, approved sitemap actions, and adapter-controlled repository/production changes |

The four folders above are bundled. GSC’s CSV/sitemap utilities, remediation-plan validator, and a dry-run-by-default approved sitemap executor run locally with the standard library. CI contract validation uses `requirements-dev.txt`. Google API access, GSC write scope, GitHub, Cloudflare, CMS, GA4, PageSpeed/CrUX, live technical checks, and rendering are optional integrations or specialist handoffs with explicit evidence states.

> **Change-control boundary:** The pack is read-only by default. It can execute a sitemap write, pull request, or production adapter action only after it has captured before-state, validated one remediation plan, shown the exact payload and rollback, and obtained explicit human approval. A Search Console submit/delete call does not guarantee crawling or indexation; a PR does not mean deployed.

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
- GSC performance, indexing/coverage, sitemap, CTR, content decay, cannibalization, or approved remediation planning → **GSC Growth Operator**
- Single headline, one component, isolated motion → specialist skills (do **not** activate ACS)

Optional companion installs (SEO/CRO, motion, etc.) belong in this README / CATALOG — never as hard requirements inside skill bodies.

## Enforced safeguards and current scope

The original main-branch hardening checklist is now enforced:

1. `scripts/validate_pack.py` reads `tests/routing-cases.yaml`, verifies route owner IDs in `AGENTS.md` and `ACCEPTANCE-TESTS.md`, and requires each bundled skill description to include both a use trigger and a do-not-use boundary. This remains a static check, not a model evaluation.
2. CI validates a finding and handoff fixture against `contracts/artifact-schemas.json`; the schema `$id` now points at this repository’s raw source.
3. GSC weekly/site-audit/indexing templates carry a finding ID, owner, evidence record, rollback, verification, and explicit Console-health state (`clear`, issue detail, or `not evaluated`).
4. [PR #2](https://github.com/617-East-Trust/agency-creative-skills/pull/2) is merged. Its constrained sitemap executor stays dry-run by default and requires an approved plan, matching confirmation ID, write scope, before-state, and recheck.
5. Examples now show an indexing handoff to Technical Website Soundness and a finished GSC analysis handoff to Premium Report Craft without rerunning specialist work.

Out of scope: topic clustering, GA4 channel setup, CrUX fetch, and broad generic indexing requests. Those remain agent procedures or optional integrations; the Indexing API remains restricted to eligible JobPosting or BroadcastEvent pages.

## License

MIT
