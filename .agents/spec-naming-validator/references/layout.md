# Repository Layout

Use these files as the source of truth for naming validation.

- `D:/application/spec-validator/_docs/_GroundRules/00_standard-language-ddd.yaml`
- `D:/application/spec-validator/_docs/_GroundRules/01_domain-terms.yaml`
- `D:/application/spec-validator/_docs/_GroundRules/41_typescript-module-rules.yaml`
- `D:/application/spec-validator/_docs/_GroundRules/40_security-rules-typescript.yaml`
- `D:/application/spec-validator/src/spec_validator/naming_validator.py`
- `D:/application/spec-validator/src/spec_validator/security_validator.py`

Use this wrapper to invoke the validator from the skill:

- `D:/application/spec-validator/.agents/spec-naming-validator/scripts/validate_names.py`
- `D:/application/spec-validator/.agents/spec-naming-validator/scripts/validate_security.py`

The wrapper adds the repository `src/` directory to `sys.path` and delegates to the local validator module.
