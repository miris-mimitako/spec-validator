# Traceability Validation Report

- Generated At: `2026-04-08T15:29:35.200744+00:00`
- Status: `failure`
- Total Rules: `5`
- Passed Rules: `0`
- Failed Rules: `5`
- Total Issues: `28`
- Omitted Accepted Cases: `1`
- Implementation Paths: `examples\traceability-fail\src`
- Test Paths: `examples\traceability-fail\test`

## Issue Counts

| Severity | Count |
| --- | --- |
| `ERROR` | `19` |
| `WARNING` | `9` |
| `INFO` | `0` |

### By Code

- `WARNING` `INSUFFICIENT_TEST_REFS`: 5
- `WARNING` `INVALID_TEST_COMMENT_FORMAT`: 2
- `ERROR` `MISSING_COMBINATION_DIRECTION`: 2
- `ERROR` `MISSING_IMPLEMENTATION_REF`: 2
- `WARNING` `MISSING_RELATED_RULE_IN_TRACE_RULES`: 1
- `ERROR` `MISSING_REQUIRED_TEST_LAYER`: 2
- `ERROR` `MISSING_REVERSE_COMBINATION_DIRECTION`: 2
- `ERROR` `MISSING_TEST_CASE`: 9
- `WARNING` `MISSING_TRACE_RULES_METADATA`: 1
- `ERROR` `UNMAPPED_IMPLEMENTATION_ID`: 1
- `ERROR` `UNMAPPED_TEST_ID`: 1

## Test Layer Summary

| Layer | Tests | Omitted | Rules Touched | Rule Coverage |
| --- | --- | --- | --- | --- |
| `E2E` | `0` | `0` | `0` | `0%` |
| `IT` | `6` | `0` | `4` | `80%` |
| `UNKNOWN` | `0` | `0` | `0` | `0%` |
| `UT` | `4` | `1` | `4` | `80%` |

## Traceability Summary

| Rule | Status | Implementation | Test Cases | Coverage | Summary |
| --- | --- | --- | --- | --- | --- |
| `domain-rule-001` | `PARTIAL` | `1/1` | `3/7` | `38%` | domain-rule-001: 3/7 required test perspectives covered; missing test cases: UPPER-OUT, COMBO-VALID, COMBO-INVALID, COMBO-PRIORITY; missing test layers: E2E. |
| `domain-rule-002` | `NG` | `0/1` | `3/6` | `43%` | domain-rule-002: 3/6 required test perspectives covered; implementation reference is missing; missing test cases: EMPTY-OUT, COMBO-PRIORITY; invalid test annotations: NULL-OUT; missing test layers: UT. |
| `domain-rule-003` | `PARTIAL` | `1/1` | `2/3` | `75%` | domain-rule-003: 2/3 required test perspectives covered; invalid test annotations: FORMAT-INVALID. |
| `domain-rule-004` | `NG` | `0/1` | `2/3` | `50%` | domain-rule-004: 2/3 required test perspectives covered; implementation reference is missing; missing test cases: LOWER-IN. |
| `domain-rule-005` | `PARTIAL` | `1/1` | `1/3` | `50%` | domain-rule-005: 1/3 required test perspectives covered; missing test cases: UPPER-IN, UPPER-OUT. |

## Rules

### `domain-rule-001` user-id-length

