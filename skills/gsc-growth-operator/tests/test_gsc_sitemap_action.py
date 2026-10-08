#!/usr/bin/env python3
"""Regression tests for the dry-run-only path of the GSC sitemap executor."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
EXECUTOR = TEST_DIR.parent / "scripts" / "gsc_sitemap_action.py"


def executable_plan() -> dict:
    return {
        "schema_version": 1,
        "plan_id": "GSC-EXAMPLE-SITEMAP-001",
        "finding_id": "GSC-EXAMPLE-001",
        "status": "approved",
        "action": {
            "type": "gsc_sitemap_submit",
            "owner": "GSC Growth Operator",
            "target": {"property": "sc-domain:example.com", "sitemap_url": "https://example.com/sitemap.xml"},
            "payload": {"summary": "Submit one verified sitemap."},
        },
        "risk": {"impact": "Adds one sitemap submission.", "known_uncertainty": "Submission does not guarantee indexation."},
        "preflight": {"captured_at": "2026-10-07T00:00:00Z", "passed": True, "evidence": ["sitemap audit"], "checks": ["write scope checked before execution"]},
        "rollback": {"method": "Delete the exact sitemap submission.", "owner": "GSC Growth Operator", "trigger": "Incorrect sitemap submitted."},
        "verification": {"immediate": ["Re-list sitemap state."], "recrawl": ["Reinspect sample URL after crawl."], "success_condition": "Sitemap remains accepted without errors."},
        "approval": {"required": True, "state": "approved", "approved_by": "human", "approved_at": "2026-10-07T00:01:00Z"},
        "execution": {"environment": "sandbox", "adapter": "gsc_sitemap_action", "result": "not_started"},
    }


def run(plan: dict, *extra: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "plan.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        return subprocess.run([sys.executable, str(EXECUTOR), "--plan", str(path), *extra], text=True, capture_output=True, check=False)


class GscSitemapActionTests(unittest.TestCase):
    def test_default_is_validated_dry_run_without_credentials(self) -> None:
        process = run(executable_plan())
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["result"], "DRY_RUN")
        self.assertFalse(result["write_performed"])
        self.assertEqual(result["method"], "PUT")

    def test_rejects_non_gsc_plan_before_any_credential_use(self) -> None:
        plan = executable_plan()
        plan["action"]["type"] = "github_pull_request"
        plan["action"]["target"] = {"repository": "owner/repository", "branch": "fix/example", "files": ["x"]}
        process = run(plan)
        self.assertEqual(process.returncode, 2)
        self.assertIn("plan action must be gsc_sitemap_submit", process.stdout)

    def test_requires_approved_executable_plan_even_for_dry_run(self) -> None:
        plan = executable_plan()
        plan["approval"]["state"] = "requested"
        process = run(plan)
        self.assertEqual(process.returncode, 2)
        self.assertIn("explicit approved state", process.stdout)


if __name__ == "__main__":
    unittest.main()
