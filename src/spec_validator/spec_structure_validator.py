from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parents[2]
GROUND_RULES_DIR = ROOT_DIR / "_docs" / "_GroundRules"
SPEC_STRUCTURE_FILE = GROUND_RULES_DIR / "20_spec-structure.yaml"
DEFAULT_SPECS_ROOT = ROOT_DIR / "_docs" / "_Specs"


ISSUE_SEVERITY: dict[str, str] = {
    "INVALID_SPEC_PATH": "ERROR",
    "UNKNOWN_DOCUMENT_KIND": "ERROR",
    "INVALID_YAML_ROOT": "ERROR",
    "MISSING_RULE_ID": "ERROR",
    "MISSING_RULE_DESCRIPTION": "ERROR",
    "MIXED_RULE_ENTRY_TYPE": "ERROR",
    "DUPLICATE_LOCAL_ID_IN_FILE": "ERROR",
    "DUPLICATE_CANONICAL_ID": "ERROR",
    "MISSING_REF_TARGET": "ERROR",
    "INVALID_IMPLEMENTED_IN_ENTRY": "ERROR",
    "UNKNOWN_IMPLEMENTATION_STATUS": "ERROR",
    "NO_RULES_FOUND": "WARNING",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def _issue_severity(code: str) -> str:
    return ISSUE_SEVERITY.get(code, "INFO")


def _translate_status(status: str, language: str) -> str:
    if language == "ja":
        return {
            "success": "成功",
            "failure": "失敗",
            "PASS": "PASS",
            "INVALID": "INVALID",
        }.get(status, status)
    return status


def _issue_message(issue: dict[str, Any], language: str) -> str:
    if language != "ja":
        return issue["message"]
    return {
        "INVALID_SPEC_PATH": "仕様ファイルの配置が規約に一致していません。",
        "UNKNOWN_DOCUMENT_KIND": "仕様ファイルの種別が規約に存在しません。",
        "INVALID_YAML_ROOT": "YAML のルートが mapping ではありません。",
        "MISSING_RULE_ID": "ルール項目に id がありません。",
        "MISSING_RULE_DESCRIPTION": "ルール項目に description がありません。",
        "MIXED_RULE_ENTRY_TYPE": "ルール配列に文字列などの不正な要素が含まれています。",
        "DUPLICATE_LOCAL_ID_IN_FILE": "同一ファイル内で local id が重複しています。",
        "DUPLICATE_CANONICAL_ID": "canonical id が重複しています。",
        "MISSING_REF_TARGET": "$ref の参照先ファイルが存在しません。",
        "INVALID_IMPLEMENTED_IN_ENTRY": "implemented_in の要素に path または status が不足しています。",
        "UNKNOWN_IMPLEMENTATION_STATUS": "implemented_in.status が許可された値ではありません。",
        "NO_RULES_FOUND": "仕様ファイル内に対象ルールが見つかりませんでした。",
    }.get(issue["code"], issue["message"])


class SpecStructureValidator:
    def __init__(self, rule_path: Path) -> None:
        self.rule_doc = _load_yaml(rule_path)
        self.allowed_kinds = set(self.rule_doc["root"]["allowed_domain_directories"])
        self.optional_kinds = set(self.rule_doc["root"].get("optional_domain_directories", []))
        self.known_kinds = self.allowed_kinds | self.optional_kinds
        self.file_extensions = set(self.rule_doc["document_structure"]["file_extensions"])
        self.domain_dir_pattern = re.compile(
            self.rule_doc["document_structure"]["domain_directory_pattern"]
        )
        self.local_id_patterns = [
            re.compile(pattern) for pattern in self.rule_doc["naming"]["local_id_patterns"]
        ]
        self.canonical_format = self.rule_doc["naming"]["canonical_id_format"]
        self.section_aliases = self.rule_doc["normalization"].get("section_aliases", {})
        self.allow_mixed_rule_entries = self.rule_doc["validation_rules"][
            "allow_mixed_string_and_object_entries"
        ]
        self.require_ref_target_exists = self.rule_doc["validation_rules"][
            "require_ref_target_exists"
        ]
        self.allowed_status_values = set(
            self.rule_doc["traceability_mapping"]["allowed_status_values"]
        )

    def validate(self, spec_roots: list[Path]) -> dict[str, Any]:
        documents: list[dict[str, Any]] = []
        issues: list[dict[str, Any]] = []
        canonical_counter: Counter[str] = Counter()

        spec_files = self._collect_spec_files(spec_roots)
        for path, root in spec_files:
            document, document_issues = self._validate_document(path, root)
            documents.append(document)
            issues.extend(document_issues)
            for rule in document["rules"]:
                canonical_counter[rule["canonical_id"]] += 1

        for document in documents:
            for rule in document["rules"]:
                if canonical_counter[rule["canonical_id"]] > 1:
                    issues.append(
                        {
                            "code": "DUPLICATE_CANONICAL_ID",
                            "message": "Canonical id is duplicated.",
                            "canonical_id": rule["canonical_id"],
                            "source_path": document["source_path"],
                        }
                    )

        rule_count = sum(len(document["rules"]) for document in documents)
        ref_count = sum(len(document["refs"]) for document in documents)
        implemented_in_count = sum(
            len(rule["implemented_in"])
            for document in documents
            for rule in document["rules"]
        )
        issue_counts = Counter(issue["code"] for issue in issues)
        issue_counts_by_severity = Counter(_issue_severity(issue["code"]) for issue in issues)

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "spec_roots": [str(path) for path in spec_roots],
            "summary": {
                "status": "success" if not issues else "failure",
                "total_documents": len(documents),
                "total_rules": rule_count,
                "total_refs": ref_count,
                "total_implemented_in": implemented_in_count,
                "total_issues": len(issues),
            },
            "issue_counts": dict(sorted(issue_counts.items())),
            "issue_counts_by_severity": {
                severity: issue_counts_by_severity.get(severity, 0)
                for severity in ("ERROR", "WARNING", "INFO")
            },
            "documents": documents,
            "issues": issues,
        }

    def _collect_spec_files(self, spec_roots: list[Path]) -> list[tuple[Path, Path]]:
        files: list[tuple[Path, Path]] = []
        for root in spec_roots:
            if not root.exists():
                continue
            for path in sorted(root.rglob("*")):
                if not path.is_file():
                    continue
                if path.name.lower() == "readme.md":
                    continue
                if path.suffix.lower() not in self.file_extensions:
                    continue
                files.append((path, root))
        return files

    def _validate_document(self, path: Path, root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        issues: list[dict[str, Any]] = []
        relative_parts = path.relative_to(root).parts
        domain = ""
        kind = ""
        document_name = path.stem

        if len(relative_parts) < 3:
            issues.append(
                {
                    "code": "INVALID_SPEC_PATH",
                    "message": "Spec file path does not match the required layout.",
                    "source_path": str(path),
                }
            )
        else:
            domain = relative_parts[0]
            kind = relative_parts[1]
            if not self.domain_dir_pattern.fullmatch(domain):
                issues.append(
                    {
                        "code": "INVALID_SPEC_PATH",
                        "message": "Spec file path does not match the required layout.",
                        "source_path": str(path),
                    }
                )
            if kind not in self.known_kinds:
                issues.append(
                    {
                        "code": "UNKNOWN_DOCUMENT_KIND",
                        "message": "Document kind is not defined by the spec structure rules.",
                        "source_path": str(path),
                        "kind": kind,
                    }
                )

        try:
            data = _load_yaml(path)
        except ValueError:
            issues.append(
                {
                    "code": "INVALID_YAML_ROOT",
                    "message": "YAML root must be a mapping.",
                    "source_path": str(path),
                }
            )
            data = {}

        rules = self._extract_rules(
            data=data,
            domain=domain,
            kind=kind,
            document_name=document_name,
            source_path=str(path),
            issues=issues,
        )
        refs = self._resolve_refs(data, path, issues)

        if not rules:
            issues.append(
                {
                    "code": "NO_RULES_FOUND",
                    "message": "No rule entries were found in the spec document.",
                    "source_path": str(path),
                }
            )

        return (
            {
                "source_path": str(path),
                "root_path": str(root),
                "domain": domain,
                "kind": kind,
                "document_name": document_name,
                "rules": rules,
                "refs": refs,
            },
            issues,
        )

    def _extract_rules(
        self,
        *,
        data: dict[str, Any],
        domain: str,
        kind: str,
        document_name: str,
        source_path: str,
        issues: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        section_names = set()
        for name in self.rule_doc["document_kinds"].get(kind, {}).get("local_id_sections", []):
            section_names.add(name)
            alias = self.section_aliases.get(name)
            if alias:
                section_names.add(alias)

        found_entries: list[dict[str, Any]] = []
        self._walk_sections(
            node=data,
            current_path=[],
            section_names=section_names,
            found_entries=found_entries,
            source_path=source_path,
            issues=issues,
        )

        seen_local_ids: Counter[str] = Counter()
        normalized_rules: list[dict[str, Any]] = []
        for entry in found_entries:
            local_id = entry.get("id")
            if not isinstance(local_id, str):
                issues.append(
                    {
                        "code": "MISSING_RULE_ID",
                        "message": "Rule entry is missing id.",
                        "source_path": source_path,
                        "section_path": ".".join(entry["_section_path"]),
                    }
                )
                continue
            if not any(pattern.fullmatch(local_id) for pattern in self.local_id_patterns):
                continue
            description = entry.get("description")
            if not isinstance(description, str) or not description.strip():
                issues.append(
                    {
                        "code": "MISSING_RULE_DESCRIPTION",
                        "message": "Rule entry is missing description.",
                        "source_path": source_path,
                        "local_id": local_id,
                    }
                )
            seen_local_ids[local_id] += 1
            canonical_id = self.canonical_format.format(
                domain=domain,
                kind=kind,
                document_name=document_name,
                local_id=local_id,
            )
            normalized_rules.append(
                {
                    "local_id": local_id,
                    "canonical_id": canonical_id,
                    "description": description or "",
                    "section_path": entry["_section_path"],
                    "implemented_in": self._collect_implemented_in(entry, source_path, issues, local_id),
                }
            )

        for local_id, count in seen_local_ids.items():
            if count > 1:
                issues.append(
                    {
                        "code": "DUPLICATE_LOCAL_ID_IN_FILE",
                        "message": "Local id is duplicated within the same file.",
                        "source_path": source_path,
                        "local_id": local_id,
                    }
                )

        return normalized_rules

    def _walk_sections(
        self,
        *,
        node: Any,
        current_path: list[str],
        section_names: set[str],
        found_entries: list[dict[str, Any]],
        source_path: str,
        issues: list[dict[str, Any]],
    ) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                normalized_key = self.section_aliases.get(key, key)
                next_path = [*current_path, key]
                if normalized_key in section_names:
                    self._collect_section_entries(
                        section_value=value,
                        section_path=next_path,
                        found_entries=found_entries,
                        source_path=source_path,
                        issues=issues,
                    )
                self._walk_sections(
                    node=value,
                    current_path=next_path,
                    section_names=section_names,
                    found_entries=found_entries,
                    source_path=source_path,
                    issues=issues,
                )
        elif isinstance(node, list):
            for index, item in enumerate(node):
                self._walk_sections(
                    node=item,
                    current_path=[*current_path, str(index)],
                    section_names=section_names,
                    found_entries=found_entries,
                    source_path=source_path,
                    issues=issues,
                )

    def _collect_section_entries(
        self,
        *,
        section_value: Any,
        section_path: list[str],
        found_entries: list[dict[str, Any]],
        source_path: str,
        issues: list[dict[str, Any]],
    ) -> None:
        if not isinstance(section_value, list):
            return
        for item in section_value:
            if isinstance(item, dict):
                found_entries.append({**item, "_section_path": section_path})
                continue
            if not self.allow_mixed_rule_entries:
                issues.append(
                    {
                        "code": "MIXED_RULE_ENTRY_TYPE",
                        "message": "Rule section contains non-object entries.",
                        "source_path": source_path,
                        "section_path": ".".join(section_path),
                    }
                )

    def _collect_implemented_in(
        self,
        entry: dict[str, Any],
        source_path: str,
        issues: list[dict[str, Any]],
        local_id: str,
    ) -> list[dict[str, Any]]:
        implementations = entry.get("implemented_in", [])
        if not isinstance(implementations, list):
            return []

        results: list[dict[str, Any]] = []
        for item in implementations:
            if not isinstance(item, dict):
                issues.append(
                    {
                        "code": "INVALID_IMPLEMENTED_IN_ENTRY",
                        "message": "implemented_in entry is missing required fields.",
                        "source_path": source_path,
                        "local_id": local_id,
                    }
                )
                continue
            path = item.get("path")
            status = item.get("status")
            if not isinstance(path, str) or not isinstance(status, str):
                issues.append(
                    {
                        "code": "INVALID_IMPLEMENTED_IN_ENTRY",
                        "message": "implemented_in entry is missing required fields.",
                        "source_path": source_path,
                        "local_id": local_id,
                    }
                )
                continue
            if status not in self.allowed_status_values:
                issues.append(
                    {
                        "code": "UNKNOWN_IMPLEMENTATION_STATUS",
                        "message": "implemented_in status is not allowed by the rule set.",
                        "source_path": source_path,
                        "local_id": local_id,
                        "status": status,
                    }
                )
            results.append(
                {
                    "path": path,
                    "status": status,
                    "line": item.get("line"),
                }
            )
        return results

    def _resolve_refs(
        self,
        data: dict[str, Any],
        source_path: Path,
        issues: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        refs: list[dict[str, Any]] = []

        def walk(node: Any, current_path: list[str]) -> None:
            if isinstance(node, dict):
                if "$ref" in node and isinstance(node["$ref"], str):
                    ref_value = node["$ref"]
                    resolved_path = (source_path.parent / ref_value).resolve()
                    exists = resolved_path.exists()
                    refs.append(
                        {
                            "ref": ref_value,
                            "resolved_path": str(resolved_path),
                            "exists": exists,
                            "section_path": current_path,
                        }
                    )
                    if self.require_ref_target_exists and not exists:
                        issues.append(
                            {
                                "code": "MISSING_REF_TARGET",
                                "message": "$ref target file does not exist.",
                                "source_path": str(source_path),
                                "ref": ref_value,
                            }
                        )
                for key, value in node.items():
                    walk(value, [*current_path, key])
            elif isinstance(node, list):
                for index, item in enumerate(node):
                    walk(item, [*current_path, str(index)])

        walk(data, [])
        return refs


def _format_text_report(report: dict[str, Any], language: str) -> str:
    summary = report["summary"]
    lines = [
        f"status: {_translate_status(summary['status'], language)}",
        f"total_documents: {summary['total_documents']}",
        f"total_rules: {summary['total_rules']}",
        f"total_refs: {summary['total_refs']}",
        f"total_implemented_in: {summary['total_implemented_in']}",
        f"total_issues: {summary['total_issues']}",
    ]
    for severity, count in report["issue_counts_by_severity"].items():
        lines.append(f"issues[{severity.lower()}]: {count}")
    for document in report["documents"]:
        lines.append(
            f"document: {document['domain']}/{document['kind']}/{document['document_name']} "
            f"rules={len(document['rules'])} refs={len(document['refs'])}"
        )
    for issue in report["issues"]:
        lines.append(
            f"issue[{_issue_severity(issue['code'])}/{issue['code']}]: {_issue_message(issue, language)}"
        )
    return "\n".join(lines)


def _format_markdown_report(report: dict[str, Any], language: str) -> str:
    summary = report["summary"]
    if language == "ja":
        lines = [
            "# 仕様構造検証レポート",
            "",
            f"- 生成日時: `{report['generated_at']}`",
            f"- ステータス: `{_translate_status(summary['status'], language)}`",
            f"- 総ドキュメント数: `{summary['total_documents']}`",
            f"- 総ルール数: `{summary['total_rules']}`",
            f"- 総参照数: `{summary['total_refs']}`",
            f"- 総 implemented_in 数: `{summary['total_implemented_in']}`",
            f"- 総 Issue 数: `{summary['total_issues']}`",
        ]
    else:
        lines = [
            "# Spec Structure Validation Report",
            "",
            f"- Generated At: `{report['generated_at']}`",
            f"- Status: `{summary['status']}`",
            f"- Total Documents: `{summary['total_documents']}`",
            f"- Total Rules: `{summary['total_rules']}`",
            f"- Total Refs: `{summary['total_refs']}`",
            f"- Total implemented_in: `{summary['total_implemented_in']}`",
            f"- Total Issues: `{summary['total_issues']}`",
        ]

    if report["spec_roots"]:
        joined = ", ".join(f"`{item}`" for item in report["spec_roots"])
        lines.append(f"- {'対象ルート' if language == 'ja' else 'Spec Roots'}: {joined}")

    lines.extend(["", "## " + ("Issue 集計" if language == "ja" else "Issue Counts"), ""])
    lines.append("| " + ("重要度" if language == "ja" else "Severity") + " | " + ("件数" if language == "ja" else "Count") + " |")
    lines.append("| --- | --- |")
    for severity, count in report["issue_counts_by_severity"].items():
        lines.append(f"| `{severity}` | `{count}` |")

    lines.extend(["", "## " + ("コード別集計" if language == "ja" else "By Code"), ""])
    if report["issue_counts"]:
        for code, count in report["issue_counts"].items():
            lines.append(f"- `{_issue_severity(code)}` `{code}`: {count}")
    else:
        lines.append("- " + ("なし" if language == "ja" else "None"))

    lines.extend(["", "## " + ("ドキュメント一覧" if language == "ja" else "Documents"), ""])
    lines.append(
        "| "
        + ("ドメイン" if language == "ja" else "Domain")
        + " | "
        + ("種別" if language == "ja" else "Kind")
        + " | "
        + ("ファイル" if language == "ja" else "File")
        + " | "
        + ("ルール数" if language == "ja" else "Rules")
        + " | "
        + ("参照数" if language == "ja" else "Refs")
        + " |"
    )
    lines.append("| --- | --- | --- | --- | --- |")
    for document in report["documents"]:
        lines.append(
            f"| `{document['domain']}` | `{document['kind']}` | `{document['source_path']}` | "
            f"`{len(document['rules'])}` | `{len(document['refs'])}` |"
        )

    lines.extend(["", "## " + ("ルール一覧" if language == "ja" else "Rules"), ""])
    for document in report["documents"]:
        lines.append(f"### `{document['source_path']}`")
        lines.append("")
        if document["rules"]:
            for rule in document["rules"]:
                lines.append(f"- `{rule['canonical_id']}`")
                lines.append(f"  - local id: `{rule['local_id']}`")
                if rule["description"]:
                    lines.append(f"  - {'説明' if language == 'ja' else 'Description'}: {rule['description']}")
                if rule["implemented_in"]:
                    lines.append(f"  - implemented_in: `{len(rule['implemented_in'])}`")
        else:
            lines.append(f"- {'ルールなし' if language == 'ja' else 'No rules'}")
        if document["refs"]:
            lines.append(f"- {'参照' if language == 'ja' else 'Refs'}:")
            for ref in document["refs"]:
                state = "OK" if ref["exists"] else "MISSING"
                lines.append(
                    f"  - `{ref['ref']}` -> `{ref['resolved_path']}` ({state})"
                )
        lines.append("")

    lines.extend(["## " + ("Issues 詳細" if language == "ja" else "Issues"), ""])
    if report["issues"]:
        for issue in report["issues"]:
            lines.append(
                f"- `{_issue_severity(issue['code'])}` `{issue['code']}`: {_issue_message(issue, language)}"
            )
            if "source_path" in issue:
                lines.append(f"  - source: `{issue['source_path']}`")
            if "canonical_id" in issue:
                lines.append(f"  - canonical_id: `{issue['canonical_id']}`")
            if "local_id" in issue:
                lines.append(f"  - local_id: `{issue['local_id']}`")
            if "ref" in issue:
                lines.append(f"  - ref: `{issue['ref']}`")
            if "kind" in issue:
                lines.append(f"  - kind: `{issue['kind']}`")
    else:
        lines.append("- " + ("なし" if language == "ja" else "None"))

    return "\n".join(lines) + "\n"


def _write_report(path: Path, report_format: str, report: dict[str, Any], language: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if report_format == "json":
        content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    else:
        content = _format_markdown_report(report, language)
    path.write_text(content, encoding="utf-8-sig")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate spec document structure, canonical ids, refs, and implemented_in fields."
    )
    parser.add_argument(
        "--spec-root",
        action="append",
        default=[],
        help="Spec root directory. Repeatable.",
    )
    parser.add_argument(
        "--structure-rules",
        default=str(SPEC_STRUCTURE_FILE),
        help="Path to 20_spec-structure.yaml",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Console output format.",
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
    parser.add_argument(
        "--language",
        choices=("ja", "en"),
        default="ja",
        help="Output language for text and markdown reports.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    spec_roots = [Path(item) for item in args.spec_root] if args.spec_root else [DEFAULT_SPECS_ROOT]

    validator = SpecStructureValidator(Path(args.structure_rules))
    report = validator.validate(spec_roots)

    if args.report:
        _write_report(Path(args.report), args.report_format, report, args.language)

    if args.format == "text":
        print(_format_text_report(report, args.language))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    return 0 if report["summary"]["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
