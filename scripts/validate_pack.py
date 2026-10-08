#!/usr/bin/env python3
"""Lightweight, dependency-free validation for the Agency Creative Skills pack."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter fence")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("unclosed YAML frontmatter") from exc
    values = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("no skills/*/SKILL.md files found")
    for skill in skills:
        try:
            metadata = frontmatter(skill)
        except ValueError as exc:
            errors.append(f"{skill.relative_to(root)}: {exc}")
            continue
        if metadata.get("name") != skill.parent.name:
            errors.append(f"{skill.relative_to(root)}: frontmatter name must equal directory name")
        if "description" not in metadata:
            errors.append(f"{skill.relative_to(root)}: missing description field")
        if len(skill.read_text(encoding="utf-8").splitlines()) > 500:
            errors.append(f"{skill.relative_to(root)}: SKILL.md exceeds 500 lines")
        text = skill.read_text(encoding="utf-8")
        for relative in re.findall(r"(?:references|templates|scripts)/[A-Za-z0-9_./-]+", text):
            candidate = skill.parent / relative.rstrip(".,;:)")
            if not candidate.exists():
                errors.append(f"{skill.relative_to(root)}: referenced file missing: {relative}")

    plugin = json.loads((root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    marketplace_plugin = next((item for item in marketplace.get("plugins", []) if item.get("name") == plugin.get("name")), None)
    if not marketplace_plugin:
        errors.append("marketplace.json lacks the plugin declared in plugin.json")
    elif marketplace_plugin.get("version") != plugin.get("version"):
        errors.append("plugin.json and marketplace.json versions differ")

    catalog = (root / "CATALOG.md").read_text(encoding="utf-8")
    if "sand-workflow:" in catalog:
        errors.append("CATALOG.md contains non-portable sand-workflow links")
    for skill in skills:
        relative = f"skills/{skill.parent.name}/SKILL.md"
        if relative not in catalog:
            errors.append(f"CATALOG.md missing local skill link: {relative}")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    for skill in skills:
        if skill.parent.name not in agents:
            errors.append(f"AGENTS.md missing skill: {skill.parent.name}")

    gsc = root / "skills" / "gsc-growth-operator"
    remediation_files = [
        gsc / "references" / "remediation-control.md",
        gsc / "templates" / "remediation-plan.md",
        gsc / "templates" / "remediation-plan.json",
        gsc / "scripts" / "validate_remediation_plan.py",
        gsc / "scripts" / "gsc_sitemap_action.py",
    ]
    for candidate in remediation_files:
        if not candidate.exists():
            errors.append(f"missing remediation asset: {candidate.relative_to(root)}")
    if not errors and gsc.exists():
        try:
            json.loads((root / "contracts" / "artifact-schemas.json").read_text(encoding="utf-8"))
            json.loads((gsc / "templates" / "remediation-plan.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"remediation JSON validation failed: {exc}")
        else:
            process = subprocess.run(
                [sys.executable, str(gsc / "scripts" / "validate_remediation_plan.py"), "--plan", str(gsc / "templates" / "remediation-plan.json"), "--stage", "planned"],
                text=True,
                capture_output=True,
                check=False,
            )
            if process.returncode:
                errors.append("remediation plan template failed validator: " + process.stdout.strip())

    if errors:
        print("Pack validation failed:")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print(f"Pack validation passed: {len(skills)} skills, aligned manifests, portable catalog links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
