# CSharp Profile

This skill is for C# projects that want to apply the same specification governance model as the NestJS- and Python-oriented skills.

Current scope:

- Reuse the existing validators in `src/spec_validator/`
- Reuse spec structure, traceability, and reporting flows
- Apply naming validation to C# identifiers and `.cs` files through `00_standard-language-csharp.yaml`
- Validate layer crossing with DIP rules, consumer-owned interfaces, and external DI registration

Current limitation:

- Domain terms are still shared with the other profiles by default
- If C#-specific role suffixes or framework terms are needed, add them to the C# ground rule file first

Recommended approach:

1. Keep spec structure and traceability validation language-agnostic
2. Keep C# standard language in `_docs/_GroundRules/00_standard-language-csharp.yaml`
3. Reuse the same validator engine where possible, but keep skills split by invocation context
