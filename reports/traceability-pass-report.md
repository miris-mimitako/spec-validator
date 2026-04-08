# Traceability Validation Report

- Generated At: `2026-04-08T15:29:35.201743+00:00`
- Status: `success`
- Total Rules: `5`
- Passed Rules: `5`
- Failed Rules: `0`
- Total Issues: `0`
- Omitted Accepted Cases: `0`
- Implementation Paths: `examples\traceability-pass\src`
- Test Paths: `examples\traceability-pass\test`

## Issue Counts

| Severity | Count |
| --- | --- |
| `ERROR` | `0` |
| `WARNING` | `0` |
| `INFO` | `0` |

### By Code

- None

## Test Layer Summary

| Layer | Tests | Omitted | Rules Touched | Rule Coverage |
| --- | --- | --- | --- | --- |
| `E2E` | `1` | `0` | `1` | `20%` |
| `IT` | `9` | `0` | `3` | `60%` |
| `UNKNOWN` | `0` | `0` | `0` | `0%` |
| `UT` | `12` | `0` | `5` | `100%` |

## Traceability Summary

| Rule | Status | Implementation | Test Cases | Coverage | Summary |
| --- | --- | --- | --- | --- | --- |
| `domain-rule-001` | `OK` | `1/1` | `7/7` | `100%` | domain-rule-001: implementation linked and all 7 required test perspectives are covered. |
| `domain-rule-002` | `OK` | `1/1` | `6/6` | `100%` | domain-rule-002: implementation linked and all 6 required test perspectives are covered. |
| `domain-rule-003` | `OK` | `1/1` | `3/3` | `100%` | domain-rule-003: implementation linked and all 3 required test perspectives are covered. |
| `domain-rule-004` | `OK` | `1/1` | `3/3` | `100%` | domain-rule-004: implementation linked and all 3 required test perspectives are covered. |
| `domain-rule-005` | `OK` | `1/1` | `3/3` | `100%` | domain-rule-005: implementation linked and all 3 required test perspectives are covered. |

## Rules

### `domain-rule-001` user-id-length

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-001: implementation linked and all 7 required test perspectives are covered.
- Implementation ID: `domain-rule-001-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Test Layers `100%`, Traceability `100%`
- Case Counts: PASS `7`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
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
- Invalid Test Cases: None
- Rule Issues: None

### `domain-rule-002` user-id-required

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-002: implementation linked and all 6 required test perspectives are covered.
- Implementation ID: `domain-rule-002-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Test Layers `100%`, Traceability `100%`
- Case Counts: PASS `6`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
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
- Invalid Test Cases: None
- Rule Issues: None

### `domain-rule-003` user-id-format

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-003: implementation linked and all 3 required test perspectives are covered.
- Implementation ID: `domain-rule-003-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Test Layers `100%`, Traceability `100%`
- Case Counts: PASS `3`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
- Required Test Layers: `UT`, `IT`
- Layer Summary:
  - `IT`: tests `1`, omitted `0`
  - `UT`: tests `2`, omitted `0`
- Implementation Refs:
  - `domain-rule-003-impl` at `examples\traceability-pass\src\domain\user\user-id-format.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `FORMAT-VALID` | `PASS` | `domain-rule-003-FORMAT-VALID-001` |
| `FORMAT-INVALID` | `PASS` | `domain-rule-003-FORMAT-INVALID-001` |
| `FORMAT-EDGE` | `PASS` | `domain-rule-003-FORMAT-EDGE-001` |
- Observed Test Cases:
  - Suffix `FORMAT-VALID`
    - Test `domain-rule-003-FORMAT-VALID-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:3`
  - Suffix `FORMAT-INVALID`
    - Test `domain-rule-003-FORMAT-INVALID-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:7`
  - Suffix `FORMAT-EDGE`
    - Test `domain-rule-003-FORMAT-EDGE-001` at `examples\traceability-pass\test\it\user-format.integration.spec.ts:3`
- Missing Test Cases: None
- Invalid Test Cases: None
- Rule Issues: None

### `domain-rule-004` user-display-name-min-length

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-004: implementation linked and all 3 required test perspectives are covered.
- Implementation ID: `domain-rule-004-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Test Layers `100%`, Traceability `100%`
- Case Counts: PASS `3`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
- Required Test Layers: `UT`
- Layer Summary:
  - `UT`: tests `3`, omitted `0`
- Implementation Refs:
  - `domain-rule-004-impl` at `examples\traceability-pass\src\domain\user\display-name.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `LOWER-OUT` | `PASS` | `domain-rule-004-LOWER-OUT-001` |
| `LOWER-IN` | `PASS` | `domain-rule-004-LOWER-IN-001` |
| `VALID-IN` | `PASS` | `domain-rule-004-VALID-IN-001` |
- Observed Test Cases:
  - Suffix `LOWER-OUT`
    - Test `domain-rule-004-LOWER-OUT-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:11`
  - Suffix `LOWER-IN`
    - Test `domain-rule-004-LOWER-IN-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:15`
  - Suffix `VALID-IN`
    - Test `domain-rule-004-VALID-IN-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:19`
- Missing Test Cases: None
- Invalid Test Cases: None
- Rule Issues: None

### `domain-rule-005` user-bio-max-length

- Result: `OK`
- Rule Status: `OK`
- Summary: domain-rule-005: implementation linked and all 3 required test perspectives are covered.
- Implementation ID: `domain-rule-005-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Test Layers `100%`, Traceability `100%`
- Case Counts: PASS `3`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
- Required Test Layers: `UT`
- Layer Summary:
  - `UT`: tests `3`, omitted `0`
- Implementation Refs:
  - `domain-rule-005-impl` at `examples\traceability-pass\src\domain\user\bio.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `VALID-IN` | `PASS` | `domain-rule-005-VALID-IN-001` |
| `UPPER-IN` | `PASS` | `domain-rule-005-UPPER-IN-001` |
| `UPPER-OUT` | `PASS` | `domain-rule-005-UPPER-OUT-001` |
- Observed Test Cases:
  - Suffix `VALID-IN`
    - Test `domain-rule-005-VALID-IN-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:23`
  - Suffix `UPPER-IN`
    - Test `domain-rule-005-UPPER-IN-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:27`
  - Suffix `UPPER-OUT`
    - Test `domain-rule-005-UPPER-OUT-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:31`
- Missing Test Cases: None
- Invalid Test Cases: None
- Rule Issues: None

## Global Issues

### ERROR

- None

### WARNING

- None

### INFO

- None

