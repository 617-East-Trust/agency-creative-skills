# GSC remediation controller design

## Decision

Extend `gsc-growth-operator` from evidence-led recommendations to a **human-gated remediation controller**. It may orchestrate approved Search Console sitemap actions, repository pull requests, and production adapters; it must never autonomously deploy or submit an external action.

## State machine

```text
observed → planned → approval_requested → approved → snapshotted
→ executed → immediately_verified → recrawl_recheck_pending → closed
                               ↘ rollback_required / blocked
```

One remediation plan maps to one finding and one coherent action. A plan records exact targets and payload, owner, impact, uncertainty, before-state, rollback, verification, approval, execution environment, and recheck criteria.

## Adapter boundary

- **GSC:** Submit or delete one sitemap only with OAuth scope `webmasters`; `webmasters.readonly` remains audit-only. URL Inspection is read-only. Never use Indexing API for ordinary web pages.
- **GitHub:** Create a branch and pull request containing a small reversible change, test evidence, and rollback commit/revert instruction. A PR is not a production deployment.
- **Cloudflare/CMS/deployer:** Run only after the plan identifies the exact account, zone/site/environment, adapter, payload, and rollback. The human approval must cover that exact target.

The controller uses the same plan contract in Sandbox, Windows, Cloud VPS, or Termux. A capability is unavailable until the active environment has the required connector, credentials, and test commands.

## Safety gates

1. No approval means no write.
2. No preflight snapshot, rollback, or immediate verification means no execution.
3. No write scope means no GSC sitemap change.
4. No selected account/zone/environment means no production adapter call.
5. No live technical proof means no redirect, canonical, robots, content, or deploy action.
6. Recheck after recrawl records an outcome; it never promises an indexation date.

## Deliverables

- Lean skill workflow and routing changes.
- `remediation-control.md` procedure.
- Markdown and JSON remediation-plan templates.
- Deterministic validator and regression tests.
- Shared artifact-schema extension and routing/acceptance updates.
