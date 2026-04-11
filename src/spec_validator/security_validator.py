from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parents[2]
GROUND_RULES_DIR = ROOT_DIR / "_docs" / "_GroundRules"
SECURITY_RULES_FILE = GROUND_RULES_DIR / "40_security-rules.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def _severity_for(code: str) -> str:
    return {
        "SENSITIVE_DATA_LOGGING": "ERROR",
        "SQL_INJECTION_RISK": "ERROR",
        "FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT": "ERROR",
        "FORBIDDEN_DANGEROUS_API": "WARNING",
    }.get(code, "INFO")


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    source_path: str
    line_number: int
    source_line: str


class SecurityValidator:
    def __init__(self, rules_path: Path) -> None:
        self.rules_doc = _load_yaml(rules_path)
        policy = self.rules_doc["policy"]
        detection = self.rules_doc["detection"]
        self.scan_extensions = set(policy["scan_extensions"])
        self.comment_prefixes = tuple(policy.get("comment_prefixes", []))

        sensitive_logging = detection["sensitive_logging"]
        self.logger_tokens = tuple(sensitive_logging["logger_tokens"])
        self.sensitive_terms = tuple(term.lower() for term in sensitive_logging["sensitive_terms"])

        sql_detection = detection["sql_injection_risk"]
        self.sql_execution_tokens = tuple(sql_detection["execution_tokens"])
        self.sql_keywords = tuple(keyword.lower() for keyword in sql_detection["sql_keywords"])
        self.sql_risky_patterns = [re.compile(pattern) for pattern in sql_detection["risky_construction_patterns"]]

        direct_assignment = detection["direct_literal_assignment"]
        self.allowed_assignment_patterns = [
            re.compile(pattern) for pattern in direct_assignment.get("allowed_assignment_patterns", [])
        ]
        literal_union = "|".join(direct_assignment["literal_patterns"])
        self.direct_assignment_patterns = [
            re.compile(pattern.replace("VALUE", f"(?:{literal_union})"))
            for pattern in direct_assignment["declaration_patterns"]
        ]

        self.dangerous_api_patterns = [
            re.compile(pattern) for pattern in detection["dangerous_api"]["patterns"]
        ]

    def validate(self, paths: list[Path]) -> dict[str, Any]:
        files = self._collect_files(paths)
        issues: list[Issue] = []
        for path in files:
            issues.extend(self._scan_file(path))

        issues = self._deduplicate_issues(issues)
        issue_counts = Counter(issue.code for issue in issues)
        issue_counts_by_severity = Counter(_severity_for(issue.code) for issue in issues)
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "paths": [str(path) for path in paths],
            "summary": {
                "status": "success" if not issues else "failure",
                "total_files": len(files),
                "total_issues": len(issues),
            },
            "issue_counts": dict(sorted(issue_counts.items())),
            "issue_counts_by_severity": {
                severity: issue_counts_by_severity.get(severity, 0)
                for severity in ("ERROR", "WARNING", "INFO")
            },
            "issues": [
                {
                    "code": issue.code,
                    "severity": _severity_for(issue.code),
                    "message": issue.message,
                    "source_path": issue.source_path,
                    "line_number": issue.line_number,
                    "source_line": issue.source_line,
                }
                for issue in issues
            ],
        }

    def _collect_files(self, paths: list[Path]) -> list[Path]:
        collected: list[Path] = []
        for path in paths:
            if path.is_file() and path.suffix in self.scan_extensions:
                collected.append(path)
                continue
            for extension in self.scan_extensions:
                collected.extend(sorted(candidate for candidate in path.rglob(f"*{extension}") if candidate.is_file()))
        return collected

    def _scan_file(self, path: Path) -> list[Issue]:
        text = path.read_text(encoding="utf-8-sig")
        issues: list[Issue] = []
        lines = text.splitlines()
        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or any(stripped.startswith(prefix) for prefix in self.comment_prefixes):
                continue

            sensitive_issue = self._detect_sensitive_logging(path, index, line)
            if sensitive_issue:
                issues.append(sensitive_issue)

            issues.extend(self._detect_sql_injection(path, index, line))

            direct_assignment_issue = self._detect_direct_literal_assignment(path, index, line)
            if direct_assignment_issue:
                issues.append(direct_assignment_issue)

            dangerous_api_issue = self._detect_dangerous_api(path, index, line)
            if dangerous_api_issue:
                issues.append(dangerous_api_issue)
        return issues

    def _detect_sensitive_logging(self, path: Path, line_number: int, line: str) -> Issue | None:
        lowered = line.lower()
        if not any(token.lower() in lowered for token in self.logger_tokens):
            return None
        if not any(term in lowered for term in self.sensitive_terms):
            return None
        return Issue(
            code="SENSITIVE_DATA_LOGGING",
            message="Sensitive data must not be logged.",
            source_path=str(path),
            line_number=line_number,
            source_line=line.strip(),
        )

    def _detect_sql_injection(self, path: Path, line_number: int, line: str) -> list[Issue]:
        lowered = line.lower()
        has_sql_keyword = any(keyword in lowered for keyword in self.sql_keywords)
        has_execution_token = any(token.lower() in lowered for token in self.sql_execution_tokens)
        has_risky_pattern = any(pattern.search(line) for pattern in self.sql_risky_patterns)

        if not ((has_sql_keyword and has_risky_pattern) or (has_execution_token and has_risky_pattern)):
            return []

        return [
            Issue(
                code="SQL_INJECTION_RISK",
                message="Potential SQL injection risk: avoid SQL string concatenation or interpolation.",
                source_path=str(path),
                line_number=line_number,
                source_line=line.strip(),
            )
        ]

    def _detect_direct_literal_assignment(self, path: Path, line_number: int, line: str) -> Issue | None:
        stripped = line.strip()
        if any(pattern.search(stripped) for pattern in self.allowed_assignment_patterns):
            return None
        for pattern in self.direct_assignment_patterns:
            if pattern.search(stripped):
                return Issue(
                    code="FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT",
                    message="Literal values must be assigned through a const declaration, not directly.",
                    source_path=str(path),
                    line_number=line_number,
                    source_line=stripped,
                )
        return None

    def _detect_dangerous_api(self, path: Path, line_number: int, line: str) -> Issue | None:
        for pattern in self.dangerous_api_patterns:
            if pattern.search(line):
                return Issue(
                    code="FORBIDDEN_DANGEROUS_API",
                    message="Forbidden dangerous API detected.",
                    source_path=str(path),
                    line_number=line_number,
                    source_line=line.strip(),
                )
        return None

    def _deduplicate_issues(self, issues: list[Issue]) -> list[Issue]:
        unique: list[Issue] = []
        seen: set[tuple[str, str, int, str]] = set()
        for issue in issues:
            key = (issue.code, issue.source_path, issue.line_number, issue.source_line)
            if key in seen:
                continue
            seen.add(key)
            unique.append(issue)
        return unique


