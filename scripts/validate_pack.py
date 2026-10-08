#!/usr/bin/env python3
"""Dependency-light validation for the Agency Creative Skills pack."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - dependency is installed by CI
    Draft202012Validator = None
    FormatChecker = None


OWNER_FIELD = re.compile(r"^\s*(?:expected_owner|supporting_owner|input_owner):\s*([A-Za-z0-9_-]+)\s*$")


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter fence")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("unclosed YAML frontmatter") from exc
    values: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            index += 1
            continue
        key, value = match.group(1), match.group(2).strip()
        if value in {">", ">-", "|", "|-"}:
            blocks: list[str] = []
            index += 1
            while index < end and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
                if lines[index].strip():
                    blocks.append(lines[index].strip())
                index += 1
            values[key] = " ".join(blocks)
            continue
        values[key] = value
        index += 1
    return values


def owner_ids(path: Path) -> set[str]:
    owners: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = OWNER_FIELD.match(line)
        if match:
            owners.add(match.group(1))
    return owners


def validate_contract_fixtures(root: Path, errors: list[str]) -> None:
    schema_path = root / "contracts" / "artifact-schemas.json"
    fixtures = [
        root / "tests" / "fixtures" / "artifacts" / "finding.json",
        root / "tests" / "fixtures" / "artifacts" / "handoff.json",
    ]
    if Draft202012Validator is None or FormatChecker is None:
        errors.append("jsonschema dependency missing; install requirements-dev.txt before validation")
        return
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"artifact schema invalid: {exc}")
        return
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for fixture in fixtures:
        try:
            artifact = json.loads(fixture.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"artifact fixture invalid: {fixture.relative_to(root)}: {exc}")
            continue
        findings = sorted(validator.iter_errors(artifact), key=lambda item: list(item.path))
        for finding in findings:
            location = ".".join(str(item) for item in finding.absolute_path) or "root"
            errors.append(f"artifact fixture does not match schema: {fixture.relative_to(root)} at {location}: {finding.message}")


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
        description = metadata.get("description", "")
        if not description:
            errors.append(f"{skill.relative_to(root)}: missing description field")
        elif not re.search(r"\buse\b", description, re.IGNORECASE) or not re.search(r"\bdo not use\b", description, re.IGNORECASE):
            errors.append(f"{skill.relative_to(root)}: description must contain both a use trigger and a do-not-use boundary")
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

    agents_path = root / "AGENTS.md"
    acceptance_path = root / "ACCEPTANCE-TESTS.md"
    agents = agents_path.read_text(encoding="utf-8")
    acceptance = acceptance_path.read_text(encoding="utf-8")
    for skill in skills:
        if skill.parent.name not in agents:
            errors.append(f"AGENTS.md missing skill: {skill.parent.name}")
    for owner in sorted(owner_ids(root / "tests" / "routing-cases.yaml")):
        if f"`{owner}`" not in agents:
            errors.append(f"AGENTS.md missing routing owner ID: {owner}")
        if f"`{owner}`" not in acceptance:
            errors.append(f"ACCEPTANCE-TESTS.md missing routing owner ID: {owner}")

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

    validate_contract_fixtures(root, errors)
    if errors:
        print("Pack validation failed:")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print(f"Pack validation passed: {len(skills)} skills, routing cases, contract fixtures, aligned manifests, and portable catalog links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
