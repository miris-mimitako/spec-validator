# Traceability Validation Report

- Generated At: `2026-04-08T15:09:28.685301+00:00`
- Status: `failure`
- Total Rules: `2`
- Passed Rules: `0`
- Failed Rules: `2`
- Total Issues: `21`
- Implementation Paths: `examples\traceability-fail\src`
- Test Paths: `examples\traceability-fail\test`

## Issue Counts

- `INSUFFICIENT_TEST_REFS`: 2
- `INVALID_TEST_COMMENT_FORMAT`: 1
- `MISSING_COMBINATION_DIRECTION`: 2
- `MISSING_IMPLEMENTATION_REF`: 1
- `MISSING_RELATED_RULE_IN_TRACE_RULES`: 1
- `MISSING_REQUIRED_TEST_LAYER`: 2
- `MISSING_REVERSE_COMBINATION_DIRECTION`: 2
- `MISSING_TEST_CASE`: 7
- `MISSING_TRACE_RULES_METADATA`: 1
- `UNMAPPED_IMPLEMENTATION_ID`: 1
- `UNMAPPED_TEST_ID`: 1

## Test Layer Summary

| Layer | Tests | Omitted | Rules Touched | Rule Coverage |
| --- | --- | --- | --- | --- |
| `E2E` | `0` | `0` | `0` | `0%` |
| `IT` | `4` | `0` | `2` | `100%` |
| `UNKNOWN` | `0` | `0` | `0` | `0%` |
| `UT` | `1` | `1` | `1` | `50%` |

## Traceability Summary

| Rule | Status | Implementation | Test Cases | Coverage | Summary |
| --- | --- | --- | --- | --- | --- |
| `domain-rule-001` | `PARTIAL` | `1/1` | `3/7` | `50%` | domain-rule-001: 3/7 required test perspectives covered; missing test cases: UPPER-OUT, COMBO-VALID, COMBO-INVALID, COMBO-PRIORITY; missing test layers: E2E. |
| `domain-rule-002` | `NG` | `0/1` | `3/6` | `43%` | domain-rule-002: 3/6 required test perspectives covered; implementation reference is missing; missing test cases: NULL-OUT, EMPTY-OUT, COMBO-PRIORITY; missing test layers: UT. |

## Rules

### `domain-rule-001` user-id-length

- Result: `NG`
- Rule Status: `PARTIAL`
- Summary: domain-rule-001: 3/7 required test perspectives covered; missing test cases: UPPER-OUT, COMBO-VALID, COMBO-INVALID, COMBO-PRIORITY; missing test layers: E2E.
- Implementation ID: `domain-rule-001-impl`
- Coverage: Implementation `100%`, Test Cases `43%`, Test Layers `67%`, Traceability `50%`
- Required Test Layers: `UT`, `IT`, `E2E`
- Missing Test Layers: `E2E`
- Layer Summary:
  - `IT`: tests `1`, omitted `0`
  - `UT`: tests `1`, omitted `1`
- Implementation Refs:
  - `domain-rule-001-impl` at `examples\traceability-fail\src\domain\user\user-id.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `LOWER-OUT` | `OMITTED` | Omitted: `domain-rule-001-LOWER-OUT-OMITTED` |
| `LOWER-IN` | `PASS` | `domain-rule-001-LOWER-IN-001` |
| `UPPER-IN` | `PASS` | `domain-rule-001-UPPER-IN-001` |
| `UPPER-OUT` | `MISSING` | Missing |
| `COMBO-VALID` | `MISSING` | Missing |
| `COMBO-INVALID` | `MISSING` | Missing |
| `COMBO-PRIORITY` | `MISSING` | Missing |
- Observed Test Cases:
  - Suffix `LOWER-OUT`
    - Omitted `domain-rule-001-LOWER-OUT-OMITTED` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:3`
      - Reason: upstream parser blocks values shorter than three characters
  - Suffix `LOWER-IN`
    - Test `domain-rule-001-LOWER-IN-001` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:7`
  - Suffix `UPPER-IN`
    - Test `domain-rule-001-UPPER-IN-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:3`
- Missing Test Cases:
  - `UPPER-OUT`
  - `COMBO-VALID`
  - `COMBO-INVALID`
  - `COMBO-PRIORITY`
- Rule Issues:
  - `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `MISSING_REQUIRED_TEST_LAYER`: Required test layer is missing.
  - `MISSING_COMBINATION_DIRECTION`: No combination annotation was found from this rule to the related rule.
  - `MISSING_REVERSE_COMBINATION_DIRECTION`: No reverse combination annotation was found from the related rule back to this rule.

### `domain-rule-002` user-id-required

- Result: `NG`
- Rule Status: `NG`
- Summary: domain-rule-002: 3/6 required test perspectives covered; implementation reference is missing; missing test cases: NULL-OUT, EMPTY-OUT, COMBO-PRIORITY; missing test layers: UT.
- Implementation ID: `domain-rule-002-impl`
- Coverage: Implementation `0%`, Test Cases `50%`, Test Layers `50%`, Traceability `43%`
- Required Test Layers: `UT`, `IT`
- Missing Test Layers: `UT`
- Layer Summary:
  - `IT`: tests `3`, omitted `0`
- Implementation Refs: None
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `NULL-OUT` | `MISSING` | Missing |
| `EMPTY-OUT` | `MISSING` | Missing |
| `VALID-IN` | `PASS` | `domain-rule-002-VALID-IN-001` |
| `COMBO-VALID` | `PASS` | `domain-rule-002-COMBO-VALID-001` |
| `COMBO-INVALID` | `PASS` | `domain-rule-002-COMBO-INVALID-001` |
| `COMBO-PRIORITY` | `MISSING` | Missing |
- Observed Test Cases:
  - Suffix `VALID-IN`
    - Test `domain-rule-002-VALID-IN-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:7`
  - Suffix `COMBO-VALID`
    - Test `domain-rule-002-COMBO-VALID-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:11`
  - Suffix `COMBO-INVALID`
    - Test `domain-rule-002-COMBO-INVALID-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:15`
- Missing Test Cases:
  - `NULL-OUT`
  - `EMPTY-OUT`
  - `COMBO-PRIORITY`
- Rule Issues:
  - `MISSING_IMPLEMENTATION_REF`: Implementation annotation is missing.
  - `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `MISSING_REQUIRED_TEST_LAYER`: Required test layer is missing.
  - `MISSING_TRACE_RULES_METADATA`: Combination test requires TRACE-RULES metadata.
  - `MISSING_RELATED_RULE_IN_TRACE_RULES`: TRACE-RULES metadata is missing a required related rule.
  - `MISSING_COMBINATION_DIRECTION`: No combination annotation was found from this rule to the related rule.
  - `MISSING_REVERSE_COMBINATION_DIRECTION`: No reverse combination annotation was found from the related rule back to this rule.

## Global Issues

- `UNMAPPED_IMPLEMENTATION_ID`: Implementation annotation does not map to a known rule.
  - `domain-rule-999-impl` at `examples\traceability-fail\src\domain\user\user-name.ts:2`
- `UNMAPPED_TEST_ID`: Test annotation does not map to a known expected test case.
  - `domain-rule-123-LOWER-IN-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:20`
- `INVALID_TEST_COMMENT_FORMAT`: Test annotation must use the configured TRACE comment format.
  - `domain-rule-002-NULL-OUT-001` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:11`
