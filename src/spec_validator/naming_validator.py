from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parents[2]
GROUND_RULES_DIR = ROOT_DIR / "_docs" / "_GroundRules"
STANDARD_LANGUAGE_FILE = GROUND_RULES_DIR / "00_standard-language-ddd.yaml"
DOMAIN_TERMS_FILE = GROUND_RULES_DIR / "01_domain-terms.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def _tokenize_name(name: str) -> list[str]:
    if not name:
        return []

    if "-" in name or "_" in name or "." in name:
        parts = re.split(r"[-_.]+", name)
        return [part for part in parts if part]

    return re.findall(r"[A-Z]+(?=[A-Z][a-z]|[0-9]|$)|[A-Z]?[a-z]+|[0-9]+", name)


def _normalize_identifier(name: str) -> str:
    tokens = _tokenize_name(name)
    normalized: list[str] = []
    for token in tokens:
        if not token:
            continue
        normalized.append(token if token.isupper() else token[0].upper() + token[1:])
    return "".join(normalized)


def _normalize_file_stem(path: Path) -> str:
    return _normalize_identifier(path.stem)


def _extract_typescript_identifiers(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches: list[tuple[str, str]] = []
    patterns = [
        ("class", re.compile(r"\bexport\s+class\s+([A-Za-z_][A-Za-z0-9_]*)")),
        ("interface", re.compile(r"\bexport\s+interface\s+([A-Za-z_][A-Za-z0-9_]*)")),
        ("type", re.compile(r"\bexport\s+type\s+([A-Za-z_][A-Za-z0-9_]*)")),
        ("enum", re.compile(r"\bexport\s+enum\s+([A-Za-z_][A-Za-z0-9_]*)")),
        ("function", re.compile(r"\bexport\s+function\s+([A-Za-z_][A-Za-z0-9_]*)")),
    ]
    for kind, pattern in patterns:
        for match in pattern.finditer(text):
            matches.append((kind, match.group(1)))
    return matches


@dataclass(frozen=True)
class TermEntry:
    term: str
    aliases: set[str]
    forbidden_aliases: set[str]
    allowed_role_suffixes: set[str]


class NamingValidator:
    def __init__(self, standard_language_path: Path, domain_terms_path: Path) -> None:
        self.standard_language = _load_yaml(standard_language_path)
        self.domain_terms = _load_yaml(domain_terms_path)
        self.framework_terms = self._collect_terms(self.standard_language, "framework")
        self.ddd_terms = self._collect_terms(self.standard_language, "ddd")
        self.test_terms = self._collect_terms(self.standard_language, "test")
        self.role_term_aliases = self._collect_role_term_aliases(self.standard_language)
        self.forbidden_terms = self._collect_forbidden_terms(self.standard_language)
        self.domain_entries = self._collect_domain_entries(self.domain_terms)
        self.allowed_role_suffixes = (
            self.framework_terms | self.ddd_terms | self.test_terms
        )

    def _collect_terms(self, data: dict[str, Any], key: str) -> set[str]:
        items = data.get("terms", {}).get(key, [])
        values: set[str] = set()
        for item in items:
            term = item.get("term")
            if term:
                values.add(term)
            for alias in item.get("aliases", []):
                values.add(alias)
        return values

    def _collect_forbidden_terms(self, data: dict[str, Any]) -> set[str]:
        items = data.get("terms", {}).get("generic_forbidden", [])
        values: set[str] = set()
        for item in items:
            term = item.get("term")
            if term:
                values.add(term)
            for alias in item.get("aliases", []):
                values.add(alias)
        return values

    def _collect_role_term_aliases(self, data: dict[str, Any]) -> dict[str, str]:
        values: dict[str, str] = {}
        for key in ("framework", "ddd", "test"):
            for item in data.get("terms", {}).get(key, []):
                term = item.get("term")
                if not term:
                    continue
                values[term] = term
                for alias in item.get("aliases", []):
                    values[alias] = term
        return values

    def _collect_domain_entries(self, data: dict[str, Any]) -> dict[str, TermEntry]:
        entries: dict[str, TermEntry] = {}
        for item in data.get("terms", []):
            entry = TermEntry(
                term=item["term"],
                aliases=set(item.get("aliases", [])),
                forbidden_aliases=set(item.get("forbidden_aliases", [])),
                allowed_role_suffixes=set(item.get("allowed_role_suffixes", [])),
            )
            entries[entry.term] = entry
        return entries

    def validate_name(self, name: str) -> dict[str, Any]:
        tokens = _tokenize_name(name)
        result: dict[str, Any] = {
            "name": name,
            "tokens": tokens,
            "valid": True,
            "errors": [],
            "matched_domain_terms": [],
            "matched_role_suffixes": [],
        }

        if not tokens:
            result["valid"] = False
            result["errors"].append(
                {
                    "code": "EMPTY_NAME",
                    "message": "Name must not be empty.",
                }
            )
            return result

        forbidden_matches = [token for token in tokens if token in self.forbidden_terms]
        if forbidden_matches:
            result["valid"] = False
            result["errors"].append(
                {
                    "code": "FORBIDDEN_GENERIC_TERM",
                    "message": "Forbidden generic term detected.",
                    "terms": forbidden_matches,
                }
            )

        matched_roles, remaining = self._extract_role_suffixes(tokens)
        matched_roles = [self.role_term_aliases.get(role, role) for role in matched_roles]

        result["matched_role_suffixes"] = matched_roles

        if not remaining:
            result["valid"] = False
            result["errors"].append(
                {
                    "code": "MISSING_DOMAIN_TERM",
                    "message": "A name must include at least one registered domain term.",
                }
            )
            return result

        domain_candidate = "".join(remaining)
        entry = self.domain_entries.get(domain_candidate)
        if entry:
            result["matched_domain_terms"] = [entry.term]
            if matched_roles:
                invalid_roles = [
                    role
                    for role in matched_roles
                    if role not in entry.allowed_role_suffixes
                ]
                if invalid_roles:
                    result["valid"] = False
                    result["errors"].append(
                        {
                            "code": "DISALLOWED_ROLE_SUFFIX",
                            "message": "Role suffix is not allowed for this domain term.",
                            "domain_term": entry.term,
                            "role_suffixes": invalid_roles,
                            "allowed_role_suffixes": sorted(entry.allowed_role_suffixes),
                        }
                    )
            return result

        alias_entry = self._find_alias_entry(domain_candidate)
        if alias_entry:
            result["valid"] = False
            result["errors"].append(
                {
                    "code": "NON_CANONICAL_ALIAS",
                    "message": "Alias detected where canonical domain term is required.",
                    "alias": domain_candidate,
                    "canonical": alias_entry.term,
                }
            )
            return result

        forbidden_alias_entry = self._find_forbidden_alias_entry(domain_candidate)
        if forbidden_alias_entry:
            result["valid"] = False
            result["errors"].append(
                {
                    "code": "FORBIDDEN_DOMAIN_ALIAS",
                    "message": "Forbidden alias detected for domain term.",
                    "alias": domain_candidate,
                    "canonical": forbidden_alias_entry.term,
                }
            )
            return result

        result["valid"] = False
        result["errors"].append(
            {
                "code": "UNKNOWN_DOMAIN_TERM",
                "message": "Domain term is not registered in the dictionary.",
                "candidate": domain_candidate,
            }
        )
        return result

    def validate_identifier(self, name: str) -> dict[str, Any]:
        normalized = _normalize_identifier(name)
        result = self.validate_name(normalized)
        result["original_name"] = name
        result["normalized_name"] = normalized
        return result

    def validate_typescript_path(self, path: Path) -> list[dict[str, Any]]:
        if path.is_file():
            ts_files = [path]
        else:
            ts_files = sorted(
                candidate
                for candidate in path.rglob("*.ts")
                if "node_modules" not in candidate.parts
            )

        results: list[dict[str, Any]] = []
        for ts_file in ts_files:
            file_result = self.validate_identifier(_normalize_file_stem(ts_file))
            file_result["source_type"] = "file"
            file_result["source_path"] = str(ts_file)
            file_result["source_name"] = ts_file.name
            results.append(file_result)

            for declaration_kind, declaration_name in _extract_typescript_identifiers(ts_file):
                declaration_result = self.validate_identifier(declaration_name)
                declaration_result["source_type"] = declaration_kind
                declaration_result["source_path"] = str(ts_file)
                declaration_result["source_name"] = declaration_name
                results.append(declaration_result)

        return results

    def _extract_role_suffixes(self, tokens: list[str]) -> tuple[list[str], list[str]]:
        matched_roles: list[str] = []
        remaining = tokens[:]
        while remaining:
            matched = False
            for size in (2, 1):
                if len(remaining) < size:
                    continue
                candidate = "".join(remaining[-size:])
                if candidate in self.allowed_role_suffixes or candidate in self.forbidden_terms:
                    matched_roles.insert(0, candidate)
                    remaining = remaining[:-size]
                    matched = True
                    break
            if not matched:
                break
        return matched_roles, remaining

    def _find_alias_entry(self, candidate: str) -> TermEntry | None:
        for entry in self.domain_entries.values():
            if candidate in entry.aliases:
                return entry
        return None

    def _find_forbidden_alias_entry(self, candidate: str) -> TermEntry | None:
        for entry in self.domain_entries.values():
            if candidate in entry.forbidden_aliases:
                return entry
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate names against DDD naming rules.")
    parser.add_argument("names", nargs="*", help="Names to validate.")
    parser.add_argument(
        "--path",
        help="TypeScript file or directory to scan for file names and exported declarations.",
    )
    parser.add_argument(
        "--standard-language",
        default=str(STANDARD_LANGUAGE_FILE),
        help="Path to 00_standard-language-ddd.yaml",
    )
    parser.add_argument(
        "--domain-terms",
        default=str(DOMAIN_TERMS_FILE),
        help="Path to 01_domain-terms.yaml",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format.",
    )
    return parser


def _format_text(results: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for result in results:
        status = "OK" if result["valid"] else "NG"
        label = result.get("source_name", result["name"])
        lines.append(f"{status} {label}")
        if result.get("source_type") and result.get("source_path"):
            lines.append(f"  source: {result['source_type']} @ {result['source_path']}")
        if result.get("normalized_name") and result["normalized_name"] != label:
            lines.append(f"  normalized: {result['normalized_name']}")
        if result["matched_domain_terms"]:
            lines.append(f"  domain: {', '.join(result['matched_domain_terms'])}")
        if result["matched_role_suffixes"]:
            lines.append(f"  roles: {', '.join(result['matched_role_suffixes'])}")
        for error in result["errors"]:
            lines.append(f"  error[{error['code']}]: {error['message']}")
    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    validator = NamingValidator(
        standard_language_path=Path(args.standard_language),
        domain_terms_path=Path(args.domain_terms),
    )
    results: list[dict[str, Any]] = []
    if args.names:
        results.extend(validator.validate_identifier(name) for name in args.names)
    if args.path:
        results.extend(validator.validate_typescript_path(Path(args.path)))
    if not results:
        parser.error("Provide at least one name or --path.")

    if args.format == "text":
        print(_format_text(results))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))

    return 0 if all(result["valid"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
