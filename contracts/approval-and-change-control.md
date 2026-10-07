# Approval and change-control policy

Apply this policy across all skills. Analysis is read-only by default; a launch review, audit, or recommendation is **not** approval to deploy or submit anything.

## Before a production or external action

1. Show the exact target environment/property, URLs, files/configuration, and proposed change.
2. State impact, known uncertainty, owner, rollback method, and post-change verification.
3. Save the before-state: relevant headers/source, configuration, inspection/sitemap state, evidence record, and timestamp.
4. Obtain explicit approval for production changes or external submissions.
5. Execute one coherent, reversible change set through the approved path.
6. Verify production behavior and record the outcome against the original finding ID.

## Actions that require explicit approval

- Production deploys, redirects, robots/canonical/noindex changes, DNS/CDN/security-header changes
- Sitemap submissions, URL indexing requests, or other Console actions
- Changes to analytics, conversion, CRM, or attribution configuration
- Any external publication, account permission, billing, or irreversible deletion

## Artifact identity

Every specialist handoff contains a brief ID (when an engagement brief exists), finding IDs, evidence sources, limitations, requested output, owner, and completion criteria. A finding has one authoritative evidence record and one remediation owner; other skills reference it rather than recreate it.
