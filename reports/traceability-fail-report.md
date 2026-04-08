# Traceability Validation Report

- Generated At: `2026-04-08T14:54:26.405179+00:00`
- Status: `failure`
- Total Rules: `2`
- Passed Rules: `0`
- Failed Rules: `2`
- Total Issues: `8`
- Implementation Paths: `examples\traceability-fail\src`
- Test Paths: `examples\traceability-fail\test`

## Issue Counts

- `INSUFFICIENT_TEST_REFS`: 2
- `MISSING_IMPLEMENTATION_REF`: 1
- `MISSING_TEST_CASE`: 3
- `UNMAPPED_IMPLEMENTATION_ID`: 1
- `UNMAPPED_TEST_ID`: 1

## Traceability Summary

| Rule | Status | Implementation | Test Cases | Coverage | Summary |
| --- | --- | --- | --- | --- | --- |
| `domain-rule-001` | `PARTIAL` | `1/1` | `3/4` | `80%` | domain-rule-001: 3/4 required test perspectives covered; missing test cases: UPPER-OUT. |
| `domain-rule-002` | `NG` | `0/1` | `1/3` | `25%` | domain-rule-002: 1/3 required test perspectives covered; implementation reference is missing; missing test cases: NULL-OUT, EMPTY-OUT. |

## Rules

### `domain-rule-001` user-id-length

- Result: `NG`
- Rule Status: `PARTIAL`
- Summary: domain-rule-001: 3/4 required test perspectives covered; missing test cases: UPPER-OUT.
- Implementation ID: `domain-rule-001-impl`
- Coverage: Implementation `100%`, Test Cases `75%`, Traceability `80%`
- Implementation Refs:
  - `domain-rule-001-impl` at `examples\traceability-fail\src\domain\user\user-id.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `LOWER-OUT` | `OMITTED` | Omitted: `domain-rule-001-LOWER-OUT-OMITTED` |
| `LOWER-IN` | `PASS` | `domain-rule-001-LOWER-IN-001` |
| `UPPER-IN` | `PASS` | `domain-rule-001-UPPER-IN-001` |
| `UPPER-OUT` | `MISSING` | Missing |
- Observed Test Cases:
  - Suffix `LOWER-OUT`
    - Omitted `domain-rule-001-LOWER-OUT-OMITTED` at `examples\traceability-fail\test\user-id.spec.ts:3`
      - Reason: upstream parser blocks values shorter than three characters
  - Suffix `LOWER-IN`
    - Test `domain-rule-001-LOWER-IN-001` at `examples\traceability-fail\test\user-id.spec.ts:7`
  - Suffix `UPPER-IN`
    - Test `domain-rule-001-UPPER-IN-001` at `examples\traceability-fail\test\user-id.spec.ts:11`
- Missing Test Cases:
  - `UPPER-OUT`
- Rule Issues:
  - `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.

### `domain-rule-002` user-id-required

- Result: `NG`
- Rule Status: `NG`
- Summary: domain-rule-002: 1/3 required test perspectives covered; implementation reference is missing; missing test cases: NULL-OUT, EMPTY-OUT.
- Implementation ID: `domain-rule-002-impl`
- Coverage: Implementation `0%`, Test Cases `33%`, Traceability `25%`
- Implementation Refs: None
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `NULL-OUT` | `MISSING` | Missing |
| `EMPTY-OUT` | `MISSING` | Missing |
| `VALID-IN` | `PASS` | `domain-rule-002-VALID-IN-001` |
- Observed Test Cases:
  - Suffix `VALID-IN`
    - Test `domain-rule-002-VALID-IN-001` at `examples\traceability-fail\test\user-id.spec.ts:15`
- Missing Test Cases:
  - `NULL-OUT`
  - `EMPTY-OUT`
- Rule Issues:
  - `MISSING_IMPLEMENTATION_REF`: Implementation annotation is missing.
  - `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `MISSING_TEST_CASE`: Required test case suffix is missing.

## Global Issues

- `UNMAPPED_IMPLEMENTATION_ID`: Implementation annotation does not map to a known rule.
  - `domain-rule-999-impl` at `examples\traceability-fail\src\domain\user\user-name.ts:2`
- `UNMAPPED_TEST_ID`: Test annotation does not map to a known expected test case.
  - `domain-rule-123-LOWER-IN-001` at `examples\traceability-fail\test\user-id.spec.ts:19`
