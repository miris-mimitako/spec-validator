# Python Profile

This skill is for Python projects that want to apply the same specification governance model as the NestJS-oriented skill.

Current scope:

- Reuse the existing Python validators in `src/spec_validator/`
- Reuse spec structure, traceability, and reporting flows
- Apply naming validation to Python identifiers and file names through `00_standard-language-python.yaml`
- Apply static security validation to Python files through `40_security-rules-python.yaml`

Current limitation:

- Domain terms are still shared with the NestJS-oriented profile by default
- If Python-only role suffixes or framework terms are needed, add them to the Python ground rule file first

Recommended approach:

1. Keep spec structure and traceability validation language-agnostic
2. Keep Python standard language in `_docs/_GroundRules/00_standard-language-python.yaml`
3. Reuse the same validator engine where possible, but keep skills split by invocation context
