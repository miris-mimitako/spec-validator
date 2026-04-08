---
name: spec-naming-validator
description: Validate NestJS and DDD naming rules for this repository by reading `_docs/_GroundRules/00_standard-language-ddd.yaml` and `_docs/_GroundRules/01_domain-terms.yaml`. Use when Codex needs to check candidate names, explain naming violations, or run the local Python naming validator from `.agents/spec-naming-validator/scripts/validate_names.py`.
---

# Spec Naming Validator

## Overview

Use the repository's naming dictionaries and local Python validator to judge whether a class, file, function, or module name follows the current NestJS + DDD rules.

## Workflow

1. Read `_docs/_GroundRules/00_standard-language-ddd.yaml` to understand framework terms, DDD terms, and forbidden generic terms.
2. Read `_docs/_GroundRules/01_domain-terms.yaml` to resolve canonical domain terms, aliases, forbidden aliases, and allowed role suffixes.
3. Run `scripts/validate_names.py` for one or more candidate names.
4. Report the exact violation codes and the domain term or role suffix that caused the result.

## Commands

Validate a few names quickly:

```powershell
python .agents/spec-naming-validator/scripts/validate_names.py OrderRepository PlaceOrderUseCase CustomerDTO --format text
```

Get machine-readable output:

```powershell
python .agents/spec-naming-validator/scripts/validate_names.py OrderManager UserRepository --format json
```

## Interpretation

- `FORBIDDEN_GENERIC_TERM`: contains a forbidden generic token such as `Manager`, `Helper`, or `Util`
- `UNKNOWN_DOMAIN_TERM`: uses a domain term that is not registered in the dictionary
- `FORBIDDEN_DOMAIN_ALIAS`: uses a forbidden alias for a registered domain term
- `NON_CANONICAL_ALIAS`: uses a registered alias instead of the canonical domain term
- `DISALLOWED_ROLE_SUFFIX`: uses a role suffix that is not allowed for that domain term
- `MISSING_DOMAIN_TERM`: contains only role terms and no registered domain subject

## Notes

- Do not reimplement the naming logic in this skill. Call `src/spec_validator/naming_validator.py`.
- Add new naming rules to `_docs/_GroundRules` first, then update Python only if the rule cannot be expressed in YAML alone.
- Do not approve unregistered business terms. Register them in `01_domain-terms.yaml` first.

## References

- For repository-specific file locations and execution details, read `references/layout.md`.
