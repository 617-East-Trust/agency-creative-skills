# Authorized Search Console and remediation integration contract

The package ships deterministic analyzers and a remediation-plan validator, **not** an OAuth client or an autonomous deployment client. Use only an authorized connector, internal client, or explicit user-supplied export. Never put credentials in artifacts, plans, command history, or reports.

## Capability declaration

Before any call, record what the active connector/adapter actually exposes.

| Capability | Read-only scope | Write capability / required proof | Evidence state if unavailable |
| --- | --- | --- | --- |
| Property list / Search Analytics / URL Inspection | `webmasters.readonly` | No write required | `not evaluated` |
| Sitemap list/status | `webmasters.readonly` | No write required | `not evaluated` |
| Sitemap submit/delete | Not available | OAuth `https://www.googleapis.com/auth/webmasters`; exact property + sitemap + approval | `blocked` |
| Manual actions / security issues / links | Connector/UI dependent | No generic API assumption | `not evaluated` |
| GitHub PR | Repository read/write capability | Exact repository, branch, files, tests, rollback | `blocked` |
| Cloudflare/CMS/deploy | Adapter dependent | Exact selected account/zone/site/environment, before-state, rollback, approval | `blocked` |

Manual actions, security issues, and links may be visible only in Search Console UI or a particular connector. Never claim a generic API feature exists without verified documentation.

## Request record

For each direct API/adapter call, preserve:

```text
Plan and finding IDs
Property / account / zone / repository / site / environment
Endpoint or adapter and version
Exact payload or changed files/rules/revision
Dates, filters, dimensions, pagination, and limits for read calls
Before-state artifact and timestamp
Approval record, rollback, immediate verification, and recheck condition
Result artifact and access controls
```

Detailed Search Analytics exports are never property totals unless the integration explicitly returns metrics-only totals.

## GSC sitemap writes

Google’s Search Console API documents the following write operations:

```text
PUT    https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
DELETE https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
```

Both require `https://www.googleapis.com/auth/webmasters` and have no request body. URL Inspection is not an indexing-submission endpoint. Do not use the Indexing API for ordinary web pages; require explicit eligibility for JobPosting or BroadcastEvent pages.

Before either method:

1. Validate a single remediation plan at `planned` stage.
2. Show exact property, sitemap URL, purpose, non-guaranteed outcome, and rollback to the human.
3. Obtain current explicit approval and record it in the plan.
4. Snapshot the sitemap list/status, validate write scope, and revalidate the plan at `executable` stage.
5. Execute one method, save the response/result, re-list sitemap state, and schedule/perform a later URL Inspection or coverage recheck.

The bundled `scripts/gsc_sitemap_action.py` implements this narrow path. It is dry-run by default and requires both `--execute` and a matching `--confirm-plan-id` before it refreshes credentials or sends a write. It validates the plan at `executable` stage, blocks missing write scope, captures sitemap state before/after, and emits a sanitized action record.

## Production adapter policy

A repository PR, Cloudflare rule, CMS publish, or deployment action requires the remediation-control gates. Require Technical Website Soundness proof for redirects, canonical/robots/noindex behavior, headers, or affected user paths. When multiple Cloudflare accounts or sites are accessible, ask the human to select the correct account/zone rather than inferring it.

The user’s approval covers only the exact displayed plan ID, target, payload, and rollback. A changed target, account, environment, file set, or rollout requires a new approval.