def _format_text(report: dict[str, Any]) -> str:
    lines = [
        f"status: {report['summary']['status']}",
        f"total_files: {report['summary']['total_files']}",
        f"total_issues: {report['summary']['total_issues']}",
    ]
    for severity, count in report["issue_counts_by_severity"].items():
        lines.append(f"issues[{severity.lower()}]: {count}")
    for issue in report["issues"]:
        lines.append(
            f"issue[{issue['severity']}/{issue['code']}]: "
            f"{issue['source_path']}:{issue['line_number']} {issue['message']}"
        )
    return "\n".join(lines)


def _format_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Security Validation Report",
        "",
        f"- Generated At: `{report['generated_at']}`",
        f"- Status: `{report['summary']['status']}`",
        f"- Total Files: `{report['summary']['total_files']}`",
        f"- Total Issues: `{report['summary']['total_issues']}`",
    ]
    if report["paths"]:
        joined = ", ".join(f"`{item}`" for item in report["paths"])
        lines.append(f"- Paths: {joined}")

    lines.extend(["", "## Issue Counts", "", "| Severity | Count |", "| --- | --- |"])
    for severity, count in report["issue_counts_by_severity"].items():
        lines.append(f"| `{severity}` | `{count}` |")

    lines.append("")
    if report["issue_counts"]:
        for code, count in report["issue_counts"].items():
            lines.append(f"- `{_severity_for(code)}` `{code}`: {count}")
    else:
        lines.append("- None")

    lines.extend(["", "## Issues", ""])
    if report["issues"]:
        for issue in report["issues"]:
            lines.append(
                f"- `{issue['severity']}` `{issue['code']}`: {issue['message']}"
            )
            lines.append(f"  - source: `{issue['source_path']}:{issue['line_number']}`")
            lines.append(f"  - line: `{issue['source_line']}`")
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def _write_report(path: Path, report_format: str, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if report_format == "json" else _format_markdown(report)
    path.write_text(content, encoding="utf-8-sig")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate static security rules.")
    parser.add_argument("--path", action="append", default=[], help="File or directory to scan. Repeatable.")
    parser.add_argument("--rules", default=str(SECURITY_RULES_FILE), help="Path to 40_security-rules.yaml")
    parser.add_argument("--format", choices=("json", "text"), default="json", help="Console output format.")
    parser.add_argument("--report", help="Write a validation report to this file path.")
    parser.add_argument("--report-format", choices=("markdown", "json"), default="markdown", help="Report file format.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.path:
        parser.error("Provide at least one --path.")

    validator = SecurityValidator(Path(args.rules))
    report = validator.validate([Path(item) for item in args.path])

    if args.report:
        _write_report(Path(args.report), args.report_format, report)

    if args.format == "text":
        print(_format_text(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    return 0 if report["summary"]["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