- Result: `NG`
- Rule Status: `PARTIAL`
- Summary: domain-rule-001: 3/7 required test perspectives covered; missing test cases: UPPER-OUT, COMBO-VALID, COMBO-INVALID, COMBO-PRIORITY; missing test layers: E2E.
- Implementation ID: `domain-rule-001-impl`
- Coverage: Implementation `100%`, Test Cases `43%`, Test Layers `67%`, Traceability `38%`
- Case Counts: PASS `2`, OMITTED-ACCEPTED `1`, INVALID `0`, MISSING `4`
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
| `LOWER-OUT` | `OMITTED-ACCEPTED` | Omitted: `domain-rule-001-LOWER-OUT-OMITTED` |
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
- Invalid Test Cases: None
- Rule Issues:
  - `WARNING` `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `ERROR` `MISSING_REQUIRED_TEST_LAYER`: Required test layer is missing.
  - `ERROR` `MISSING_COMBINATION_DIRECTION`: No combination annotation was found from this rule to the related rule.
  - `ERROR` `MISSING_REVERSE_COMBINATION_DIRECTION`: No reverse combination annotation was found from the related rule back to this rule.

### `domain-rule-002` user-id-required

- Result: `NG`
- Rule Status: `NG`
- Summary: domain-rule-002: 3/6 required test perspectives covered; implementation reference is missing; missing test cases: EMPTY-OUT, COMBO-PRIORITY; invalid test annotations: NULL-OUT; missing test layers: UT.
- Implementation ID: `domain-rule-002-impl`
- Coverage: Implementation `0%`, Test Cases `67%`, Test Layers `50%`, Traceability `43%`
- Case Counts: PASS `3`, OMITTED-ACCEPTED `0`, INVALID `1`, MISSING `2`
- Required Test Layers: `UT`, `IT`
- Missing Test Layers: `UT`
- Layer Summary:
  - `IT`: tests `3`, omitted `0`
- Implementation Refs: None
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `NULL-OUT` | `INVALID` | Invalid: `domain-rule-002-NULL-OUT-001` |
| `EMPTY-OUT` | `MISSING` | Missing |
| `VALID-IN` | `PASS` | `domain-rule-002-VALID-IN-001` |
| `COMBO-VALID` | `PASS` | `domain-rule-002-COMBO-VALID-001` |
| `COMBO-INVALID` | `PASS` | `domain-rule-002-COMBO-INVALID-001` |
| `COMBO-PRIORITY` | `MISSING` | Missing |
- Observed Test Cases:
  - Suffix `NULL-OUT`
    - Invalid `domain-rule-002-NULL-OUT-001` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:11`
  - Suffix `VALID-IN`
    - Test `domain-rule-002-VALID-IN-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:7`
  - Suffix `COMBO-VALID`
    - Test `domain-rule-002-COMBO-VALID-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:11`
  - Suffix `COMBO-INVALID`
    - Test `domain-rule-002-COMBO-INVALID-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:15`
- Missing Test Cases:
  - `EMPTY-OUT`
  - `COMBO-PRIORITY`
- Invalid Test Cases:
  - `NULL-OUT`
- Rule Issues:
  - `ERROR` `MISSING_IMPLEMENTATION_REF`: Implementation annotation is missing.
  - `WARNING` `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `ERROR` `MISSING_REQUIRED_TEST_LAYER`: Required test layer is missing.
  - `WARNING` `MISSING_TRACE_RULES_METADATA`: Combination test requires TRACE-RULES metadata.
  - `WARNING` `MISSING_RELATED_RULE_IN_TRACE_RULES`: TRACE-RULES metadata is missing a required related rule.
  - `ERROR` `MISSING_COMBINATION_DIRECTION`: No combination annotation was found from this rule to the related rule.
  - `ERROR` `MISSING_REVERSE_COMBINATION_DIRECTION`: No reverse combination annotation was found from the related rule back to this rule.

### `domain-rule-003` user-id-format

- Result: `NG`
- Rule Status: `PARTIAL`
- Summary: domain-rule-003: 2/3 required test perspectives covered; invalid test annotations: FORMAT-INVALID.
- Implementation ID: `domain-rule-003-impl`
- Coverage: Implementation `100%`, Test Cases `100%`, Test Layers `100%`, Traceability `75%`
- Case Counts: PASS `2`, OMITTED-ACCEPTED `0`, INVALID `1`, MISSING `0`
- Required Test Layers: `UT`, `IT`
- Layer Summary:
  - `IT`: tests `1`, omitted `0`
  - `UT`: tests `1`, omitted `0`
- Implementation Refs:
  - `domain-rule-003-impl` at `examples\traceability-fail\src\domain\user\user-id-format.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `FORMAT-VALID` | `PASS` | `domain-rule-003-FORMAT-VALID-001` |
