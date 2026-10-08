#!/usr/bin/env python3
"""Validate a human-gated GSC remediation plan without executing any action."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED_STATUS = {
    "planned",
    "approval_requested",
    "approved",
    "snapshotted",
    "executed",
    "immediately_verified",
    "recrawl_recheck_pending",
    "closed",
    "rollback_required",
    "blocked",
}
ALLOWED_ACTIONS = {
    "gsc_sitemap_submit",
    "gsc_sitemap_delete",
    "github_pull_request",
    "cloudflare_deploy",
    "cms_publish",
}
ALLOWED_ENVIRONMENTS = {"sandbox", "windows", "cloud-vps", "termux", "manual"}
FORBIDDEN_KEY_PARTS = ("token", "secret", "password", "private_key", "api_key")
FORBIDDEN_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bya29\.[A-Za-z0-9._-]+"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}"),
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def scan_secrets(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_path = f"{path}.{key}" if path else key
            if any(part in key.casefold() for part in FORBIDDEN_KEY_PARTS):
                fail(errors, f"{key_path}: credential-like keys are forbidden in remediation plans")
            scan_secrets(item, key_path, errors)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_secrets(item, f"{path}[{index}]", errors)
    elif isinstance(value, str):
        if any(pattern.search(value) for pattern in FORBIDDEN_VALUE_PATTERNS):
            fail(errors, f"{path}: credential-like value is forbidden in remediation plans")


def require_string(plan: dict[str, Any], key: str, errors: list[str]) -> None:
    if not nonempty(plan.get(key)):
        fail(errors, f"{key}: required non-empty string")


def require_list(container: dict[str, Any], key: str, errors: list[str]) -> None:
    value = container.get(key)
    if not isinstance(value, list) or not value or not all(nonempty(item) for item in value):
        fail(errors, f"{key}: required non-empty string list")


def validate(plan: Any, stage: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["plan: top-level JSON object required"], {}
    scan_secrets(plan, "", errors)
    if plan.get("schema_version") != 1:
        fail(errors, "schema_version: must equal 1")
    for key in ("plan_id", "finding_id", "status"):
        require_string(plan, key, errors)
    if plan.get("status") not in ALLOWED_STATUS:
        fail(errors, f"status: unsupported value {plan.get('status')!r}")

    action = plan.get("action")
    if not isinstance(action, dict):
        fail(errors, "action: object required")
        action = {}
    action_type = action.get("type")
    if action_type not in ALLOWED_ACTIONS:
        fail(errors, f"action.type: unsupported or prohibited action {action_type!r}")
    require_string(action, "owner", errors)
    target = action.get("target")
    if not isinstance(target, dict):
        fail(errors, "action.target: object required")
        target = {}
    payload = action.get("payload")
    if not isinstance(payload, dict) or not payload:
        fail(errors, "action.payload: non-empty object required")
    if action_type in {"gsc_sitemap_submit", "gsc_sitemap_delete"}:
        if not nonempty(target.get("property")):
            fail(errors, "action.target.property: required for GSC sitemap action")
        if not nonempty(target.get("sitemap_url")):
            fail(errors, "action.target.sitemap_url: required for GSC sitemap action")
    if action_type == "github_pull_request":
        for key in ("repository", "branch"):
            if not nonempty(target.get(key)):
                fail(errors, f"action.target.{key}: required for GitHub pull request")
        require_list(target, "files", errors)
    if action_type == "cloudflare_deploy":
        for key in ("account_id", "zone_id", "environment"):
            if not nonempty(target.get(key)):
                fail(errors, f"action.target.{key}: required for Cloudflare deployment")
    if action_type == "cms_publish":
        for key in ("site", "environment", "revision"):
            if not nonempty(target.get(key)):
                fail(errors, f"action.target.{key}: required for CMS publish")

    risk = plan.get("risk")
    if not isinstance(risk, dict) or not nonempty(risk.get("impact")) or not nonempty(risk.get("known_uncertainty")):
        fail(errors, "risk: impact and known_uncertainty are required")
    preflight = plan.get("preflight")
    if not isinstance(preflight, dict):
        fail(errors, "preflight: object required")
        preflight = {}
    else:
        require_list(preflight, "evidence", errors)
        require_list(preflight, "checks", errors)
    rollback = plan.get("rollback")
    if not isinstance(rollback, dict) or not all(nonempty(rollback.get(k)) for k in ("method", "owner", "trigger")):
        fail(errors, "rollback: method, owner, and trigger are required")
    verification = plan.get("verification")
    if not isinstance(verification, dict):
        fail(errors, "verification: object required")
    else:
        require_list(verification, "immediate", errors)
        require_list(verification, "recrawl", errors)
        if not nonempty(verification.get("success_condition")):
            fail(errors, "verification.success_condition: required non-empty string")
    approval = plan.get("approval")
    if not isinstance(approval, dict) or approval.get("required") is not True:
        fail(errors, "approval.required: must be true")
        approval = {}
    approval_state = approval.get("state")
    if approval_state not in {"not_requested", "requested", "approved", "rejected"}:
        fail(errors, f"approval.state: unsupported value {approval_state!r}")
    execution = plan.get("execution")
    if not isinstance(execution, dict):
        fail(errors, "execution: object required")
        execution = {}
    elif execution.get("environment") not in ALLOWED_ENVIRONMENTS:
        fail(errors, f"execution.environment: unsupported value {execution.get('environment')!r}")

    if stage in {"approval", "executable"}:
        if approval_state != "approved" or not nonempty(approval.get("approved_by")) or not nonempty(approval.get("approved_at")):
            fail(errors, "approval stage: explicit approved state, approver, and timestamp required")
    if stage == "executable":
        if plan.get("status") not in {"approved", "snapshotted"}:
            fail(errors, "executable stage: status must be approved or snapshotted")
        if not nonempty(preflight.get("captured_at")) or preflight.get("passed") is not True:
            fail(errors, "executable stage: captured and passed preflight required")
        if not nonempty(execution.get("adapter")):
            fail(errors, "executable stage: execution.adapter required")

    redacted = json.dumps(plan, sort_keys=True, separators=(",", ":"))
    summary = {
        "result": "PASS" if not errors else "FAIL",
        "stage": stage,
        "plan_id": plan.get("plan_id"),
        "finding_id": plan.get("finding_id"),
        "action_type": action_type,
        "status": plan.get("status"),
        "plan_sha256": hashlib.sha256(redacted.encode()).hexdigest(),
        "errors": errors,
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, help="Path to a remediation-plan JSON file")
    parser.add_argument("--stage", choices=("planned", "approval", "executable"), default="planned")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()
    try:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"result": "FAIL", "errors": [f"plan: {exc}"]}, indent=2))
        return 2
    errors, summary = validate(plan, args.stage)
    rendered = json.dumps(summary, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
