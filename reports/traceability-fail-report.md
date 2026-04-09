# トレーサビリティ検証レポート

- 生成日時: `2026-04-09T12:23:45.290488+00:00`
- ステータス: `失敗`
- 総ルール数: `5`
- 成功ルール数: `0`
- 失敗ルール数: `5`
- 総 Issue 数: `28`
- 受理済み OMITTED 数: `1`
- 実装対象パス: `examples\traceability-fail\src`
- テスト対象パス: `examples\traceability-fail\test`

## Issue 集計

| 重要度 | 件数 |
| --- | --- |
| `ERROR` | `19` |
| `WARNING` | `9` |
| `INFO` | `0` |

### コード別

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

## テストレイヤ集計

| レイヤ | テスト数 | OMITTED 数 | 到達ルール数 | ルール到達率 |
| --- | --- | --- | --- | --- |
| `E2E` | `0` | `0` | `0` | `0%` |
| `IT` | `6` | `0` | `4` | `80%` |
| `UNKNOWN` | `0` | `0` | `0` | `0%` |
| `UT` | `4` | `1` | `4` | `80%` |

## トレーサビリティ要約

| ルール | 状態 | 実装 | テスト観点 | カバレッジ | 要約 |
| --- | --- | --- | --- | --- | --- |
| `domain-rule-001` | `PARTIAL` | `1/1` | `3/7` | `38%` | domain-rule-001: 必須テスト観点 7 件中 3 件を確認。 不足観点: UPPER-OUT, COMBO-VALID, COMBO-INVALID, COMBO-PRIORITY。 不足レイヤ: E2E。 |
| `domain-rule-002` | `NG` | `0/1` | `3/6` | `43%` | domain-rule-002: 必須テスト観点 6 件中 3 件を確認。 実装注釈が不足しています。 不足観点: EMPTY-OUT, COMBO-PRIORITY。 不正注釈観点: NULL-OUT。 不足レイヤ: UT。 |
| `domain-rule-003` | `PARTIAL` | `1/1` | `2/3` | `75%` | domain-rule-003: 必須テスト観点 3 件中 2 件を確認。 不正注釈観点: FORMAT-INVALID。 |
| `domain-rule-004` | `NG` | `0/1` | `2/3` | `50%` | domain-rule-004: 必須テスト観点 3 件中 2 件を確認。 実装注釈が不足しています。 不足観点: LOWER-IN。 |
| `domain-rule-005` | `PARTIAL` | `1/1` | `1/3` | `50%` | domain-rule-005: 必須テスト観点 3 件中 1 件を確認。 不足観点: UPPER-IN, UPPER-OUT。 |

## ルール詳細

### `domain-rule-001` user-id-length

- 結果: `NG`
- ルール状態: `PARTIAL`
- 要約: domain-rule-001: 必須テスト観点 7 件中 3 件を確認。 不足観点: UPPER-OUT, COMBO-VALID, COMBO-INVALID, COMBO-PRIORITY。 不足レイヤ: E2E。
- 実装 ID: `domain-rule-001-impl`
- カバレッジ: 実装 `100%`, テスト観点 `43%`, テストレイヤ `67%`, トレーサビリティ `38%`
- 観点別件数: PASS `2`, OMITTED-ACCEPTED `1`, INVALID `0`, MISSING `4`
- 必須テストレイヤ: `UT`, `IT`, `E2E`
- 不足テストレイヤ: `E2E`
- レイヤ集計:
  - `IT`: テスト `1`, OMITTED `0`
  - `UT`: テスト `1`, OMITTED `1`
- 実装参照:
  - `domain-rule-001-impl` at `examples\traceability-fail\src\domain\user\user-id.ts:2`
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `LOWER-OUT` | `OMITTED-ACCEPTED` | OMITTED: `domain-rule-001-LOWER-OUT-OMITTED` |
| `LOWER-IN` | `PASS` | `domain-rule-001-LOWER-IN-001` |
| `UPPER-IN` | `PASS` | `domain-rule-001-UPPER-IN-001` |
| `UPPER-OUT` | `MISSING` | 不足 |
| `COMBO-VALID` | `MISSING` | 不足 |
| `COMBO-INVALID` | `MISSING` | 不足 |
| `COMBO-PRIORITY` | `MISSING` | 不足 |
- 確認済みテスト観点:
  - 観点 `LOWER-OUT`
    - OMITTED `domain-rule-001-LOWER-OUT-OMITTED` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:3`
      - 理由: upstream parser blocks values shorter than three characters
  - 観点 `LOWER-IN`
    - テスト `domain-rule-001-LOWER-IN-001` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:7`
  - 観点 `UPPER-IN`
    - テスト `domain-rule-001-UPPER-IN-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:3`
- 不足テスト観点:
  - `UPPER-OUT`
  - `COMBO-VALID`
  - `COMBO-INVALID`
  - `COMBO-PRIORITY`
