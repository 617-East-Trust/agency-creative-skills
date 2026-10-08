#!/usr/bin/env python3
"""Regression tests for the human-gated remediation-plan validator."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
VALIDATOR = TEST_DIR.parent / "scripts" / "validate_remediation_plan.py"


def base_plan() -> dict:
    return {
        "schema_version": 1,
        "plan_id": "GSC-EXAMPLE-001",
        "finding_id": "GSC-EXAMPLE-001",
        "status": "approved",
        "action": {
            "type": "github_pull_request",
            "owner": "Technical Website Soundness",
            "target": {
                "environment": "production",
                "repository": "owner/repository",
                "branch": "fix/example",
                "files": ["hosting/redirects.conf"],
            },
            "payload": {"summary": "Add one path-preserving redirect."},
        },
        "risk": {"impact": "Affects host routing.", "known_uncertainty": "Form behavior requires smoke testing."},
        "preflight": {
            "captured_at": "2026-10-07T00:00:00Z",
            "passed": True,
            "evidence": ["URL Inspection", "redirect matrix"],
            "checks": ["Core paths mapped", "rollback revision available"],
        },
        "rollback": {"method": "Revert the focused commit.", "owner": "Technical Website Soundness", "trigger": "Any required route fails."},
        "verification": {
            "immediate": ["Check one-hop redirect and form path."],
            "recrawl": ["Reinspect after recrawl."],
            "success_condition": "Apex is selected after recrawl.",
        },
        "approval": {"required": True, "state": "approved", "approved_by": "human", "approved_at": "2026-10-07T00:01:00Z"},
        "execution": {"environment": "sandbox", "adapter": "github", "result": "not_started"},
    }


def run(plan: dict, stage: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "plan.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        return subprocess.run([sys.executable, str(VALIDATOR), "--plan", str(path), "--stage", stage], text=True, capture_output=True, check=False)


class RemediationPlanTests(unittest.TestCase):
    def test_executable_plan_passes(self) -> None:
        process = run(base_plan(), "executable")
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["action_type"], "github_pull_request")
        self.assertTrue(result["plan_sha256"])

    def test_execution_requires_explicit_approval(self) -> None:
        plan = base_plan()
        plan["approval"] = {"required": True, "state": "requested", "approved_by": "", "approved_at": ""}
        process = run(plan, "executable")
        self.assertEqual(process.returncode, 2)
        self.assertIn("explicit approved state", process.stdout)

    def test_disallows_indexing_api_and_secret_material(self) -> None:
        plan = base_plan()
        plan["action"]["type"] = "indexing_api_request"
        plan["action"]["payload"]["access_token"] = "ya29.example-secret"
        process = run(plan, "planned")
        self.assertEqual(process.returncode, 2)
        self.assertIn("unsupported or prohibited action", process.stdout)
        self.assertIn("credential-like keys", process.stdout)

    def test_cloudflare_requires_selected_account_zone_and_environment(self) -> None:
        plan = base_plan()
        plan["action"] = {"type": "cloudflare_deploy", "owner": "Technical Website Soundness", "target": {}, "payload": {"summary": "Change redirect rule."}}
        process = run(plan, "planned")
        self.assertEqual(process.returncode, 2)
        self.assertIn("action.target.account_id", process.stdout)
        self.assertIn("action.target.zone_id", process.stdout)
        self.assertIn("action.target.environment", process.stdout)


if __name__ == "__main__":
    unittest.main()
