---
name: spec-csharp-validator
description: Validate C#-oriented specification governance for this repository. Use when Codex needs to apply the repository's YAML-based rules to C# projects, including spec structure checks under `_docs/_Specs`, traceability validation between specifications, implementation, and tests, and naming validation for C# files or identifiers after C#-specific standard language rules are defined.
---

# Spec CSharp Validator

## Overview

Use this skill to run the repository's validators in C#-centered workflows.
Keep the execution engine shared with the existing validators in `src/spec_validator/`, but treat this skill as the C#-facing entry point.

## Workflow

1. Read `references/layout.md` to confirm the validator entry points and rule files.
2. Read `references/csharp-profile.md` when the task is about applying the governance model to C# code or .NET project structure.
3. Run the relevant wrapper under `scripts/`.
4. Report exact issue codes, affected paths, and whether the result is `PASS`, `OMITTED-ACCEPTED`, `INVALID`, or `MISSING`.

## Commands

Validate spec structure:

```powershell
python .agents/spec-csharp-validator/scripts/validate_spec_structure.py --spec-root _docs/_Specs --format text
```

Validate traceability:

```powershell
python .agents/spec-csharp-validator/scripts/validate_traceability.py --implementation-path examples/traceability-pass/src --test-path examples/traceability-pass/test --format text
```

Validate names:

```powershell
python .agents/spec-csharp-validator/scripts/validate_names.py OrderRepository OrderController --format text
```

Validate layered DIP rules:

```powershell
python .agents/spec-csharp-validator/scripts/validate_architecture.py --path examples/csharp-architecture-pass/src --format text
```

Validate static security rules:

```powershell
python .agents/spec-csharp-validator/scripts/validate_security.py --path examples/csharp-security-pass/src --format text
```

Write a Markdown report:

```powershell
python .agents/spec-csharp-validator/scripts/validate_spec_structure.py --spec-root samples --format text --report reports/spec-structure-samples-report.md --report-format markdown
```

## Notes

- Reuse the validator engines in `src/spec_validator/`. Do not duplicate validation logic in the skill.
- Keep this skill C#-facing. Keep the existing `spec-naming-validator` as the NestJS-facing skill and `spec-python-validator` as the Python-facing skill.
- Extend naming governance for C# by adding C#-specific standard language first, then update the validator only when YAML alone cannot express the rule.
- Use `_docs/_Specs` as the canonical spec root. Treat `samples/` as compatibility input and migration material.
