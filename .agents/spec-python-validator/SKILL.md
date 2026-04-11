---
name: spec-python-validator
description: Validate Python-oriented specification governance for this repository. Use when Codex needs to apply the repository's YAML-based rules to Python projects, including spec structure checks under `_docs/_Specs`, traceability validation between specifications, implementation, and tests, and naming validation for Python files or identifiers after Python-specific term rules are defined.
---

# Spec Python Validator

## Overview

Use this skill to run the repository's validators in Python-centered workflows.
Keep the execution engine shared with the existing validators in `src/spec_validator/`, but treat this skill as the Python-facing entry point.

## Workflow

1. Read `references/layout.md` to confirm the validator entry points and rule files.
2. Read `references/python-profile.md` when the task is about applying the governance model to Python code or Python project structure.
3. Run the relevant wrapper under `scripts/`.
4. Report exact issue codes, affected paths, and whether the result is `PASS`, `OMITTED-ACCEPTED`, `INVALID`, or `MISSING`.

## Commands

Validate spec structure:

```powershell
python .agents/spec-python-validator/scripts/validate_spec_structure.py --spec-root _docs/_Specs --format text
```

Validate traceability:

```powershell
python .agents/spec-python-validator/scripts/validate_traceability.py --implementation-path examples/traceability-pass/src --test-path examples/traceability-pass/test --format text
```

Validate names:

```powershell
python .agents/spec-python-validator/scripts/validate_names.py OrderRepository PlaceOrderUseCase --format text
```

Validate static security rules:

```powershell
python .agents/spec-python-validator/scripts/validate_security.py --path examples/python-security-pass/src --format text
```

Write a Markdown report:

```powershell
python .agents/spec-python-validator/scripts/validate_spec_structure.py --spec-root samples --format text --report reports/spec-structure-samples-report.md --report-format markdown
```

## Notes

- Reuse the validator engines in `src/spec_validator/`. Do not duplicate validation logic in the skill.
- Keep this skill Python-facing. Keep the existing `spec-naming-validator` as the NestJS-facing skill.
- Extend naming governance for Python by adding Python-specific term dictionaries first, then update the validator only when YAML alone cannot express the rule.
- Use `_docs/_Specs` as the canonical spec root. Treat `samples/` as compatibility input and migration material.
