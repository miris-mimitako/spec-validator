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
DOCS_DIR = ROOT_DIR / "_docs"
DOCUMENTS_DIR = DOCS_DIR / "_Documents"
GROUND_RULES_DIR = DOCS_DIR / "_GroundRules"
DOMAIN_RULES_FILE = DOCUMENTS_DIR / "10_domain-rule.yaml"
TEST_RULES_FILE = GROUND_RULES_DIR / "10_test-rules.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def _collect_files(paths: list[Path]) -> list[Path]:
    collected: list[Path] = []
    for path in paths:
        if path.is_file():
            collected.append(path)
            continue
        collected.extend(
            candidate
            for candidate in sorted(path.rglob("*"))
            if candidate.is_file() and "node_modules" not in candidate.parts
        )
    return collected


@dataclass(frozen=True)
class GeneratedCase:
    suffix: str
    sequence_required: bool
    description: str


@dataclass(frozen=True)
class TestPattern:
    pattern_id: str
    generated_cases: list[GeneratedCase]
    minimum_cases: int
    multi_rule_support: dict[str, Any]


@dataclass(frozen=True)
class DomainRule:
    rule_id: str
    name: str
    rule_type: str
    implementation_id: str
    required_test_patterns: list[str]
    required_test_layers: list[str]
    related_rule_ids: list[str]
    minimum_implementation_refs: int
    minimum_test_refs: int


@dataclass(frozen=True)
class Annotation:
    annotation_type: str
    value: str
    source_path: str
    line_number: int
    reason: str | None = None
    test_layer: str | None = None
    related_rule_ids: list[str] | None = None


def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 1.0
    return numerator / denominator


def _to_percent(value: float) -> int:
    return round(value * 100)


