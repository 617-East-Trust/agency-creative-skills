# Authorized Search Console integration contract

This package ships local analyzers, **not** an OAuth client. Use an already-authorized connector, an approved internal client, or explicit exported files. Never paste credentials into skill artifacts, command history, or reports.

## Required capability declarations

Before calling a tool, record which of these capabilities it actually exposes:

| Capability | Use | Evidence state if unavailable |
| --- | --- | --- |
| Property list | Confirm correct GSC property | `not evaluated` |
| Search Analytics query | Property KPI or detailed query/page data | `not evaluated` |
| Pagination / export limits | Retrieve/describe row coverage | `unknown` if not documented |
| URL Inspection | Google-side index/coverage/canonical state | `not evaluated` |
| Sitemap list/submission state | GSC sitemap processing context | `not evaluated` |
| Manual actions | Confirm available Console status | `not evaluated` |
| Security issues | Confirm available Console status | `not evaluated` |
| Links report | Context for linking diagnosis | `not evaluated` |

Manual actions, security issues, and links may be visible only through the Search Console UI or a particular connector, not a generic API client. Do not claim an API feature exists without the tool’s own documentation.

## Request contract

For any direct integration call, preserve:

```text
Property: exact sc-domain or URL-prefix property
Endpoint/tool and version: exact name
Filters: search type, country, device, query/page dimensions
Dates: start, end, freshness treatment
Pagination: requested limit, retrieved count, known cap/omission
Raw artifact: saved/linked location and access controls
```

For Search Analytics queries, paginate deliberately and report the requested dimensions, row limit, and retrieved count. Never call a detailed response the complete property total unless the integration explicitly returns it as one.

## External action policy

Read-only retrieval is the default. Before a sitemap submission or URL indexing request, show the exact property, URLs/sitemap, reason, and expected non-guaranteed result; require explicit approval; save before-state; then recheck and record the outcome. In the full pack, follow the shared approval-and-change-control contract; in a standalone install, preserve these same steps in the evidence record.
