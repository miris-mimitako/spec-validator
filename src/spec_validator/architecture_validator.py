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
ARCHITECTURE_RULES_FILE = GROUND_RULES_DIR / "30_architecture-layer-rules.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


@dataclass(frozen=True)
class TypeDecl:
    name: str
    kind: str
    layer: str
    source_path: str
    implements: list[str]
    constructor_params: list[str]
    manual_news: list[str]


def _severity_for(code: str) -> str:
    return {
        "CONCRETE_CROSS_LAYER_DEPENDENCY": "ERROR",
        "PROVIDER_OWNED_INTERFACE": "ERROR",
        "MANUAL_CROSS_LAYER_INSTANTIATION": "ERROR",
        "FORBIDDEN_LAYER_DEPENDENCY": "ERROR",
        "MISSING_EXTERNAL_DI_REGISTRATION": "WARNING",
    }.get(code, "INFO")


class ArchitectureValidator:
    def __init__(self, rules_path: Path) -> None:
        self.rules_doc = _load_yaml(rules_path)
        self.layer_patterns = self._compile_layer_patterns()
        self.allowed_layer_dependencies = self._build_allowed_layer_dependencies()
        self.interface_name_pattern = re.compile(
            self.rules_doc["detection"]["interface_name_pattern"]
        )
        self.di_patterns = [
            re.compile(pattern) for pattern in self.rules_doc["detection"]["external_di_registration"]["patterns"]
        ]

    def _compile_layer_patterns(self) -> list[tuple[str, list[re.Pattern[str]]]]:
        compiled: list[tuple[str, list[re.Pattern[str]]]] = []
        for item in self.rules_doc["layers"]:
            compiled.append(
                (
                    item["layer_id"],
                    [re.compile(pattern) for pattern in item["path_patterns"]],
                )
            )
        return compiled

    def _build_allowed_layer_dependencies(self) -> dict[str, set[str]]:
        policy = self.rules_doc["policy"]["layer_dependency_policy"]
        allowed: dict[str, set[str]] = {}
        for layer_id, definition in policy.items():
            allowed[layer_id] = set(definition.get("allowed_layers", []))
        return allowed

    def validate(self, paths: list[Path]) -> dict[str, Any]:
        files = self._collect_cs_files(paths)
        declarations = [self._parse_csharp_file(path) for path in files]
        type_map = {decl.name: decl for decl in declarations}
        registrations = self._collect_di_registrations(files)

        issues: list[dict[str, Any]] = []
        cross_layer_contracts: list[dict[str, Any]] = []

        for decl in declarations:
            if decl.kind != "class":
                continue
            for param in decl.constructor_params:
                target = type_map.get(param)
                if not target:
                    continue
                if self._is_forbidden_layer_dependency(decl.layer, target.layer):
                    issues.append(
                        {
                            "code": "FORBIDDEN_LAYER_DEPENDENCY",
                            "message": self._format_forbidden_layer_message(decl.layer, target.layer),
                            "consumer_type": decl.name,
                            "consumer_layer": decl.layer,
                            "dependency_type": target.name,
                            "dependency_layer": target.layer,
                            "source_path": decl.source_path,
                        }
                    )
                if target.kind != "interface":
                    if target.layer == decl.layer:
                        continue
                    issues.append(
                        {
                            "code": "CONCRETE_CROSS_LAYER_DEPENDENCY",
                            "message": "Cross-layer dependency must not reference a concrete class.",
                            "consumer_type": decl.name,
                            "consumer_layer": decl.layer,
                            "dependency_type": target.name,
                            "dependency_layer": target.layer,
                            "source_path": decl.source_path,
                        }
                    )
                    continue
                if target.layer != decl.layer:
                    issues.append(
                        {
                            "code": "PROVIDER_OWNED_INTERFACE",
                            "message": "Cross-layer interface must be owned by the consuming layer.",
                            "consumer_type": decl.name,
                            "consumer_layer": decl.layer,
                            "interface_type": target.name,
                            "interface_layer": target.layer,
                            "source_path": decl.source_path,
                        }
                    )
                    continue
                implementations = [
                    candidate
                    for candidate in declarations
                    if candidate.kind == "class"
                    and target.name in candidate.implements
                    and candidate.layer != decl.layer
                ]
                for implementation in implementations:
                    cross_layer_contracts.append(
                        {
                            "consumer_type": decl.name,
                            "consumer_layer": decl.layer,
                            "interface_type": target.name,
                            "interface_layer": target.layer,
                            "implementation_type": implementation.name,
                            "implementation_layer": implementation.layer,
                        }
                    )
                    if (target.name, implementation.name) not in registrations:
                        issues.append(
                            {
                                "code": "MISSING_EXTERNAL_DI_REGISTRATION",
                                "message": "Cross-layer contract must be registered in an external DI composition root.",
                                "consumer_type": decl.name,
                                "interface_type": target.name,
                                "implementation_type": implementation.name,
                                "source_path": implementation.source_path,
                            }
                        )

            for created_type in decl.manual_news:
                target = type_map.get(created_type)
                if not target or target.layer == decl.layer:
                    continue
                if self._is_forbidden_layer_dependency(decl.layer, target.layer):
                    issues.append(
                        {
                            "code": "FORBIDDEN_LAYER_DEPENDENCY",
                            "message": self._format_forbidden_layer_message(decl.layer, target.layer),
                            "consumer_type": decl.name,
                            "consumer_layer": decl.layer,
                            "dependency_type": target.name,
                            "dependency_layer": target.layer,
                            "source_path": decl.source_path,
                        }
                    )
                issues.append(
                    {
                        "code": "MANUAL_CROSS_LAYER_INSTANTIATION",
                        "message": "Cross-layer dependency must not be created with manual instantiation.",
                        "consumer_type": decl.name,
                        "consumer_layer": decl.layer,
                        "dependency_type": target.name,
                        "dependency_layer": target.layer,
                        "source_path": decl.source_path,
                    }
                )

        issues = self._deduplicate_issues(issues)
        issue_counts = Counter(issue["code"] for issue in issues)
        issue_counts_by_severity = Counter(_severity_for(issue["code"]) for issue in issues)
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "paths": [str(path) for path in paths],
            "layer_dependency_policy": {
                layer: sorted(targets) for layer, targets in sorted(self.allowed_layer_dependencies.items())
            },
            "summary": {
                "status": "success" if not issues else "failure",
                "total_files": len(files),
                "total_types": len(declarations),
                "total_contracts": len(cross_layer_contracts),
                "total_issues": len(issues),
            },
            "issue_counts": dict(sorted(issue_counts.items())),
            "issue_counts_by_severity": {
                severity: issue_counts_by_severity.get(severity, 0)
                for severity in ("ERROR", "WARNING", "INFO")
            },
            "contracts": cross_layer_contracts,
            "issues": issues,
        }

    def _deduplicate_issues(self, issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
        unique: list[dict[str, Any]] = []
        seen: set[tuple[Any, ...]] = set()
        for issue in issues:
            key = (
                issue.get("code"),
                issue.get("consumer_type"),
                issue.get("consumer_layer"),
                issue.get("dependency_type"),
                issue.get("dependency_layer"),
                issue.get("interface_type"),
                issue.get("interface_layer"),
                issue.get("implementation_type"),
                issue.get("implementation_layer"),
                issue.get("source_path"),
            )
            if key in seen:
                continue
            seen.add(key)
            unique.append(issue)
        return unique

    def _is_forbidden_layer_dependency(self, source_layer: str, target_layer: str) -> bool:
        if source_layer == target_layer:
            return False
        allowed_targets = self.allowed_layer_dependencies.get(source_layer)
        if allowed_targets is None:
            return False
        return target_layer not in allowed_targets

    def _format_forbidden_layer_message(self, source_layer: str, target_layer: str) -> str:
        return (
            "Layer dependency direction is forbidden by architecture policy: "
            f"{source_layer} -> {target_layer}."
        )

    def _collect_cs_files(self, paths: list[Path]) -> list[Path]:
        collected: list[Path] = []
        for path in paths:
            if path.is_file() and path.suffix == ".cs":
                collected.append(path)
                continue
            collected.extend(sorted(candidate for candidate in path.rglob("*.cs") if candidate.is_file()))
        return collected

    def _detect_layer(self, path: Path) -> str:
        normalized = str(path).replace("/", "\\")
        for layer_id, patterns in self.layer_patterns:
            for pattern in patterns:
                if pattern.search(normalized):
                    return layer_id
        return "unknown"

    def _parse_csharp_file(self, path: Path) -> TypeDecl:
        text = path.read_text(encoding="utf-8-sig")
        layer = self._detect_layer(path)
        class_match = re.search(
            r"\b(?:public|internal|private|protected)?\s*(?:sealed\s+|abstract\s+|partial\s+)*class\s+([A-Za-z_][A-Za-z0-9_]*)(?:\s*:\s*([^{]+))?",
            text,
        )
        interface_match = re.search(
            r"\b(?:public|internal|private|protected)?\s*interface\s+([A-Za-z_][A-Za-z0-9_]*)",
            text,
        )
        record_match = re.search(
            r"\b(?:public|internal|private|protected)?\s*(?:sealed\s+|partial\s+)*record\s+([A-Za-z_][A-Za-z0-9_]*)(?:\s*:\s*([^{]+))?",
            text,
        )

        name = path.stem
        kind = "class"
        implements: list[str] = []
        constructor_params: list[str] = []

        if interface_match:
            name = interface_match.group(1)
            kind = "interface"
        elif record_match:
            name = record_match.group(1)
            kind = "record"
            implements = self._split_base_types(record_match.group(2))
        elif class_match:
            name = class_match.group(1)
            kind = "class"
            implements = self._split_base_types(class_match.group(2))
            ctor_pattern = re.compile(
                rf"\bpublic\s+{re.escape(name)}\s*\((.*?)\)",
                re.DOTALL,
            )
            for match in ctor_pattern.finditer(text):
                constructor_params.extend(self._extract_param_types(match.group(1)))

        manual_news = re.findall(
            self.rules_doc["detection"]["manual_instantiation"]["pattern"],
            text,
        )
        return TypeDecl(
            name=name,
            kind=kind,
            layer=layer,
            source_path=str(path),
            implements=implements,
            constructor_params=constructor_params,
            manual_news=manual_news,
        )

    def _split_base_types(self, raw: str | None) -> list[str]:
        if not raw:
            return []
        items = []
        for part in raw.split(","):
            token = part.strip().split("<", 1)[0].strip()
            if token:
                items.append(token.split(".")[-1])
        return items

    def _extract_param_types(self, raw: str) -> list[str]:
        types: list[str] = []
        for part in raw.split(","):
            cleaned = re.sub(r"\s+", " ", part.strip())
            if not cleaned:
                continue
            cleaned = re.sub(r"\b(this|params|ref|out|in|required|readonly)\b", "", cleaned)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            tokens = cleaned.split(" ")
            if len(tokens) < 2:
                continue
            type_name = tokens[-2]
            type_name = type_name.split("<", 1)[0].split(".")[-1].strip("?")
            if type_name:
                types.append(type_name)
        return types

    def _collect_di_registrations(self, files: list[Path]) -> set[tuple[str, str]]:
        registrations: set[tuple[str, str]] = set()
        for path in files:
            text = path.read_text(encoding="utf-8-sig")
            if self._detect_layer(path) != "composition_root":
                continue
            for pattern in self.di_patterns:
                for match in pattern.finditer(text):
                    registrations.add((match.group("interface"), match.group("implementation")))
        return registrations


def _format_text(report: dict[str, Any]) -> str:
    lines = [
        f"status: {report['summary']['status']}",
        f"total_files: {report['summary']['total_files']}",
        f"total_types: {report['summary']['total_types']}",
        f"total_contracts: {report['summary']['total_contracts']}",
        f"total_issues: {report['summary']['total_issues']}",
    ]
    for severity, count in report["issue_counts_by_severity"].items():
        lines.append(f"issues[{severity.lower()}]: {count}")
    for issue in report["issues"]:
        lines.append(f"issue[{_severity_for(issue['code'])}/{issue['code']}]: {issue['message']}")
    return "\n".join(lines)


def _format_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Architecture Validation Report",
        "",
        f"- Generated At: `{report['generated_at']}`",
        f"- Status: `{report['summary']['status']}`",
        f"- Total Files: `{report['summary']['total_files']}`",
        f"- Total Types: `{report['summary']['total_types']}`",
        f"- Total Contracts: `{report['summary']['total_contracts']}`",
        f"- Total Issues: `{report['summary']['total_issues']}`",
    ]
    if report["paths"]:
        joined = ", ".join(f"`{item}`" for item in report["paths"])
        lines.append(f"- Paths: {joined}")

    lines.extend(["", "## Layer Dependency Policy", ""])
    lines.append("| Source Layer | Allowed Target Layers |")
    lines.append("| --- | --- |")
    for source_layer, targets in report["layer_dependency_policy"].items():
        rendered_targets = ", ".join(f"`{target}`" for target in targets) if targets else "`(none)`"
        lines.append(f"| `{source_layer}` | {rendered_targets} |")

    lines.extend(["", "## Issue Counts", ""])
    lines.append("| Severity | Count |")
    lines.append("| --- | --- |")
    for severity, count in report["issue_counts_by_severity"].items():
        lines.append(f"| `{severity}` | `{count}` |")
    lines.append("")
    if report["issue_counts"]:
        for code, count in report["issue_counts"].items():
            lines.append(f"- `{_severity_for(code)}` `{code}`: {count}")
    else:
        lines.append("- None")

    lines.extend(["", "## Contracts", ""])
    if report["contracts"]:
        lines.append("| Consumer | Interface | Implementation |")
        lines.append("| --- | --- | --- |")
        for item in report["contracts"]:
            lines.append(
                f"| `{item['consumer_type']} ({item['consumer_layer']})` | "
                f"`{item['interface_type']} ({item['interface_layer']})` | "
                f"`{item['implementation_type']} ({item['implementation_layer']})` |"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Issues", ""])
    if report["issues"]:
        for issue in report["issues"]:
            lines.append(f"- `{_severity_for(issue['code'])}` `{issue['code']}`: {issue['message']}")
            if "consumer_type" in issue:
                lines.append(f"  - consumer: `{issue['consumer_type']}`")
            if "consumer_layer" in issue:
                lines.append(f"  - consumer layer: `{issue['consumer_layer']}`")
            if "interface_type" in issue:
                lines.append(f"  - interface: `{issue['interface_type']}`")
            if "interface_layer" in issue:
                lines.append(f"  - interface layer: `{issue['interface_layer']}`")
            if "implementation_type" in issue:
                lines.append(f"  - implementation: `{issue['implementation_type']}`")
            if "implementation_layer" in issue:
                lines.append(f"  - implementation layer: `{issue['implementation_layer']}`")
            if "dependency_type" in issue:
                lines.append(f"  - dependency: `{issue['dependency_type']}`")
            if "dependency_layer" in issue:
                lines.append(f"  - dependency layer: `{issue['dependency_layer']}`")
            if "source_path" in issue:
                lines.append(f"  - source: `{issue['source_path']}`")
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def _write_report(path: Path, report_format: str, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if report_format == "json" else _format_markdown(report)
    path.write_text(content, encoding="utf-8-sig")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate layered architecture DIP rules for C#.")
    parser.add_argument("--path", action="append", default=[], help="C# file or directory to scan. Repeatable.")
    parser.add_argument("--rules", default=str(ARCHITECTURE_RULES_FILE), help="Path to 30_architecture-layer-rules.yaml")
    parser.add_argument("--format", choices=("json", "text"), default="json", help="Console output format.")
    parser.add_argument("--report", help="Write a validation report to this file path.")
    parser.add_argument("--report-format", choices=("markdown", "json"), default="markdown", help="Report file format.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.path:
        parser.error("Provide at least one --path.")

    validator = ArchitectureValidator(Path(args.rules))
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