| `FORMAT-INVALID` | `INVALID` | Invalid: `domain-rule-003-FORMAT-INVALID-001` |
| `FORMAT-EDGE` | `PASS` | `domain-rule-003-FORMAT-EDGE-001` |
- Observed Test Cases:
  - Suffix `FORMAT-VALID`
    - Test `domain-rule-003-FORMAT-VALID-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:3`
  - Suffix `FORMAT-INVALID`
    - Invalid `domain-rule-003-FORMAT-INVALID-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:7`
  - Suffix `FORMAT-EDGE`
    - Test `domain-rule-003-FORMAT-EDGE-001` at `examples\traceability-fail\test\it\user-format.integration.spec.ts:3`
- Missing Test Cases: None
- Invalid Test Cases:
  - `FORMAT-INVALID`
- Rule Issues:
  - `WARNING` `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.

### `domain-rule-004` user-display-name-min-length

- Result: `NG`
- Rule Status: `NG`
- Summary: domain-rule-004: 2/3 required test perspectives covered; implementation reference is missing; missing test cases: LOWER-IN.
- Implementation ID: `domain-rule-004-impl`
- Coverage: Implementation `0%`, Test Cases `67%`, Test Layers `100%`, Traceability `50%`
- Case Counts: PASS `2`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `1`
- Required Test Layers: `UT`
- Layer Summary:
  - `IT`: tests `1`, omitted `0`
  - `UT`: tests `1`, omitted `0`
- Implementation Refs: None
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `LOWER-OUT` | `PASS` | `domain-rule-004-LOWER-OUT-001` |
| `LOWER-IN` | `MISSING` | Missing |
| `VALID-IN` | `PASS` | `domain-rule-004-VALID-IN-999` |
- Observed Test Cases:
  - Suffix `LOWER-OUT`
    - Test `domain-rule-004-LOWER-OUT-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:11`
  - Suffix `VALID-IN`
    - Test `domain-rule-004-VALID-IN-999` at `examples\traceability-fail\test\it\user-format.integration.spec.ts:7`
- Missing Test Cases:
  - `LOWER-IN`
- Invalid Test Cases: None
- Rule Issues:
  - `ERROR` `MISSING_IMPLEMENTATION_REF`: Implementation annotation is missing.
  - `WARNING` `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.

### `domain-rule-005` user-bio-max-length

- Result: `NG`
- Rule Status: `PARTIAL`
- Summary: domain-rule-005: 1/3 required test perspectives covered; missing test cases: UPPER-IN, UPPER-OUT.
- Implementation ID: `domain-rule-005-impl`
- Coverage: Implementation `100%`, Test Cases `33%`, Test Layers `100%`, Traceability `50%`
- Case Counts: PASS `1`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `2`
- Required Test Layers: `UT`
- Layer Summary:
  - `UT`: tests `1`, omitted `0`
- Implementation Refs:
  - `domain-rule-005-impl` at `examples\traceability-fail\src\domain\user\bio.ts:2`
- Expected Test Matrix:

| Suffix | Status | Evidence |
| --- | --- | --- |
| `VALID-IN` | `PASS` | `domain-rule-005-VALID-IN-001` |
| `UPPER-IN` | `MISSING` | Missing |
| `UPPER-OUT` | `MISSING` | Missing |
- Observed Test Cases:
  - Suffix `VALID-IN`
    - Test `domain-rule-005-VALID-IN-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:15`
- Missing Test Cases:
  - `UPPER-IN`
  - `UPPER-OUT`
- Invalid Test Cases: None
- Rule Issues:
  - `WARNING` `INSUFFICIENT_TEST_REFS`: Required number of test references was not met.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.
  - `ERROR` `MISSING_TEST_CASE`: Required test case suffix is missing.

## Global Issues

### ERROR

- `UNMAPPED_IMPLEMENTATION_ID`: Implementation annotation does not map to a known rule.
  - `domain-rule-999-impl` at `examples\traceability-fail\src\domain\user\user-name.ts:2`
- `UNMAPPED_TEST_ID`: Test annotation does not map to a known expected test case.
  - `domain-rule-123-LOWER-IN-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:20`

### WARNING

- `INVALID_TEST_COMMENT_FORMAT`: Test annotation must use the configured TRACE comment format.
  - `domain-rule-003-FORMAT-INVALID-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:7`
- `INVALID_TEST_COMMENT_FORMAT`: Test annotation must use the configured TRACE comment format.
  - `domain-rule-002-NULL-OUT-001` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:11`

### INFO

- None

