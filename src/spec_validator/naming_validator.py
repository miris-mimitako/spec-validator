from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parents[2]
GROUND_RULES_DIR = ROOT_DIR / "_docs" / "_GroundRules"
STANDARD_LANGUAGE_FILE = GROUND_RULES_DIR / "00_standard-language-ddd.yaml"
PYTHON_STANDARD_LANGUAGE_FILE = GROUND_RULES_DIR / "00_standard-language-python.yaml"
CSHARP_STANDARD_LANGUAGE_FILE = GROUND_RULES_DIR / "00_standard-language-csharp.yaml"
DOMAIN_TERMS_FILE = GROUND_RULES_DIR / "01_domain-terms.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
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
    text = path.read_text(encoding="utf-8-sig")
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


def _extract_python_identifiers(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8-sig")
    matches: list[tuple[str, str]] = []
    patterns = [
        ("class", re.compile(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\b", re.MULTILINE)),
        ("function", re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\b", re.MULTILINE)),
    ]
    for kind, pattern in patterns:
        for match in pattern.finditer(text):
            matches.append((kind, match.group(1)))
    return matches


def _extract_csharp_identifiers(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8-sig")
    matches: list[tuple[str, str]] = []
    patterns = [
        (
            "class",
            re.compile(
                r"\b(?:public|internal|private|protected)?\s*(?:sealed\s+|abstract\s+|partial\s+)*class\s+([A-Za-z_][A-Za-z0-9_]*)"
            ),
        ),
        (
            "interface",
            re.compile(
                r"\b(?:public|internal|private|protected)?\s*interface\s+([A-Za-z_][A-Za-z0-9_]*)"
            ),
        ),
        (
            "record",
            re.compile(
                r"\b(?:public|internal|private|protected)?\s*(?:sealed\s+|partial\s+)*record\s+([A-Za-z_][A-Za-z0-9_]*)"
            ),
        ),
    ]
    for kind, pattern in patterns:
        for match in pattern.finditer(text):
            matches.append((kind, match.group(1)))
    return matches


def _make_report_payload(
    results: list[dict[str, Any]],
    *,
    scanned_path: str | None,
    input_names: list[str],
) -> dict[str, Any]:
    file_results = [result for result in results if result.get("source_type") == "file"]
    declaration_results = [result for result in results if result.get("source_type") != "file"]

    if file_results:
        report_units = file_results
        report_scope = "file"
    else:
        report_units = results
        report_scope = "item"

    passed = [result for result in report_units if result["valid"]]
    failed = [result for result in report_units if not result["valid"]]

    error_counts: dict[str, int] = {}
    for result in failed:
        for error in result["errors"]:
            code = error["code"]
            error_counts[code] = error_counts.get(code, 0) + 1

    files: list[dict[str, Any]] = []
    if file_results:
        declarations_by_path: dict[str, list[dict[str, Any]]] = {}
        for declaration in declaration_results:
            declarations_by_path.setdefault(declaration["source_path"], []).append(declaration)

        for file_result in file_results:
            files.append(
                {
                    "path": file_result["source_path"],
                    "name": file_result["source_name"],
                    "valid": file_result["valid"],
                    "errors": file_result["errors"],
                    "matched_domain_terms": file_result["matched_domain_terms"],
                    "matched_role_suffixes": file_result["matched_role_suffixes"],
                    "normalized_name": file_result.get("normalized_name"),
                    "declarations": declarations_by_path.get(file_result["source_path"], []),
                }
            )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scanned_path": scanned_path,
        "input_names": input_names,
        "summary": {
            "scope": report_scope,
            "total": len(report_units),
            "passed": len(passed),
            "failed": len(failed),
            "status": "success" if not failed else "failure",
        },
        "error_counts": dict(sorted(error_counts.items())),
        "files": files,
        "passed": passed,
        "failed": failed,
        "declarations": declaration_results,
    }


def _format_markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Naming Validation Report",
        "",
        f"- Generated At: `{report['generated_at']}`",
        f"- Status: `{summary['status']}`",
        f"- Scope: `{summary['scope']}`",
        f"- Total: `{summary['total']}`",
        f"- Passed: `{summary['passed']}`",
        f"- Failed: `{summary['failed']}`",
    ]

    if report["scanned_path"]:
        lines.append(f"- Scanned Path: `{report['scanned_path']}`")
    if report["input_names"]:
        joined = ", ".join(f"`{name}`" for name in report["input_names"])
        lines.append(f"- Input Names: {joined}")

    lines.extend(["", "## Error Counts", ""])
    if report["error_counts"]:
        for code, count in report["error_counts"].items():
            lines.append(f"- `{code}`: {count}")
    else:
        lines.append("- None")

    if report["files"]:
        lines.extend(["", "## Files", ""])
        for file_entry in report["files"]:
            lines.extend(_format_markdown_file_result(file_entry))
    else:
        lines.extend(["", "## Passed", ""])
        if report["passed"]:
            for result in report["passed"]:
                lines.extend(_format_markdown_result(result))
        else:
            lines.append("- None")

        lines.extend(["", "## Failed", ""])
        if report["failed"]:
            for result in report["failed"]:
                lines.extend(_format_markdown_result(result))
        else:
            lines.append("- None")

    return "\n".join(lines) + "\n"


def _format_markdown_file_result(file_entry: dict[str, Any]) -> list[str]:
    lines = [f"### `{file_entry['name']}`", ""]
    lines.append(f"- Result: `{'OK' if file_entry['valid'] else 'NG'}`")
    lines.append(f"- Path: `{file_entry['path']}`")
    if file_entry.get("normalized_name") and file_entry["normalized_name"] != file_entry["name"]:
        lines.append(f"- Normalized Name: `{file_entry['normalized_name']}`")
    if file_entry["matched_domain_terms"]:
        lines.append(
            f"- Domain Terms: {', '.join(f'`{term}`' for term in file_entry['matched_domain_terms'])}"
        )
    if file_entry["matched_role_suffixes"]:
        lines.append(
            f"- Role Suffixes: {', '.join(f'`{role}`' for role in file_entry['matched_role_suffixes'])}"
        )
    if file_entry["errors"]:
        lines.append("- File Errors:")
        for error in file_entry["errors"]:
            lines.append(f"  - `{error['code']}`: {error['message']}")
    else:
        lines.append("- File Errors: None")

    if file_entry["declarations"]:
        lines.append("- Declarations:")
        for declaration in file_entry["declarations"]:
            declaration_status = "OK" if declaration["valid"] else "NG"
            lines.append(f"  - `{declaration['source_name']}`: `{declaration_status}`")
            if declaration["matched_domain_terms"]:
                domain_terms = ", ".join(
                    f"`{term}`" for term in declaration["matched_domain_terms"]
                )
                lines.append(f"    - Domain Terms: {domain_terms}")
            if declaration["matched_role_suffixes"]:
                role_terms = ", ".join(
                    f"`{role}`" for role in declaration["matched_role_suffixes"]
                )
                lines.append(f"    - Role Suffixes: {role_terms}")
            if declaration["errors"]:
                for error in declaration["errors"]:
                    lines.append(f"    - `{error['code']}`: {error['message']}")
    else:
        lines.append("- Declarations: None")

    lines.append("")
    return lines


def _format_markdown_result(result: dict[str, Any]) -> list[str]:
    label = result.get("source_name", result["name"])
    lines = [f"### `{label}`", ""]
    lines.append(f"- Result: `{'OK' if result['valid'] else 'NG'}`")

    if result.get("source_type") and result.get("source_path"):
        lines.append(f"- Source: `{result['source_type']}` in `{result['source_path']}`")
    if result.get("normalized_name") and result["normalized_name"] != label:
        lines.append(f"- Normalized Name: `{result['normalized_name']}`")
    if result["matched_domain_terms"]:
        lines.append(
            f"- Domain Terms: {', '.join(f'`{term}`' for term in result['matched_domain_terms'])}"
        )
    if result["matched_role_suffixes"]:
        lines.append(
            f"- Role Suffixes: {', '.join(f'`{role}`' for role in result['matched_role_suffixes'])}"
        )

    if result["errors"]:
        lines.append("- Errors:")
        for error in result["errors"]:
            lines.append(f"  - `{error['code']}`: {error['message']}")

    lines.append("")
    return lines


def _write_report(report_path: Path, report_format: str, report: dict[str, Any]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if report_format == "json":
        content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    else:
        content = _format_markdown_report(report)
    report_path.write_text(content, encoding="utf-8-sig")


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

    def validate_path(self, path: Path) -> list[dict[str, Any]]:
        if path.is_file():
            source_files = [path]
        else:
            source_files = sorted(
                candidate
                for candidate in path.rglob("*")
                if candidate.is_file()
                and "node_modules" not in candidate.parts
                and candidate.suffix in {".ts", ".py", ".cs"}
            )

        results: list[dict[str, Any]] = []
        for source_file in source_files:
            file_result = self.validate_identifier(_normalize_file_stem(source_file))
            file_result["source_type"] = "file"
            file_result["source_path"] = str(source_file)
            file_result["source_name"] = source_file.name
            results.append(file_result)

            for declaration_kind, declaration_name in self._extract_identifiers(source_file):
                declaration_result = self.validate_identifier(declaration_name)
                declaration_result["source_type"] = declaration_kind
                declaration_result["source_path"] = str(source_file)
                declaration_result["source_name"] = declaration_name
                results.append(declaration_result)

        return results

    def _extract_identifiers(self, path: Path) -> list[tuple[str, str]]:
        if path.suffix == ".ts":
            return _extract_typescript_identifiers(path)
        if path.suffix == ".py":
            return _extract_python_identifiers(path)
        if path.suffix == ".cs":
            return _extract_csharp_identifiers(path)
        return []

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
        help="Source file or directory to scan for file names and declarations.",
    )
    parser.add_argument(
        "--profile",
        choices=("nestjs", "python", "csharp"),
        help="Use a built-in standard language profile.",
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
    parser.add_argument(
        "--report",
        help="Write a validation report to this file path.",
    )
    parser.add_argument(
        "--report-format",
        choices=("markdown", "json"),
        default="markdown",
        help="Report file format.",
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

    standard_language_path = Path(args.standard_language)
    if args.profile == "python":
        standard_language_path = PYTHON_STANDARD_LANGUAGE_FILE
    elif args.profile == "csharp":
        standard_language_path = CSHARP_STANDARD_LANGUAGE_FILE
    elif args.profile == "nestjs":
        standard_language_path = STANDARD_LANGUAGE_FILE

    validator = NamingValidator(
        standard_language_path=standard_language_path,
        domain_terms_path=Path(args.domain_terms),
    )
    results: list[dict[str, Any]] = []
    if args.names:
        results.extend(validator.validate_identifier(name) for name in args.names)
    if args.path:
        results.extend(validator.validate_path(Path(args.path)))
    if not results:
        parser.error("Provide at least one name or --path.")

    report = _make_report_payload(
        results,
        scanned_path=args.path,
        input_names=args.names,
    )

    if args.report:
        _write_report(Path(args.report), args.report_format, report)

    if args.format == "text":
        print(_format_text(results))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))

    return 0 if all(result["valid"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
