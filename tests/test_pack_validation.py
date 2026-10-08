#!/usr/bin/env python3
"""Regression tests for static routing and artifact-contract guardrails."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_pack.py"


def cloned_pack() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    directory = tempfile.TemporaryDirectory()
    target = Path(directory.name) / "pack"
    shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return directory, target


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(root / "scripts" / "validate_pack.py"), str(root)], text=True, capture_output=True, check=False)


class PackValidationTests(unittest.TestCase):
    def test_current_pack_passes_static_validation(self) -> None:
        process = run(ROOT)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_missing_routing_owner_fails_validation(self) -> None:
        directory, clone = cloned_pack()
        self.addCleanup(directory.cleanup)
        agents = clone / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8").replace("`copy-specialist`", "copy-specialist"), encoding="utf-8")
        process = run(clone)
        self.assertEqual(process.returncode, 1)
        self.assertIn("AGENTS.md missing routing owner ID: copy-specialist", process.stdout)

    def test_invalid_contract_fixture_fails_validation(self) -> None:
        directory, clone = cloned_pack()
        self.addCleanup(directory.cleanup)
        fixture = clone / "tests" / "fixtures" / "artifacts" / "finding.json"
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        payload["condition"] = "unsupported"
        fixture.write_text(json.dumps(payload), encoding="utf-8")
        process = run(clone)
        self.assertEqual(process.returncode, 1)
        self.assertIn("artifact fixture does not match schema", process.stdout)


if __name__ == "__main__":
    unittest.main()
