#!/usr/bin/env python3
"""Execute one approved Search Console sitemap submit/delete action.

The default is a dry run. --execute requires a validated executable plan, a matching
--confirm-plan-id, OAuth scope https://www.googleapis.com/auth/webmasters, and the
standard GSC credential environment variables. The script never writes credentials
or access tokens to output artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from validate_remediation_plan import validate

TOKEN_URL = "https://oauth2.googleapis.com/token"
API_ROOT = "https://www.googleapis.com/webmasters/v3/sites"
WRITE_SCOPE = "https://www.googleapis.com/auth/webmasters"


def request_json(url: str, method: str, token: str, payload: bytes | None = None) -> tuple[int, dict[str, Any] | None]:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    request = Request(url, data=payload, headers=headers, method=method)
    try:
        with urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8", "replace")
            return response.status, json.loads(raw) if raw.strip() else None
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            detail: dict[str, Any] | None = json.loads(raw)
        except json.JSONDecodeError:
            detail = {"raw": raw[:1000]}
        return exc.code, detail


def refresh_access_token() -> tuple[str, list[str]]:
    required = [
        "GOOGLE_SEARCH_CONSOLE_CLIENT_ID",
        "GOOGLE_SEARCH_CONSOLE_CLIENT_SECRET",
        "GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN",
    ]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise ValueError("missing credential environment variable(s): " + ", ".join(missing))
    body = urllib.parse.urlencode(
        {
            "client_id": os.environ["GOOGLE_SEARCH_CONSOLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_SEARCH_CONSOLE_CLIENT_SECRET"],
            "refresh_token": os.environ["GOOGLE_SEARCH_CONSOLE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        }
    ).encode()
    request = Request(TOKEN_URL, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    with urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    token = payload.get("access_token")
    if not isinstance(token, str) or not token:
        raise ValueError("token refresh did not return an access token")
    return token, str(payload.get("scope", "")).split()


def action_url(property_id: str, sitemap_url: str) -> str:
    return f"{API_ROOT}/{urllib.parse.quote(property_id, safe='')}/sitemaps/{urllib.parse.quote(sitemap_url, safe='')}"


def sitemap_list_url(property_id: str) -> str:
    return f"{API_ROOT}/{urllib.parse.quote(property_id, safe='')}/sitemaps"


def summarize_list(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    items = (payload or {}).get("sitemap", [])
    if not isinstance(items, list):
        return []
    return [
        {
            "path": item.get("path"),
            "lastSubmitted": item.get("lastSubmitted"),
            "lastDownloaded": item.get("lastDownloaded"),
            "warnings": item.get("warnings"),
            "errors": item.get("errors"),
        }
        for item in items
        if isinstance(item, dict)
    ]


def output(result: dict[str, Any], target: str | None) -> None:
    rendered = json.dumps(result, indent=2) + "\n"
    if target:
        Path(target).write_text(rendered, encoding="utf-8")
    print(rendered, end="")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, help="Executable remediation-plan JSON")
    parser.add_argument("--confirm-plan-id", help="Must exactly match plan_id when using --execute")
    parser.add_argument("--execute", action="store_true", help="Perform the approved write; omit for dry run")
    parser.add_argument("--output", help="Optional JSON action record path")
    args = parser.parse_args()

    try:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        output({"result": "FAIL", "errors": [f"plan: {exc}"]}, args.output)
        return 2
    errors, summary = validate(plan, "executable")
    if errors:
        output({"result": "FAIL", "phase": "plan_validation", "errors": errors, "plan_id": plan.get("plan_id")}, args.output)
        return 2

    action = plan["action"]
    action_type = action["type"]
    if action_type not in {"gsc_sitemap_submit", "gsc_sitemap_delete"}:
        output({"result": "FAIL", "phase": "action_validation", "errors": ["plan action must be gsc_sitemap_submit or gsc_sitemap_delete"], "plan_id": plan["plan_id"]}, args.output)
        return 2
    target = action["target"]
    property_id, sitemap_url = target["property"], target["sitemap_url"]
    method = "PUT" if action_type == "gsc_sitemap_submit" else "DELETE"
    record: dict[str, Any] = {
        "plan_id": plan["plan_id"],
        "finding_id": plan["finding_id"],
        "action_type": action_type,
        "property": property_id,
        "sitemap_url": sitemap_url,
        "method": method,
        "result": "DRY_RUN",
        "write_performed": False,
        "plan_sha256": summary["plan_sha256"],
    }
    if not args.execute:
        record["next_step"] = "Obtain current human approval, then rerun with --execute --confirm-plan-id matching this plan."
        output(record, args.output)
        return 0
    if args.confirm_plan_id != plan["plan_id"]:
        output(record | {"result": "FAIL", "errors": ["--confirm-plan-id must exactly match plan_id"]}, args.output)
        return 2

    try:
        token, scopes = refresh_access_token()
    except (OSError, ValueError, HTTPError, json.JSONDecodeError) as exc:
        output(record | {"result": "FAIL", "phase": "oauth", "errors": [str(exc)]}, args.output)
        return 2
    if WRITE_SCOPE not in scopes:
        output(record | {"result": "BLOCKED", "phase": "scope", "required_scope": WRITE_SCOPE, "granted_scopes": scopes, "errors": ["write scope unavailable; no action was performed"]}, args.output)
        return 2

    before_status, before_payload = request_json(sitemap_list_url(property_id), "GET", token)
    if before_status != 200:
        output(record | {"result": "FAIL", "phase": "before_state", "http_status": before_status, "api_error": before_payload, "errors": ["could not capture sitemap before-state; no action was performed"]}, args.output)
        return 2
    action_status, action_payload = request_json(action_url(property_id, sitemap_url), method, token)
    after_status, after_payload = request_json(sitemap_list_url(property_id), "GET", token)
    record.update(
        {
            "result": "EXECUTED" if 200 <= action_status < 300 else "FAIL",
            "write_performed": 200 <= action_status < 300,
            "before_state": summarize_list(before_payload),
            "action_http_status": action_status,
            "action_response": action_payload,
            "after_state_http_status": after_status,
            "after_state": summarize_list(after_payload),
            "immediate_verification_required": plan["verification"]["immediate"],
            "recrawl_recheck_required": plan["verification"]["recrawl"],
        }
    )
    output(record, args.output)
    return 0 if record["result"] == "EXECUTED" and after_status == 200 else 2


if __name__ == "__main__":
    raise SystemExit(main())
