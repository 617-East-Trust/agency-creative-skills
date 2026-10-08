# Remediation control and execution contract

Use this reference before a GSC write, repository change, Cloudflare/CMS action, or production deployment.

## State machine

```text
observed → planned → approval_requested → approved → snapshotted
→ executed → immediately_verified → recrawl_recheck_pending → closed
                               ↘ rollback_required / blocked
```

A plan has one finding ID and one coherent action. `blocked` preserves the reason; it is not a reason to substitute another action.

## Plan minimums

Validate `templates/remediation-plan.json` with `scripts/validate_remediation_plan.py`.

| Gate | Required evidence |
| --- | --- |
| Planned | Finding, exact target, exact payload, owner, impact/uncertainty, rollback, immediate and recrawl verification |
| Approval requested | Exact payload shown to the human; no hidden URLs, files, rules, or environment changes |
| Approved | Explicit human approval for this plan ID and payload in the current interaction |
| Snapshotted | Timestamped before-state: relevant GSC/URL Inspection state, live proof, configuration/revision, and test baseline |
| Executable | Required adapter and write scope are present; preflight passed; one action only; rollback is actionable |
| Closed | Immediate verification and later recheck recorded against the original finding |

The validator checks plan structure, not whether a person actually approved. The agent must obtain the approval itself.

## Action classes and capabilities

| Action type | Required capability | Allowed execution | Never infer |
| --- | --- | --- | --- |
| `gsc_sitemap_submit` | GSC OAuth `webmasters` write scope | One `PUT /webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` with no body | Submission means indexed |
| `gsc_sitemap_delete` | GSC OAuth `webmasters` write scope | One `DELETE` against the exact property/sitemap | Deletion repairs a site issue |
| `github_pull_request` | Authorized repository and branch/PR capability | Branch, focused change, tests, PR, rollback/revert instruction | PR means deployed |
| `cloudflare_deploy` | Exact selected account, zone, and Cloudflare adapter capability | One approved rule/config change and captured prior state | Any accessible account is the right account |
| `cms_publish` | Exact CMS/site/environment and publish/revision capability | One approved content/config revision | Publishing means Google will crawl/index it |

`webmasters.readonly` permits analysis and URL Inspection, but not sitemap submit/delete. Google’s general Indexing API is prohibited unless page eligibility is explicitly proven for JobPosting or BroadcastEvent.

## Adapter preflight

### GSC sitemap action

1. Record property, current sitemap list/status, exact sitemap URL, purpose, and expected non-guaranteed outcome.
2. Confirm a `webmasters` (not `webmasters.readonly`) token.
3. Validate the sitemap URL and intended canonical host through supplied technical evidence.
4. Obtain approval. Execute one submit/delete request.
5. Record HTTP/API result and re-list sitemap state. Recheck coverage/Inspection later.

Use `scripts/gsc_sitemap_action.py` for this action. It defaults to a validated dry run and only performs a write with `--execute --confirm-plan-id <exact-plan-id>`. It captures sitemap list state before and after the one `PUT`/`DELETE`, blocks `webmasters.readonly`, and never writes tokens to its output.

### GitHub pull request

1. Confirm repository, branch strategy, target deployment environment, files, and test commands.
2. Capture affected production behavior and current revision. Require Technical Website Soundness proof for redirects, canonicals, robots, or headers.
3. Make one focused commit on a branch. Run relevant tests and capture output.
4. Open a PR with plan ID, finding ID, before-state, change, tests, rollback/revert, and deployment verification.
5. Treat merge/deployment as a separate approval when it can affect production.

### Cloudflare / CMS / deployer

1. Require exact account and zone/site/environment. Ask the human to choose when multiple accounts exist.
2. Capture current rule/config/revision, related page behavior, and rollback mechanism.
3. Show the exact operation and material settings in the approval request.
4. Apply one reversible change, run immediate production checks, and restore before-state if verification fails.
5. Keep the action ledger current and schedule/perform the recrawl recheck without predicting a date.

## Technical proof requirement

Before redirect, canonical, robots, `noindex`, sitemap-generator, CDN, or production-content changes, require Technical Website Soundness evidence for the exact target:

```text
final response and redirect chain
X-Robots-Tag and meta robots
user canonical and rendered canonical
robots.txt applicability
sitemap presence and internal-link context
form/conversion-path smoke test where applicable
current configuration/revision and rollback path
```

## Execution environments

The plan contract is portable. Run it in the active **Sandbox**, **Windows**, **Cloud VPS**, or **Termux** environment only when that environment has the named adapter, credentials, and verification tools. Do not copy secrets between environments or assume a connector is available after switching devices.

## Action ledger record

After every state transition, append: plan ID, finding ID, timestamp, actor/adapter, exact target, status, before/after artifact locations, result, rollback status, immediate verification, and recheck due condition. Keep credentials and raw tokens out of the ledger.
