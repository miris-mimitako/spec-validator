# Traceability Validation Report

- Generated At: `2026-04-08T15:09:18.276690+00:00`
- Status: `success`
- Total Rules: `2`
- Passed Rules: `2`
- Failed Rules: `0`
- Total Issues: `0`
- Implementation Paths: `examples\traceability-pass\src`
- Test Paths: `examples\traceability-pass\test`

## Issue Counts

- None

## Test Layer Summary

| Layer | Tests | Omitted | Rules Touched | Rule Coverage |
| --- | --- | --- | --- | --- |
| `E2E` | `1` | `0` | `1` | `50%` |
| `IT` | `8` | `0` | `2` | `100%` |
| `UNKNOWN` | `0` | `0` | `0` | `0%` |
| `UT` | `4` | `0` | `2` | `100%` |

## Traceability Summary

| Rule | Status | Implementation | Test Cases | Coverage | Summary |
| --- | --- | --- | --- | --- | --- |
| `domain-rule-001` | `OK` | `1/1` | `7/7` | `100%` | domain-rule-001: implementation linked and all 7 required test perspectives are covered. |
| `domain-rule-002` | `OK` | `1/1` | `6/6` | `100%` | domain-rule-002: implementation linked and all 6 required test perspectives are covered. |

## Rules

### `domain-rule-001` user-id-length

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-001: implementation linked and all 7 required test perspectives are covered.
- Implementation ID: `domain-rule-001-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Test Layers `100%`, Traceability `100%`
- Required Test Layers: `UT`, `IT`, `E2E`
- Layer Summary:
  - `E2E`: tests `1`, omitted `0`
  - `IT`: tests `4`, omitted `0`
  - `UT`: tests `2`, omitted `0`
- Implementation Refs:
  - `domain-rule-001-impl` at `examples\traceability-pass\src\domain\user\user-id.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `LOWER-OUT` | `PASS` | `domain-rule-001-LOWER-OUT-001` |
| `LOWER-IN` | `PASS` | `domain-rule-001-LOWER-IN-001` |
| `UPPER-IN` | `PASS` | `domain-rule-001-UPPER-IN-001` |
| `UPPER-OUT` | `PASS` | `domain-rule-001-UPPER-OUT-001` |
| `COMBO-VALID` | `PASS` | `domain-rule-001-COMBO-VALID-001` |
| `COMBO-INVALID` | `PASS` | `domain-rule-001-COMBO-INVALID-001` |
| `COMBO-PRIORITY` | `PASS` | `domain-rule-001-COMBO-PRIORITY-001` |
- Observed Test Cases:
  - Suffix `LOWER-OUT`
    - Test `domain-rule-001-LOWER-OUT-001` at `examples\traceability-pass\test\ut\user-id.unit.spec.ts:3`
  - Suffix `LOWER-IN`
    - Test `domain-rule-001-LOWER-IN-001` at `examples\traceability-pass\test\ut\user-id.unit.spec.ts:7`
  - Suffix `UPPER-IN`
    - Test `domain-rule-001-UPPER-IN-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:3`
  - Suffix `UPPER-OUT`
    - Test `domain-rule-001-UPPER-OUT-001` at `examples\traceability-pass\test\e2e\user-id.e2e-spec.ts:3`
  - Suffix `COMBO-VALID`
    - Test `domain-rule-001-COMBO-VALID-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:7`
  - Suffix `COMBO-INVALID`
    - Test `domain-rule-001-COMBO-INVALID-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:12`
  - Suffix `COMBO-PRIORITY`
    - Test `domain-rule-001-COMBO-PRIORITY-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:17`
- Missing Test Cases: None
- Rule Issues: None

### `domain-rule-002` user-id-required

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-002: implementation linked and all 6 required test perspectives are covered.
- Implementation ID: `domain-rule-002-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Test Layers `100%`, Traceability `100%`
- Required Test Layers: `UT`, `IT`
- Layer Summary:
  - `IT`: tests `4`, omitted `0`
  - `UT`: tests `2`, omitted `0`
- Implementation Refs:
  - `domain-rule-002-impl` at `examples\traceability-pass\src\domain\user\user-id.ts:3`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `NULL-OUT` | `PASS` | `domain-rule-002-NULL-OUT-001` |
| `EMPTY-OUT` | `PASS` | `domain-rule-002-EMPTY-OUT-001` |
| `VALID-IN` | `PASS` | `domain-rule-002-VALID-IN-001` |
| `COMBO-VALID` | `PASS` | `domain-rule-002-COMBO-VALID-001` |
| `COMBO-INVALID` | `PASS` | `domain-rule-002-COMBO-INVALID-001` |
| `COMBO-PRIORITY` | `PASS` | `domain-rule-002-COMBO-PRIORITY-001` |
- Observed Test Cases:
  - Suffix `NULL-OUT`
    - Test `domain-rule-002-NULL-OUT-001` at `examples\traceability-pass\test\ut\user-id.unit.spec.ts:11`
  - Suffix `EMPTY-OUT`
    - Test `domain-rule-002-EMPTY-OUT-001` at `examples\traceability-pass\test\ut\user-id.unit.spec.ts:15`
  - Suffix `VALID-IN`
    - Test `domain-rule-002-VALID-IN-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:22`
  - Suffix `COMBO-VALID`
    - Test `domain-rule-002-COMBO-VALID-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:26`
  - Suffix `COMBO-INVALID`
    - Test `domain-rule-002-COMBO-INVALID-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:31`
  - Suffix `COMBO-PRIORITY`
    - Test `domain-rule-002-COMBO-PRIORITY-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:36`
- Missing Test Cases: None
- Rule Issues: None

## Global Issues

- None