class TraceabilityValidator:
    def __init__(
        self,
        domain_rules_path: Path,
        test_rules_path: Path,
    ) -> None:
        self.domain_rules_doc = _load_yaml(domain_rules_path)
        self.test_rules_doc = _load_yaml(test_rules_path)
        self.domain_rules = self._collect_domain_rules()
        self.test_patterns = self._collect_test_patterns()
        self.comment_extraction = self.test_rules_doc["comment_extraction"]
        self.test_layers = self._collect_test_layers()
        self.impl_validation_pattern = re.compile(
            self.test_rules_doc["traceability_rules"]["implementation_annotation"][
                "required_pattern"
            ]
        )
        self.test_id_validation_pattern = re.compile(
            self.test_rules_doc["naming"]["base_test_id_pattern"]
        )
        self.omitted_validation_pattern = re.compile(
            self.test_rules_doc["omitted_rule"]["required_pattern"]
        )
        self.impl_extract_pattern = re.compile(
            self.comment_extraction["loose_detection"]["implementation_token_pattern"]
        )
        self.test_id_extract_pattern = re.compile(
            self.comment_extraction["loose_detection"]["test_token_pattern"]
        )
        self.omitted_extract_pattern = re.compile(
            self.comment_extraction["loose_detection"]["omitted_token_pattern"]
        )
        self.implementation_comment_pattern = re.compile(
            self.comment_extraction["implementation_comment_pattern"]
        )
        self.test_comment_pattern = re.compile(
            self.comment_extraction["test_comment_pattern"]
        )
        self.omitted_comment_pattern = re.compile(
            self.comment_extraction["omitted_comment_pattern"]
        )
        self.related_rules_comment_pattern = re.compile(
            self.comment_extraction["related_rules_comment_pattern"]
        )
        self.related_rule_extract_pattern = re.compile(
            self.comment_extraction["loose_detection"]["related_rule_token_pattern"]
        )

    def _collect_test_layers(self) -> list[dict[str, Any]]:
        layers: list[dict[str, Any]] = []
        for item in self.test_rules_doc.get("test_layers", {}).get("definitions", []):
            layers.append(
                {
                    "layer_id": item["layer_id"],
                    "patterns": [re.compile(pattern) for pattern in item.get("path_patterns", [])],
                }
            )
        return layers

    def _collect_domain_rules(self) -> dict[str, DomainRule]:
        rules: dict[str, DomainRule] = {}
        for domain in self.domain_rules_doc.get("domains", []):
            for item in domain.get("rules", []):
                rule = DomainRule(
                    rule_id=item["rule_id"],
                    name=item["name"],
                    rule_type=item["rule_type"],
                    implementation_id=item["implementation"]["implementation_id"],
                    required_test_patterns=item["traceability"]["required_test_patterns"],
                    required_test_layers=item["traceability"].get("required_test_layers", []),
                    related_rule_ids=item["traceability"].get("related_rule_ids", []),
                    minimum_implementation_refs=item["traceability"][
                        "minimum_implementation_refs"
                    ],
                    minimum_test_refs=item["traceability"]["minimum_test_refs"],
                )
                rules[rule.rule_id] = rule
        return rules

    def _collect_test_patterns(self) -> dict[str, TestPattern]:
        patterns: dict[str, TestPattern] = {}
        for item in self.test_rules_doc.get("test_patterns", []):
            patterns[item["pattern_id"]] = TestPattern(
                pattern_id=item["pattern_id"],
                generated_cases=[
                    GeneratedCase(
                        suffix=case["suffix"],
                        sequence_required=case["sequence_required"],
                        description=case["description"],
                    )
                    for case in item.get("generated_cases", [])
                ],
                minimum_cases=item["minimum_cases"],
                multi_rule_support=item.get("multi_rule_support", {"enabled": False}),
            )
        return patterns

    def scan_paths(
        self,
        implementation_paths: list[Path],
        test_paths: list[Path],
    ) -> dict[str, list[Annotation]]:
        implementation_annotations = self._scan_files(_collect_files(implementation_paths), "impl")
        test_annotations = self._scan_files(_collect_files(test_paths), "test")
        return {
            "implementation_annotations": implementation_annotations,
            "test_annotations": test_annotations,
        }

    def _scan_files(self, files: list[Path], scan_kind: str) -> list[Annotation]:
        annotations: list[Annotation] = []
        for path in files:
            text = path.read_text(encoding="utf-8")
            for line_number, line in enumerate(text.splitlines(), start=1):
                annotations.extend(self._scan_line(path, line_number, line, scan_kind))
        return annotations

    def _scan_line(
        self,
        path: Path,
        line_number: int,
        line: str,
        scan_kind: str,
    ) -> list[Annotation]:
        annotations: list[Annotation] = []
        source_path = str(path)
        if scan_kind == "impl":
            strict_match = self.implementation_comment_pattern.match(line)
            if strict_match:
                annotations.append(
                    Annotation(
                        annotation_type="implementation",
                        value=strict_match.group(1),
                        source_path=source_path,
                        line_number=line_number,
                    )
                )
                return annotations

            if self.comment_extraction["invalid_format_is_error"]:
                for match in self.impl_extract_pattern.finditer(line):
                    token = match.group(0)
                    if not self.impl_validation_pattern.fullmatch(token):
                        continue
                    annotations.append(
                        Annotation(
                            annotation_type="invalid_implementation_format",
                            value=token,
                            source_path=source_path,
                            line_number=line_number,
                        )
                    )
            return annotations

        test_layer = self._detect_test_layer(path)
        related_rules_match = self.related_rules_comment_pattern.match(line)
        if related_rules_match:
            related_rule_ids = [item.strip() for item in related_rules_match.group(1).split(",")]
            annotations.append(
                Annotation(
                    annotation_type="related_rules",
                    value=related_rules_match.group(1),
                    source_path=source_path,
                    line_number=line_number,
                    test_layer=test_layer,
                    related_rule_ids=related_rule_ids,
                )
            )
            return annotations
        omitted_match = self.omitted_comment_pattern.match(line)
        if omitted_match:
            token = omitted_match.group(1)
            value_with_reason = omitted_match.group(0).split("TRACE:", 1)[1].strip()
            if self.omitted_validation_pattern.fullmatch(value_with_reason):
                annotations.append(
                    Annotation(
                        annotation_type="omitted",
                        value=token,
                        source_path=source_path,
                        line_number=line_number,
                        reason=omitted_match.group(2).strip(),
                        test_layer=test_layer,
                    )
                )
            return annotations

        test_match = self.test_comment_pattern.match(line)
        if test_match:
            annotations.append(
                Annotation(
                    annotation_type="test",
                    value=test_match.group(1),
                    source_path=source_path,
                    line_number=line_number,
                    test_layer=test_layer,
                )
            )
            return annotations

        if self.comment_extraction["invalid_format_is_error"]:
            for match in self.related_rule_extract_pattern.finditer(line):
                token = match.group(0)
                if token.count("domain-rule-") >= 2:
                    annotations.append(
                        Annotation(
                            annotation_type="invalid_related_rules_format",
                            value=token,
                            source_path=source_path,
                            line_number=line_number,
                            test_layer=test_layer,
                        )
                    )
            for match in self.omitted_extract_pattern.finditer(line):
                token = match.group(0)
                if token.endswith("-OMITTED"):
                    annotations.append(
                        Annotation(
                            annotation_type="invalid_test_format",
                            value=token,
                            source_path=source_path,
                            line_number=line_number,
                            test_layer=test_layer,
                        )
                    )
            for match in self.test_id_extract_pattern.finditer(line):
                token = match.group(0)
                if not self.test_id_validation_pattern.fullmatch(token):
                    continue
                annotations.append(
                    Annotation(
                        annotation_type="invalid_test_format",
                        value=token,
                        source_path=source_path,
                        line_number=line_number,
                        test_layer=test_layer,
                    )
                )
        return annotations

    def _detect_test_layer(self, path: Path) -> str:
        normalized = str(path).replace("/", "\\")
        for layer in self.test_layers:
            for pattern in layer["patterns"]:
                if pattern.search(normalized):
                    return layer["layer_id"]
        return self.test_rules_doc["test_layers"]["default_layer"]

    def validate(
        self,
        implementation_paths: list[Path],
        test_paths: list[Path],
    ) -> dict[str, Any]:
        scanned = self.scan_paths(implementation_paths, test_paths)
        implementation_annotations = scanned["implementation_annotations"]
        test_annotations = scanned["test_annotations"]

        implementation_by_id: dict[str, list[Annotation]] = {}
        for annotation in implementation_annotations:
            if annotation.annotation_type != "implementation":
                continue
            implementation_by_id.setdefault(annotation.value, []).append(annotation)

        observed_test_ids: dict[str, list[Annotation]] = {}
        observed_omitted_ids: dict[str, list[Annotation]] = {}
        unmapped_test_annotations: list[Annotation] = []
        duplicate_test_ids: list[dict[str, Any]] = []
        invalid_comment_annotations: list[Annotation] = []
        directional_combo_links: dict[tuple[str, str], int] = {}
        related_rules_by_location: dict[tuple[str, int], Annotation] = {}

        expected_test_ids = self._expected_test_ids_by_rule()
        expected_case_keys = {
            (rule_id, suffix)
            for rule_id, suffixes in expected_test_ids.items()
            for suffix in suffixes
        }

        for annotation in test_annotations:
            if annotation.annotation_type == "related_rules":
                related_rules_by_location[(annotation.source_path, annotation.line_number)] = annotation

        for annotation in test_annotations:
            if annotation.annotation_type == "related_rules":
                continue
            if annotation.annotation_type == "invalid_test_format":
                invalid_comment_annotations.append(annotation)
                continue
            if annotation.annotation_type == "invalid_related_rules_format":
                invalid_comment_annotations.append(annotation)
                continue
            if annotation.annotation_type == "omitted":
                annotation = self._attach_related_rules(annotation, related_rules_by_location)
                parsed = self._parse_omitted_id(annotation.value)
                if parsed and (parsed["rule_id"], parsed["suffix"]) in expected_case_keys:
                    key = annotation.value
                    observed_omitted_ids.setdefault(key, []).append(annotation)
                    self._register_combo_link(
                        directional_combo_links,
                        parsed["rule_id"],
                        parsed["suffix"],
                        annotation.related_rule_ids or [],
                    )
                else:
                    unmapped_test_annotations.append(annotation)
                continue

            annotation = self._attach_related_rules(annotation, related_rules_by_location)
            parsed = self._parse_test_id(annotation.value)
            if not parsed or (parsed["rule_id"], parsed["suffix"]) not in expected_case_keys:
                unmapped_test_annotations.append(annotation)
                continue

            observed_test_ids.setdefault(annotation.value, []).append(annotation)
            self._register_combo_link(
                directional_combo_links,
                parsed["rule_id"],
                parsed["suffix"],
                annotation.related_rule_ids or [],
            )

        for test_id, annotations in observed_test_ids.items():
            if len(annotations) > 1:
                duplicate_test_ids.append(
                    {
                        "test_id": test_id,
                        "occurrences": [
                            {
                                "source_path": item.source_path,
                                "line_number": item.line_number,
                            }
                            for item in annotations
                        ],
                    }
                )

        rule_results: list[dict[str, Any]] = []
        issues: list[dict[str, Any]] = []

        config_relation_issues = self._validate_related_rule_config()
        for issue in config_relation_issues:
            issues.append(issue)

        for rule in self.domain_rules.values():
            implementation_refs = implementation_by_id.get(rule.implementation_id, [])
            expected_suffixes = expected_test_ids[rule.rule_id]
            observed_cases: list[dict[str, Any]] = []
            missing_cases: list[dict[str, Any]] = []
            case_matrix: list[dict[str, Any]] = []

            total_test_refs = 0
            for suffix in expected_suffixes:
                matching_tests = self._matching_test_annotations(
                    observed_test_ids,
                    rule.rule_id,
                    suffix,
                )
                matching_omitted = self._matching_omitted_annotations(
                    observed_omitted_ids,
                    rule.rule_id,
                    suffix,
                )
                total_test_refs += len(matching_tests) + len(matching_omitted)
                case_status = self._case_status(matching_tests, matching_omitted)
                case_matrix.append(
                    {
                        "suffix": suffix,
                        "status": case_status,
                        "tests": [self._annotation_to_dict(item) for item in matching_tests],
                        "omitted": [self._annotation_to_dict(item) for item in matching_omitted],
                    }
                )
                if matching_tests or matching_omitted:
                    observed_cases.append(
                        {
                            "suffix": suffix,
                            "tests": [self._annotation_to_dict(item) for item in matching_tests],
                            "omitted": [self._annotation_to_dict(item) for item in matching_omitted],
                        }
                    )
                else:
                    missing_cases.append({"suffix": suffix})

            rule_issues: list[dict[str, Any]] = []
            for issue in config_relation_issues:
                if issue["rule_id"] == rule.rule_id:
                    rule_issues.append(issue)
            if len(implementation_refs) < rule.minimum_implementation_refs:
                issue = {
                    "code": "MISSING_IMPLEMENTATION_REF",
                    "rule_id": rule.rule_id,
                    "message": "Implementation annotation is missing.",
                    "expected": rule.implementation_id,
                    "minimum_required": rule.minimum_implementation_refs,
                    "observed": len(implementation_refs),
                }
                rule_issues.append(issue)
                issues.append(issue)

            if total_test_refs < rule.minimum_test_refs:
                issue = {
                    "code": "INSUFFICIENT_TEST_REFS",
                    "rule_id": rule.rule_id,
                    "message": "Required number of test references was not met.",
                    "minimum_required": rule.minimum_test_refs,
                    "observed": total_test_refs,
                }
                rule_issues.append(issue)
                issues.append(issue)

            for missing in missing_cases:
                issue = {
                    "code": "MISSING_TEST_CASE",
                    "rule_id": rule.rule_id,
                    "message": "Required test case suffix is missing.",
                    "suffix": missing["suffix"],
                }
                rule_issues.append(issue)
                issues.append(issue)

            rule_layer_summary = self._build_rule_layer_summary(case_matrix)
            missing_layers = [
                layer for layer in rule.required_test_layers if layer not in rule_layer_summary
            ]
            for layer in missing_layers:
                issue = {
                    "code": "MISSING_REQUIRED_TEST_LAYER",
                    "rule_id": rule.rule_id,
                    "message": "Required test layer is missing.",
                    "layer": layer,
                }
                rule_issues.append(issue)
                issues.append(issue)

            combination_issues = self._validate_combination_metadata(
                rule=rule,
                case_matrix=case_matrix,
            )
            for issue in combination_issues:
                rule_issues.append(issue)
                issues.append(issue)

            reverse_link_issues = self._validate_bidirectional_combo_links(
                rule=rule,
                directional_combo_links=directional_combo_links,
            )
            for issue in reverse_link_issues:
                rule_issues.append(issue)
                issues.append(issue)

            implementation_coverage = _ratio(
                min(len(implementation_refs), rule.minimum_implementation_refs),
                rule.minimum_implementation_refs,
            )
            test_case_coverage = _ratio(
                len(expected_suffixes) - len(missing_cases),
                len(expected_suffixes),
            )
            observed_case_count = sum(
                1 for case in case_matrix if case["status"] in {"PASS", "OMITTED"}
            )
            observed_layers = len(
                [layer for layer in rule.required_test_layers if layer in rule_layer_summary]
            )
            layer_coverage = _ratio(observed_layers, len(rule.required_test_layers))
            traceability_coverage = _ratio(
                (
                    min(len(implementation_refs), rule.minimum_implementation_refs)
                    + observed_case_count
                ),
                rule.minimum_implementation_refs + len(expected_suffixes),
            )
            rule_status = self._determine_rule_status(
                missing_cases=missing_cases,
                implementation_refs=implementation_refs,
                minimum_implementation_refs=rule.minimum_implementation_refs,
                has_omitted=any(case["status"] == "OMITTED" for case in case_matrix),
                rule_issues=rule_issues,
            )
            summary_text = self._build_rule_summary(
                rule=rule,
                rule_status=rule_status,
                implementation_refs=implementation_refs,
                expected_suffixes=expected_suffixes,
                missing_cases=missing_cases,
                case_matrix=case_matrix,
                missing_layers=missing_layers,
                rule_issues=rule_issues,
            )

            rule_results.append(
                {
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "valid": not rule_issues,
                    "status": rule_status,
                    "summary_text": summary_text,
                    "minimum_implementation_refs": rule.minimum_implementation_refs,
                    "implementation_id": rule.implementation_id,
                    "implementation_refs": [
                        self._annotation_to_dict(item) for item in implementation_refs
                    ],
                    "observed_cases": observed_cases,
                    "case_matrix": case_matrix,
                    "missing_cases": missing_cases,
                    "required_test_layers": rule.required_test_layers,
                    "missing_test_layers": missing_layers,
                    "coverage": {
                        "implementation_ref_coverage": implementation_coverage,
                        "test_case_coverage": test_case_coverage,
                        "test_layer_coverage": layer_coverage,
                        "traceability_coverage": traceability_coverage,
                    },
                    "layer_summary": rule_layer_summary,
                    "issues": rule_issues,
                }
            )

        for annotation in implementation_annotations:
            if annotation.annotation_type == "invalid_implementation_format":
                issues.append(
                    {
                        "code": "INVALID_IMPLEMENTATION_COMMENT_FORMAT",
                        "message": "Implementation annotation must use the configured TRACE comment format.",
                        "annotation": self._annotation_to_dict(annotation),
                    }
                )
                continue
            if annotation.value not in {rule.implementation_id for rule in self.domain_rules.values()}:
                issues.append(
                    {
                        "code": "UNMAPPED_IMPLEMENTATION_ID",
                        "message": "Implementation annotation does not map to a known rule.",
                        "annotation": self._annotation_to_dict(annotation),
                    }
                )

        for annotation in unmapped_test_annotations:
            issues.append(
                {
                    "code": "UNMAPPED_TEST_ID",
                    "message": "Test annotation does not map to a known expected test case.",
                    "annotation": self._annotation_to_dict(annotation),
                }
            )

        for item in duplicate_test_ids:
            issues.append(
                {
                    "code": "DUPLICATE_TEST_ID",
                    "message": "Test ID appears multiple times.",
                    **item,
                }
            )

        for annotation in invalid_comment_annotations:
            issues.append(
                {
                    "code": (
                        "INVALID_RELATED_RULES_COMMENT_FORMAT"
                        if annotation.annotation_type == "invalid_related_rules_format"
                        else "INVALID_TEST_COMMENT_FORMAT"
                    ),
                    "message": (
                        "TRACE-RULES annotation must use the configured comment format."
                        if annotation.annotation_type == "invalid_related_rules_format"
                        else "Test annotation must use the configured TRACE comment format."
                    ),
                    "annotation": self._annotation_to_dict(annotation),
                }
            )

        passed_rules = [item for item in rule_results if item["valid"]]
        failed_rules = [item for item in rule_results if not item["valid"]]
        issue_counts: dict[str, int] = {}
        for issue in issues:
            issue_counts[issue["code"]] = issue_counts.get(issue["code"], 0) + 1

        layer_summary = self._build_global_layer_summary(
            list(observed_test_ids.values()),
            list(observed_omitted_ids.values()),
            rule_results,
        )

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "implementation_paths": [str(path) for path in implementation_paths],
            "test_paths": [str(path) for path in test_paths],
            "summary": {
                "total_rules": len(rule_results),
                "passed_rules": len(passed_rules),
                "failed_rules": len(failed_rules),
                "total_issues": len(issues),
                "status": "success" if not issues else "failure",
            },
            "issue_counts": dict(sorted(issue_counts.items())),
            "layer_summary": layer_summary,
            "rules": rule_results,
            "issues": issues,
        }

    def _register_combo_link(
        self,
        directional_combo_links: dict[tuple[str, str], int],
        primary_rule_id: str,
        suffix: str,
        related_rule_ids: list[str],
    ) -> None:
        if not suffix.startswith("COMBO-"):
            return
        for related_rule_id in related_rule_ids:
            if related_rule_id == primary_rule_id:
                continue
            key = (primary_rule_id, related_rule_id)
            directional_combo_links[key] = directional_combo_links.get(key, 0) + 1

    def _validate_related_rule_config(self) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        for rule in self.domain_rules.values():
            for related_rule_id in rule.related_rule_ids:
                related_rule = self.domain_rules.get(related_rule_id)
                if not related_rule:
                    issues.append(
                        {
                            "code": "UNKNOWN_RELATED_RULE_ID",
                            "rule_id": rule.rule_id,
                            "message": "Related rule id is not defined in domain rules.",
                            "related_rule_id": related_rule_id,
                        }
                    )
                    continue
                if rule.rule_id not in related_rule.related_rule_ids:
                    issues.append(
                        {
                            "code": "MISSING_REVERSE_RULE_RELATION_CONFIG",
                            "rule_id": rule.rule_id,
                            "message": "Related rule config is not bidirectional.",
                            "related_rule_id": related_rule_id,
                        }
                    )
        return issues

    def _validate_bidirectional_combo_links(
        self,
        *,
        rule: DomainRule,
        directional_combo_links: dict[tuple[str, str], int],
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        combo_required = "cross-rule-combination" in rule.required_test_patterns
        if not combo_required:
            return issues

        for related_rule_id in rule.related_rule_ids:
            if directional_combo_links.get((rule.rule_id, related_rule_id), 0) == 0:
                issues.append(
                    {
                        "code": "MISSING_COMBINATION_DIRECTION",
                        "rule_id": rule.rule_id,
                        "message": "No combination annotation was found from this rule to the related rule.",
                        "related_rule_id": related_rule_id,
                    }
                )
            if directional_combo_links.get((related_rule_id, rule.rule_id), 0) == 0:
                issues.append(
                    {
                        "code": "MISSING_REVERSE_COMBINATION_DIRECTION",
                        "rule_id": rule.rule_id,
                        "message": "No reverse combination annotation was found from the related rule back to this rule.",
                        "related_rule_id": related_rule_id,
                    }
                )
        return issues

    def _case_status(
        self,
        matching_tests: list[Annotation],
        matching_omitted: list[Annotation],
    ) -> str:
        if matching_tests:
            return "PASS"
        if matching_omitted:
            return "OMITTED"
        return "MISSING"

    def _determine_rule_status(
        self,
        *,
        missing_cases: list[dict[str, Any]],
        implementation_refs: list[Annotation],
        minimum_implementation_refs: int,
        has_omitted: bool,
        rule_issues: list[dict[str, Any]],
    ) -> str:
        if not rule_issues:
            return "OK"
        if has_omitted and len(implementation_refs) >= minimum_implementation_refs and not missing_cases:
            return "BLOCKED"
        if implementation_refs or has_omitted:
            return "PARTIAL"
        return "NG"

    def _build_rule_summary(
        self,
        *,
        rule: DomainRule,
        rule_status: str,
        implementation_refs: list[Annotation],
        expected_suffixes: list[str],
        missing_cases: list[dict[str, Any]],
        case_matrix: list[dict[str, Any]],
        missing_layers: list[str],
        rule_issues: list[dict[str, Any]],
    ) -> str:
        observed_count = sum(
            1 for case in case_matrix if case["status"] in {"PASS", "OMITTED"}
        )
        if rule_status == "OK":
            return (
                f"{rule.rule_id}: implementation linked and all {len(expected_suffixes)} "
                "required test perspectives are covered."
            )

        parts: list[str] = []
        if len(implementation_refs) < rule.minimum_implementation_refs:
            parts.append("implementation reference is missing")
        if missing_cases:
            missing_suffixes = ", ".join(item["suffix"] for item in missing_cases)
            parts.append(f"missing test cases: {missing_suffixes}")
        if missing_layers:
            parts.append(f"missing test layers: {', '.join(missing_layers)}")
        if not parts and rule_issues:
            parts.append("traceability issues detected")
        joined = "; ".join(parts)
        return (
            f"{rule.rule_id}: {observed_count}/{len(expected_suffixes)} required test "
            f"perspectives covered; {joined}."
        )

    def _expected_test_ids_by_rule(self) -> dict[str, list[str]]:
        expected: dict[str, list[str]] = {}
        for rule in self.domain_rules.values():
            suffixes: list[str] = []
            for pattern_id in rule.required_test_patterns:
                pattern = self.test_patterns[pattern_id]
                suffixes.extend(case.suffix for case in pattern.generated_cases)
            expected[rule.rule_id] = suffixes
        return expected

    def _matching_test_annotations(
        self,
        observed_test_ids: dict[str, list[Annotation]],
        rule_id: str,
        suffix: str,
    ) -> list[Annotation]:
        matches: list[Annotation] = []
        prefix = f"{rule_id}-{suffix}-"
        for test_id, annotations in observed_test_ids.items():
            if test_id.startswith(prefix):
                matches.extend(annotations)
        return matches

    def _matching_omitted_annotations(
        self,
        observed_omitted_ids: dict[str, list[Annotation]],
        rule_id: str,
        suffix: str,
    ) -> list[Annotation]:
        matches: list[Annotation] = []
        token = f"{rule_id}-{suffix}-OMITTED"
        for omitted_id, annotations in observed_omitted_ids.items():
            if omitted_id == token:
                matches.extend(annotations)
        return matches

    def _parse_test_id(self, value: str) -> dict[str, str] | None:
        parts = value.split("-")
        if len(parts) < 5:
            return None
        return {
            "rule_id": "-".join(parts[:3]),
            "suffix": "-".join(parts[3:-1]),
            "sequence": parts[-1],
        }

    def _parse_omitted_id(self, value: str) -> dict[str, str] | None:
        parts = value.split("-")
        if len(parts) < 5 or parts[-1] != "OMITTED":
            return None
        return {
            "rule_id": "-".join(parts[:3]),
            "suffix": "-".join(parts[3:-1]),
        }

    def _annotation_to_dict(self, annotation: Annotation) -> dict[str, Any]:
        return {
            "annotation_type": annotation.annotation_type,
            "value": annotation.value,
            "source_path": annotation.source_path,
            "line_number": annotation.line_number,
            "reason": annotation.reason,
            "test_layer": annotation.test_layer,
            "related_rule_ids": annotation.related_rule_ids,
        }

    def _attach_related_rules(
        self,
        annotation: Annotation,
        related_rules_by_location: dict[tuple[str, int], Annotation],
    ) -> Annotation:
        related = related_rules_by_location.get((annotation.source_path, annotation.line_number + 1))
        if not related:
            related = related_rules_by_location.get((annotation.source_path, annotation.line_number - 1))
        if not related:
            return annotation
        return Annotation(
            annotation_type=annotation.annotation_type,
            value=annotation.value,
            source_path=annotation.source_path,
            line_number=annotation.line_number,
            reason=annotation.reason,
            test_layer=annotation.test_layer,
            related_rule_ids=related.related_rule_ids,
        )

    def _validate_combination_metadata(
        self,
        *,
        rule: DomainRule,
        case_matrix: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        for pattern_id in rule.required_test_patterns:
            pattern = self.test_patterns[pattern_id]
            if not pattern.multi_rule_support.get("enabled"):
                continue
            combination_suffixes = {case.suffix for case in pattern.generated_cases}
            for case in case_matrix:
                if case["suffix"] not in combination_suffixes:
                    continue
                annotations = case["tests"] + case["omitted"]
                if not annotations:
                    continue
                for annotation in annotations:
                    related_rule_ids = annotation.get("related_rule_ids") or []
                    if len(related_rule_ids) < pattern.multi_rule_support["minimum_related_rules"]:
                        issues.append(
                            {
                                "code": "MISSING_TRACE_RULES_METADATA",
                                "rule_id": rule.rule_id,
                                "message": "Combination test requires TRACE-RULES metadata.",
                                "suffix": case["suffix"],
                                "annotation": annotation,
                            }
                        )
                        continue
                    if (
                        pattern.multi_rule_support.get("relation_must_include_primary_rule")
                        and rule.rule_id not in related_rule_ids
                    ):
                        issues.append(
                            {
                                "code": "INVALID_TRACE_RULES_METADATA",
                                "rule_id": rule.rule_id,
                                "message": "TRACE-RULES metadata must include the primary rule id.",
                                "suffix": case["suffix"],
                                "annotation": annotation,
                            }
                        )
                    for related_rule_id in rule.related_rule_ids:
                        if related_rule_id not in related_rule_ids:
                            issues.append(
                                {
                                    "code": "MISSING_RELATED_RULE_IN_TRACE_RULES",
                                    "rule_id": rule.rule_id,
                                    "message": "TRACE-RULES metadata is missing a required related rule.",
                                    "suffix": case["suffix"],
                                    "related_rule_id": related_rule_id,
                                    "annotation": annotation,
                                }
                            )
        return issues

    def _build_rule_layer_summary(self, case_matrix: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
        summary: dict[str, dict[str, int]] = {}
        for case in case_matrix:
            for test in case["tests"]:
                layer = test.get("test_layer") or "UNKNOWN"
                summary.setdefault(layer, {"tests": 0, "omitted": 0})
                summary[layer]["tests"] += 1
            for omitted in case["omitted"]:
                layer = omitted.get("test_layer") or "UNKNOWN"
                summary.setdefault(layer, {"tests": 0, "omitted": 0})
                summary[layer]["omitted"] += 1
        return dict(sorted(summary.items()))

    def _build_global_layer_summary(
        self,
        observed_test_annotation_lists: list[list[Annotation]],
        observed_omitted_annotation_lists: list[list[Annotation]],
        rule_results: list[dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        summary: dict[str, dict[str, Any]] = {}
        for layer in [item["layer_id"] for item in self.test_layers]:
            summary[layer] = {
                "tests": 0,
                "omitted": 0,
                "rules_touched": 0,
            }
        default_layer = self.test_rules_doc["test_layers"]["default_layer"]
        summary.setdefault(default_layer, {"tests": 0, "omitted": 0, "rules_touched": 0})

        rules_touched_by_layer: dict[str, set[str]] = {key: set() for key in summary}
        for annotations in observed_test_annotation_lists:
            for annotation in annotations:
                layer = annotation.test_layer or default_layer
                summary.setdefault(layer, {"tests": 0, "omitted": 0, "rules_touched": 0})
                summary[layer]["tests"] += 1
                parsed = self._parse_test_id(annotation.value)
                if parsed:
                    rules_touched_by_layer.setdefault(layer, set()).add(parsed["rule_id"])
        for annotations in observed_omitted_annotation_lists:
            for annotation in annotations:
                layer = annotation.test_layer or default_layer
                summary.setdefault(layer, {"tests": 0, "omitted": 0, "rules_touched": 0})
                summary[layer]["omitted"] += 1
                parsed = self._parse_omitted_id(annotation.value)
                if parsed:
                    rules_touched_by_layer.setdefault(layer, set()).add(parsed["rule_id"])
        for layer, touched in rules_touched_by_layer.items():
            summary.setdefault(layer, {"tests": 0, "omitted": 0, "rules_touched": 0})
            summary[layer]["rules_touched"] = len(touched)

        total_rules = len(rule_results)
        for layer, item in summary.items():
            item["rule_coverage"] = _ratio(item["rules_touched"], total_rules)

        return dict(sorted(summary.items()))


def _format_text_report(report: dict[str, Any]) -> str:
    lines = [
        f"status: {report['summary']['status']}",
        f"total_rules: {report['summary']['total_rules']}",
        f"passed_rules: {report['summary']['passed_rules']}",
        f"failed_rules: {report['summary']['failed_rules']}",
        f"total_issues: {report['summary']['total_issues']}",
    ]
    for layer, item in report["layer_summary"].items():
        lines.append(
            f"layer[{layer}]: tests={item['tests']} omitted={item['omitted']} "
            f"rules={item['rules_touched']} coverage={_to_percent(item['rule_coverage'])}%"
        )
    for rule in report["rules"]:
        lines.append(f"{rule['status']} {rule['rule_id']} {rule['name']}")
        lines.append(f"  summary: {rule['summary_text']}")
        lines.append(
            "  coverage: "
            f"impl={_to_percent(rule['coverage']['implementation_ref_coverage'])}% "
            f"test={_to_percent(rule['coverage']['test_case_coverage'])}% "
            f"layer={_to_percent(rule['coverage']['test_layer_coverage'])}% "
            f"traceability={_to_percent(rule['coverage']['traceability_coverage'])}%"
        )
        if rule["layer_summary"]:
            for layer, item in rule["layer_summary"].items():
                lines.append(
                    f"  layer[{layer}]: tests={item['tests']} omitted={item['omitted']}"
                )
        for issue in rule["issues"]:
            lines.append(f"  issue[{issue['code']}]: {issue['message']}")
    for issue in report["issues"]:
        if issue["code"] in {
            "UNMAPPED_IMPLEMENTATION_ID",
            "UNMAPPED_TEST_ID",
            "DUPLICATE_TEST_ID",
            "INVALID_IMPLEMENTATION_COMMENT_FORMAT",
            "INVALID_TEST_COMMENT_FORMAT",
            "INVALID_RELATED_RULES_COMMENT_FORMAT",
            "UNKNOWN_RELATED_RULE_ID",
            "MISSING_REVERSE_RULE_RELATION_CONFIG",
        }:
            lines.append(f"issue[{issue['code']}]: {issue['message']}")
    return "\n".join(lines)


def _format_markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Traceability Validation Report",
        "",
        f"- Generated At: `{report['generated_at']}`",
        f"- Status: `{summary['status']}`",
        f"- Total Rules: `{summary['total_rules']}`",
        f"- Passed Rules: `{summary['passed_rules']}`",
        f"- Failed Rules: `{summary['failed_rules']}`",
        f"- Total Issues: `{summary['total_issues']}`",
    ]

    if report["implementation_paths"]:
        joined = ", ".join(f"`{path}`" for path in report["implementation_paths"])
        lines.append(f"- Implementation Paths: {joined}")
    if report["test_paths"]:
        joined = ", ".join(f"`{path}`" for path in report["test_paths"])
        lines.append(f"- Test Paths: {joined}")

    lines.extend(["", "## Issue Counts", ""])
    if report["issue_counts"]:
        for code, count in report["issue_counts"].items():
            lines.append(f"- `{code}`: {count}")
    else:
        lines.append("- None")

    lines.extend(["", "## Test Layer Summary", ""])
    lines.append("| Layer | Tests | Omitted | Rules Touched | Rule Coverage |")
    lines.append("| --- | --- | --- | --- | --- |")
    for layer, item in report["layer_summary"].items():
        lines.append(
            f"| `{layer}` | `{item['tests']}` | `{item['omitted']}` | "
            f"`{item['rules_touched']}` | `{_to_percent(item['rule_coverage'])}%` |"
        )

    lines.extend(["", "## Traceability Summary", ""])
    lines.append("| Rule | Status | Implementation | Test Cases | Coverage | Summary |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for rule in report["rules"]:
        implementation_status = (
            f"{len(rule['implementation_refs'])}/{rule['minimum_implementation_refs']}"
        )
        observed = sum(
            1 for case in rule["case_matrix"] if case["status"] in {"PASS", "OMITTED"}
        )
        total = len(rule["case_matrix"])
        coverage = _to_percent(rule["coverage"]["traceability_coverage"])
        lines.append(
            f"| `{rule['rule_id']}` | `{rule['status']}` | `{implementation_status}` | "
            f"`{observed}/{total}` | `{coverage}%` | {rule['summary_text']} |"
        )

    lines.extend(["", "## Rules", ""])
    for rule in report["rules"]:
        lines.append(f"### `{rule['rule_id']}` {rule['name']}")
        lines.append("")
        lines.append(f"- Result: `{'OK' if rule['valid'] else 'NG'}`")
        lines.append(f"- Rule Status: `{rule['status']}`")
        lines.append(f"- Summary: {rule['summary_text']}")
        lines.append(f"- Implementation ID: `{rule['implementation_id']}`")
        lines.append(
            "- Coverage: "
            f"Implementation `{_to_percent(rule['coverage']['implementation_ref_coverage'])}%`, "
            f"Test Cases `{_to_percent(rule['coverage']['test_case_coverage'])}%`, "
            f"Test Layers `{_to_percent(rule['coverage']['test_layer_coverage'])}%`, "
            f"Traceability `{_to_percent(rule['coverage']['traceability_coverage'])}%`"
        )
        if rule["required_test_layers"]:
            lines.append(
                f"- Required Test Layers: {', '.join(f'`{layer}`' for layer in rule['required_test_layers'])}"
            )
        if rule["missing_test_layers"]:
            lines.append(
                f"- Missing Test Layers: {', '.join(f'`{layer}`' for layer in rule['missing_test_layers'])}"
            )
        if rule["layer_summary"]:
            lines.append("- Layer Summary:")
            for layer, item in rule["layer_summary"].items():
                lines.append(
                    f"  - `{layer}`: tests `{item['tests']}`, omitted `{item['omitted']}`"
                )
        if rule["implementation_refs"]:
            lines.append("- Implementation Refs:")
            for item in rule["implementation_refs"]:
                lines.append(f"  - `{item['value']}` at `{item['source_path']}:{item['line_number']}`")
        else:
            lines.append("- Implementation Refs: None")

        lines.append("- Expected Test Matrix:")
        lines.append("")
        lines.append("| Suffix | Status | Evidence |")
        lines.append("| --- | --- | --- |")
        for case in rule["case_matrix"]:
            evidence_parts: list[str] = []
            if case["tests"]:
                evidence_parts.append(
                    ", ".join(f"`{item['value']}`" for item in case["tests"])
                )
            if case["omitted"]:
                omitted_values = ", ".join(f"`{item['value']}`" for item in case["omitted"])
                evidence_parts.append(f"Omitted: {omitted_values}")
            evidence = "; ".join(evidence_parts) if evidence_parts else "Missing"
            lines.append(f"| `{case['suffix']}` | `{case['status']}` | {evidence} |")

        if rule["observed_cases"]:
            lines.append("- Observed Test Cases:")
            for case in rule["observed_cases"]:
                lines.append(f"  - Suffix `{case['suffix']}`")
                if case["tests"]:
                    for test in case["tests"]:
                        lines.append(
                            f"    - Test `{test['value']}` at `{test['source_path']}:{test['line_number']}`"
                        )
                if case["omitted"]:
                    for omitted in case["omitted"]:
                        lines.append(
                            f"    - Omitted `{omitted['value']}` at `{omitted['source_path']}:{omitted['line_number']}`"
                        )
                        if omitted["reason"]:
                            lines.append(f"      - Reason: {omitted['reason']}")
        else:
            lines.append("- Observed Test Cases: None")

        if rule["missing_cases"]:
            lines.append("- Missing Test Cases:")
            for item in rule["missing_cases"]:
                lines.append(f"  - `{item['suffix']}`")
        else:
            lines.append("- Missing Test Cases: None")

        if rule["issues"]:
            lines.append("- Rule Issues:")
            for issue in rule["issues"]:
                lines.append(f"  - `{issue['code']}`: {issue['message']}")
        else:
            lines.append("- Rule Issues: None")
        lines.append("")

    lines.extend(["## Global Issues", ""])
    global_issues = [
        issue
        for issue in report["issues"]
        if issue["code"]
        in {
            "UNMAPPED_IMPLEMENTATION_ID",
            "UNMAPPED_TEST_ID",
            "DUPLICATE_TEST_ID",
            "INVALID_IMPLEMENTATION_COMMENT_FORMAT",
            "INVALID_TEST_COMMENT_FORMAT",
            "INVALID_RELATED_RULES_COMMENT_FORMAT",
            "UNKNOWN_RELATED_RULE_ID",
            "MISSING_REVERSE_RULE_RELATION_CONFIG",
        }
    ]
    if global_issues:
        for issue in global_issues:
            lines.append(f"- `{issue['code']}`: {issue['message']}")
            if "annotation" in issue:
                item = issue["annotation"]
                lines.append(f"  - `{item['value']}` at `{item['source_path']}:{item['line_number']}`")
            if "test_id" in issue:
                lines.append(f"  - Test ID: `{issue['test_id']}`")
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def _write_report(path: Path, report_format: str, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if report_format == "json":
        content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    else:
        content = _format_markdown_report(report)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate static traceability between domain rules, implementation annotations, and test annotations."
    )
    parser.add_argument(
        "--implementation-path",
        action="append",
        default=[],
        help="Implementation file or directory to scan. Repeatable.",
    )
    parser.add_argument(
        "--test-path",
        action="append",
        default=[],
        help="Test file or directory to scan. Repeatable.",
    )
    parser.add_argument(
        "--domain-rules",
        default=str(DOMAIN_RULES_FILE),
        help="Path to 10_domain-rule.yaml",
    )
    parser.add_argument(
        "--test-rules",
        default=str(TEST_RULES_FILE),
        help="Path to 10_test-rules.yaml",
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
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.implementation_path and not args.test_path:
        parser.error("Provide at least one --implementation-path or --test-path.")

    validator = TraceabilityValidator(
        domain_rules_path=Path(args.domain_rules),
        test_rules_path=Path(args.test_rules),
    )
    report = validator.validate(
        implementation_paths=[Path(path) for path in args.implementation_path],
        test_paths=[Path(path) for path in args.test_path],
    )

    if args.report:
        _write_report(Path(args.report), args.report_format, report)

    if args.format == "text":
        print(_format_text_report(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    return 0 if report["summary"]["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
