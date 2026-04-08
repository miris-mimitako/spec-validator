# Traceability Validation Report

- Generated At: `2026-04-08T14:54:32.832204+00:00`
- Status: `success`
- Total Rules: `2`
- Passed Rules: `2`
- Failed Rules: `0`
- Total Issues: `0`
- Implementation Paths: `examples\traceability-pass\src`
- Test Paths: `examples\traceability-pass\test`

## Issue Counts

- None

## Traceability Summary

| Rule | Status | Implementation | Test Cases | Coverage | Summary |
| --- | --- | --- | --- | --- | --- |
| `domain-rule-001` | `OK` | `1/1` | `4/4` | `100%` | domain-rule-001: implementation linked and all 4 required test perspectives are covered. |
| `domain-rule-002` | `OK` | `1/1` | `3/3` | `100%` | domain-rule-002: implementation linked and all 3 required test perspectives are covered. |

## Rules

### `domain-rule-001` user-id-length

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-001: implementation linked and all 4 required test perspectives are covered.
- Implementation ID: `domain-rule-001-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Traceability `100%`
- Implementation Refs:
  - `domain-rule-001-impl` at `examples\traceability-pass\src\domain\user\user-id.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `LOWER-OUT` | `PASS` | `domain-rule-001-LOWER-OUT-001` |
| `LOWER-IN` | `PASS` | `domain-rule-001-LOWER-IN-001` |
| `UPPER-IN` | `PASS` | `domain-rule-001-UPPER-IN-001` |
| `UPPER-OUT` | `PASS` | `domain-rule-001-UPPER-OUT-001` |
- Observed Test Cases:
  - Suffix `LOWER-OUT`
    - Test `domain-rule-001-LOWER-OUT-001` at `examples\traceability-pass\test\user-id.spec.ts:3`
  - Suffix `LOWER-IN`
    - Test `domain-rule-001-LOWER-IN-001` at `examples\traceability-pass\test\user-id.spec.ts:7`
  - Suffix `UPPER-IN`
    - Test `domain-rule-001-UPPER-IN-001` at `examples\traceability-pass\test\user-id.spec.ts:11`
  - Suffix `UPPER-OUT`
    - Test `domain-rule-001-UPPER-OUT-001` at `examples\traceability-pass\test\user-id.spec.ts:15`
- Missing Test Cases: None
- Rule Issues: None

### `domain-rule-002` user-id-required

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-002: implementation linked and all 3 required test perspectives are covered.
- Implementation ID: `domain-rule-002-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Traceability `100%`
- Implementation Refs:
  - `domain-rule-002-impl` at `examples\traceability-pass\src\domain\user\user-id.ts:3`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `NULL-OUT` | `PASS` | `domain-rule-002-NULL-OUT-001` |
| `EMPTY-OUT` | `PASS` | `domain-rule-002-EMPTY-OUT-001` |
| `VALID-IN` | `PASS` | `domain-rule-002-VALID-IN-001` |
- Observed Test Cases:
  - Suffix `NULL-OUT`
    - Test `domain-rule-002-NULL-OUT-001` at `examples\traceability-pass\test\user-id.spec.ts:19`
  - Suffix `EMPTY-OUT`
    - Test `domain-rule-002-EMPTY-OUT-001` at `examples\traceability-pass\test\user-id.spec.ts:23`
  - Suffix `VALID-IN`
    - Test `domain-rule-002-VALID-IN-001` at `examples\traceability-pass\test\user-id.spec.ts:27`
- Missing Test Cases: None
- Rule Issues: None

## Global Issues

- None