- 不正テスト観点: なし
- ルール Issues:
  - `WARNING` `INSUFFICIENT_TEST_REFS`: 必要なテスト注釈数に達していません。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。
  - `ERROR` `MISSING_REQUIRED_TEST_LAYER`: 必須のテストレイヤが不足しています。
  - `ERROR` `MISSING_COMBINATION_DIRECTION`: このルールから関連ルールへの組み合わせ注釈がありません。
  - `ERROR` `MISSING_REVERSE_COMBINATION_DIRECTION`: 関連ルール側からこのルールへの逆方向の組み合わせ注釈がありません。

### `domain-rule-002` user-id-required

- 結果: `NG`
- ルール状態: `NG`
- 要約: domain-rule-002: 必須テスト観点 6 件中 3 件を確認。 実装注釈が不足しています。 不足観点: EMPTY-OUT, COMBO-PRIORITY。 不正注釈観点: NULL-OUT。 不足レイヤ: UT。
- 実装 ID: `domain-rule-002-impl`
- カバレッジ: 実装 `0%`, テスト観点 `67%`, テストレイヤ `50%`, トレーサビリティ `43%`
- 観点別件数: PASS `3`, OMITTED-ACCEPTED `0`, INVALID `1`, MISSING `2`
- 必須テストレイヤ: `UT`, `IT`
- 不足テストレイヤ: `UT`
- レイヤ集計:
  - `IT`: テスト `3`, OMITTED `0`
