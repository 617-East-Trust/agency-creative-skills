# Agency Creative Skills

This repository contains Agent Skills following https://agentskills.io/specification.

## Layout

```
skills/
  agency-creative-studio/SKILL.md
  premium-report-craft/SKILL.md
  technical-website-soundness/SKILL.md
```

Each skill directory name must match the `name` field in that skill's YAML frontmatter (kebab-case).

## Install targets

Skills install to `.agents/skills/` (cross-agent) and/or `.claude/skills/` / `.cursor/skills/` depending on the harness.