- 実装参照: なし
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `NULL-OUT` | `INVALID` | 不正: `domain-rule-002-NULL-OUT-001` |
| `EMPTY-OUT` | `MISSING` | 不足 |
| `VALID-IN` | `PASS` | `domain-rule-002-VALID-IN-001` |
| `COMBO-VALID` | `PASS` | `domain-rule-002-COMBO-VALID-001` |
| `COMBO-INVALID` | `PASS` | `domain-rule-002-COMBO-INVALID-001` |
| `COMBO-PRIORITY` | `MISSING` | 不足 |
- 確認済みテスト観点:
  - 観点 `NULL-OUT`
    - 不正 `domain-rule-002-NULL-OUT-001` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:11`
  - 観点 `VALID-IN`
    - テスト `domain-rule-002-VALID-IN-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:7`
  - 観点 `COMBO-VALID`
    - テスト `domain-rule-002-COMBO-VALID-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:11`
  - 観点 `COMBO-INVALID`
    - テスト `domain-rule-002-COMBO-INVALID-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:15`
- 不足テスト観点:
  - `EMPTY-OUT`
  - `COMBO-PRIORITY`
- 不正テスト観点:
  - `NULL-OUT`
- ルール Issues:
  - `ERROR` `MISSING_IMPLEMENTATION_REF`: 実装注釈が不足しています。
  - `WARNING` `INSUFFICIENT_TEST_REFS`: 必要なテスト注釈数に達していません。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。
  - `ERROR` `MISSING_REQUIRED_TEST_LAYER`: 必須のテストレイヤが不足しています。
  - `WARNING` `MISSING_TRACE_RULES_METADATA`: 組み合わせテストに TRACE-RULES メタデータが必要です。
  - `WARNING` `MISSING_RELATED_RULE_IN_TRACE_RULES`: TRACE-RULES に必須の関連ルールが含まれていません。
  - `ERROR` `MISSING_COMBINATION_DIRECTION`: このルールから関連ルールへの組み合わせ注釈がありません。
  - `ERROR` `MISSING_REVERSE_COMBINATION_DIRECTION`: 関連ルール側からこのルールへの逆方向の組み合わせ注釈がありません。

### `domain-rule-003` user-id-format

- 結果: `NG`
- ルール状態: `PARTIAL`
- 要約: domain-rule-003: 必須テスト観点 3 件中 2 件を確認。 不正注釈観点: FORMAT-INVALID。
- 実装 ID: `domain-rule-003-impl`
- カバレッジ: 実装 `100%`, テスト観点 `100%`, テストレイヤ `100%`, トレーサビリティ `75%`
- 観点別件数: PASS `2`, OMITTED-ACCEPTED `0`, INVALID `1`, MISSING `0`
- 必須テストレイヤ: `UT`, `IT`
- レイヤ集計:
  - `IT`: テスト `1`, OMITTED `0`
  - `UT`: テスト `1`, OMITTED `0`
- 実装参照:
  - `domain-rule-003-impl` at `examples\traceability-fail\src\domain\user\user-id-format.ts:2`
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `FORMAT-VALID` | `PASS` | `domain-rule-003-FORMAT-VALID-001` |
| `FORMAT-INVALID` | `INVALID` | 不正: `domain-rule-003-FORMAT-INVALID-001` |
| `FORMAT-EDGE` | `PASS` | `domain-rule-003-FORMAT-EDGE-001` |
- 確認済みテスト観点:
  - 観点 `FORMAT-VALID`
    - テスト `domain-rule-003-FORMAT-VALID-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:3`
  - 観点 `FORMAT-INVALID`
    - 不正 `domain-rule-003-FORMAT-INVALID-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:7`
  - 観点 `FORMAT-EDGE`
    - テスト `domain-rule-003-FORMAT-EDGE-001` at `examples\traceability-fail\test\it\user-format.integration.spec.ts:3`
- 不足テスト観点: なし
- 不正テスト観点:
  - `FORMAT-INVALID`
- ルール Issues:
  - `WARNING` `INSUFFICIENT_TEST_REFS`: 必要なテスト注釈数に達していません。

### `domain-rule-004` user-display-name-min-length

- 結果: `NG`
- ルール状態: `NG`
- 要約: domain-rule-004: 必須テスト観点 3 件中 2 件を確認。 実装注釈が不足しています。 不足観点: LOWER-IN。
- 実装 ID: `domain-rule-004-impl`
- カバレッジ: 実装 `0%`, テスト観点 `67%`, テストレイヤ `100%`, トレーサビリティ `50%`
- 観点別件数: PASS `2`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `1`
- 必須テストレイヤ: `UT`
- レイヤ集計:
  - `IT`: テスト `1`, OMITTED `0`
  - `UT`: テスト `1`, OMITTED `0`
- 実装参照: なし
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `LOWER-OUT` | `PASS` | `domain-rule-004-LOWER-OUT-001` |
| `LOWER-IN` | `MISSING` | 不足 |
| `VALID-IN` | `PASS` | `domain-rule-004-VALID-IN-999` |
- 確認済みテスト観点:
  - 観点 `LOWER-OUT`
    - テスト `domain-rule-004-LOWER-OUT-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:11`
  - 観点 `VALID-IN`
    - テスト `domain-rule-004-VALID-IN-999` at `examples\traceability-fail\test\it\user-format.integration.spec.ts:7`
- 不足テスト観点:
  - `LOWER-IN`
- 不正テスト観点: なし
- ルール Issues:
  - `ERROR` `MISSING_IMPLEMENTATION_REF`: 実装注釈が不足しています。
  - `WARNING` `INSUFFICIENT_TEST_REFS`: 必要なテスト注釈数に達していません。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。

### `domain-rule-005` user-bio-max-length

- 結果: `NG`
- ルール状態: `PARTIAL`
- 要約: domain-rule-005: 必須テスト観点 3 件中 1 件を確認。 不足観点: UPPER-IN, UPPER-OUT。
- 実装 ID: `domain-rule-005-impl`
- カバレッジ: 実装 `100%`, テスト観点 `33%`, テストレイヤ `100%`, トレーサビリティ `50%`
- 観点別件数: PASS `1`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `2`
- 必須テストレイヤ: `UT`
- レイヤ集計:
  - `UT`: テスト `1`, OMITTED `0`
- 実装参照:
  - `domain-rule-005-impl` at `examples\traceability-fail\src\domain\user\bio.ts:2`
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `VALID-IN` | `PASS` | `domain-rule-005-VALID-IN-001` |
| `UPPER-IN` | `MISSING` | 不足 |
| `UPPER-OUT` | `MISSING` | 不足 |
- 確認済みテスト観点:
  - 観点 `VALID-IN`
    - テスト `domain-rule-005-VALID-IN-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:15`
- 不足テスト観点:
  - `UPPER-IN`
  - `UPPER-OUT`
- 不正テスト観点: なし
- ルール Issues:
  - `WARNING` `INSUFFICIENT_TEST_REFS`: 必要なテスト注釈数に達していません。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。
  - `ERROR` `MISSING_TEST_CASE`: 必須のテスト観点が不足しています。

## 全体 Issues

### ERROR

- `UNMAPPED_IMPLEMENTATION_ID`: 実装注釈が既知のルールに対応していません。
  - `domain-rule-999-impl` at `examples\traceability-fail\src\domain\user\user-name.ts:2`
- `UNMAPPED_TEST_ID`: テスト注釈が期待されるテスト観点に対応していません。
  - `domain-rule-123-LOWER-IN-001` at `examples\traceability-fail\test\it\user-id.integration.spec.ts:20`

### WARNING

- `INVALID_TEST_COMMENT_FORMAT`: テスト注釈が規定の TRACE コメント形式ではありません。
  - `domain-rule-003-FORMAT-INVALID-001` at `examples\traceability-fail\test\ut\user-format.unit.spec.ts:7`
- `INVALID_TEST_COMMENT_FORMAT`: テスト注釈が規定の TRACE コメント形式ではありません。
  - `domain-rule-002-NULL-OUT-001` at `examples\traceability-fail\test\ut\user-id.unit.spec.ts:11`

### INFO

- なし

