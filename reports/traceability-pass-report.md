# トレーサビリティ検証レポート

- 生成日時: `2026-04-09T12:23:45.287486+00:00`
- ステータス: `成功`
- 総ルール数: `5`
- 成功ルール数: `5`
- 失敗ルール数: `0`
- 総 Issue 数: `0`
- 受理済み OMITTED 数: `0`
- 実装対象パス: `examples\traceability-pass\src`
- テスト対象パス: `examples\traceability-pass\test`

## Issue 集計

| 重要度 | 件数 |
| --- | --- |
| `ERROR` | `0` |
| `WARNING` | `0` |
| `INFO` | `0` |

### コード別

- なし

## テストレイヤ集計

| レイヤ | テスト数 | OMITTED 数 | 到達ルール数 | ルール到達率 |
| --- | --- | --- | --- | --- |
| `E2E` | `1` | `0` | `1` | `20%` |
| `IT` | `9` | `0` | `3` | `60%` |
| `UNKNOWN` | `0` | `0` | `0` | `0%` |
| `UT` | `12` | `0` | `5` | `100%` |

## トレーサビリティ要約

| ルール | 状態 | 実装 | テスト観点 | カバレッジ | 要約 |
| --- | --- | --- | --- | --- | --- |
| `domain-rule-001` | `OK` | `1/1` | `7/7` | `100%` | domain-rule-001: 実装注釈と必須テスト観点がすべて揃っています。 |
| `domain-rule-002` | `OK` | `1/1` | `6/6` | `100%` | domain-rule-002: 実装注釈と必須テスト観点がすべて揃っています。 |
| `domain-rule-003` | `OK` | `1/1` | `3/3` | `100%` | domain-rule-003: 実装注釈と必須テスト観点がすべて揃っています。 |
| `domain-rule-004` | `OK` | `1/1` | `3/3` | `100%` | domain-rule-004: 実装注釈と必須テスト観点がすべて揃っています。 |
| `domain-rule-005` | `OK` | `1/1` | `3/3` | `100%` | domain-rule-005: 実装注釈と必須テスト観点がすべて揃っています。 |

## ルール詳細

### `domain-rule-001` user-id-length

- 結果: `OK`
- ルール状態: `OK`
- 要約: domain-rule-001: 実装注釈と必須テスト観点がすべて揃っています。
- 実装 ID: `domain-rule-001-impl`
- カバレッジ: 実装 `100%`, テスト観点 `100%`, テストレイヤ `100%`, トレーサビリティ `100%`
- 観点別件数: PASS `7`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
- 必須テストレイヤ: `UT`, `IT`, `E2E`
- レイヤ集計:
  - `E2E`: テスト `1`, OMITTED `0`
  - `IT`: テスト `4`, OMITTED `0`
  - `UT`: テスト `2`, OMITTED `0`
- 実装参照:
  - `domain-rule-001-impl` at `examples\traceability-pass\src\domain\user\user-id.ts:2`
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `LOWER-OUT` | `PASS` | `domain-rule-001-LOWER-OUT-001` |
| `LOWER-IN` | `PASS` | `domain-rule-001-LOWER-IN-001` |
| `UPPER-IN` | `PASS` | `domain-rule-001-UPPER-IN-001` |
| `UPPER-OUT` | `PASS` | `domain-rule-001-UPPER-OUT-001` |
| `COMBO-VALID` | `PASS` | `domain-rule-001-COMBO-VALID-001` |
| `COMBO-INVALID` | `PASS` | `domain-rule-001-COMBO-INVALID-001` |
| `COMBO-PRIORITY` | `PASS` | `domain-rule-001-COMBO-PRIORITY-001` |
- 確認済みテスト観点:
  - 観点 `LOWER-OUT`
    - テスト `domain-rule-001-LOWER-OUT-001` at `examples\traceability-pass\test\ut\user-id.unit.spec.ts:3`
  - 観点 `LOWER-IN`
    - テスト `domain-rule-001-LOWER-IN-001` at `examples\traceability-pass\test\ut\user-id.unit.spec.ts:7`
  - 観点 `UPPER-IN`
    - テスト `domain-rule-001-UPPER-IN-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:3`
  - 観点 `UPPER-OUT`
    - テスト `domain-rule-001-UPPER-OUT-001` at `examples\traceability-pass\test\e2e\user-id.e2e-spec.ts:3`
  - 観点 `COMBO-VALID`
    - テスト `domain-rule-001-COMBO-VALID-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:7`
  - 観点 `COMBO-INVALID`
    - テスト `domain-rule-001-COMBO-INVALID-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:12`
  - 観点 `COMBO-PRIORITY`
    - テスト `domain-rule-001-COMBO-PRIORITY-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:17`
- 不足テスト観点: なし
- 不正テスト観点: なし
- ルール Issues: なし

### `domain-rule-002` user-id-required

- 結果: `OK`
- ルール状態: `OK`
- 要約: domain-rule-002: 実装注釈と必須テスト観点がすべて揃っています。
- 実装 ID: `domain-rule-002-impl`
- カバレッジ: 実装 `100%`, テスト観点 `100%`, テストレイヤ `100%`, トレーサビリティ `100%`
- 観点別件数: PASS `6`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
- 必須テストレイヤ: `UT`, `IT`
- レイヤ集計:
  - `IT`: テスト `4`, OMITTED `0`
  - `UT`: テスト `2`, OMITTED `0`
- 実装参照:
  - `domain-rule-002-impl` at `examples\traceability-pass\src\domain\user\user-id.ts:3`
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `NULL-OUT` | `PASS` | `domain-rule-002-NULL-OUT-001` |
| `EMPTY-OUT` | `PASS` | `domain-rule-002-EMPTY-OUT-001` |
| `VALID-IN` | `PASS` | `domain-rule-002-VALID-IN-001` |
| `COMBO-VALID` | `PASS` | `domain-rule-002-COMBO-VALID-001` |
| `COMBO-INVALID` | `PASS` | `domain-rule-002-COMBO-INVALID-001` |
| `COMBO-PRIORITY` | `PASS` | `domain-rule-002-COMBO-PRIORITY-001` |
- 確認済みテスト観点:
  - 観点 `NULL-OUT`
    - テスト `domain-rule-002-NULL-OUT-001` at `examples\traceability-pass\test\ut\user-id.unit.spec.ts:11`
  - 観点 `EMPTY-OUT`
    - テスト `domain-rule-002-EMPTY-OUT-001` at `examples\traceability-pass\test\ut\user-id.unit.spec.ts:15`
  - 観点 `VALID-IN`
    - テスト `domain-rule-002-VALID-IN-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:22`
  - 観点 `COMBO-VALID`
    - テスト `domain-rule-002-COMBO-VALID-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:26`
  - 観点 `COMBO-INVALID`
    - テスト `domain-rule-002-COMBO-INVALID-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:31`
  - 観点 `COMBO-PRIORITY`
    - テスト `domain-rule-002-COMBO-PRIORITY-001` at `examples\traceability-pass\test\it\user-id.integration.spec.ts:36`
- 不足テスト観点: なし
- 不正テスト観点: なし
- ルール Issues: なし

### `domain-rule-003` user-id-format

- 結果: `OK`
- ルール状態: `OK`
- 要約: domain-rule-003: 実装注釈と必須テスト観点がすべて揃っています。
- 実装 ID: `domain-rule-003-impl`
- カバレッジ: 実装 `100%`, テスト観点 `100%`, テストレイヤ `100%`, トレーサビリティ `100%`
- 観点別件数: PASS `3`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
- 必須テストレイヤ: `UT`, `IT`
- レイヤ集計:
  - `IT`: テスト `1`, OMITTED `0`
  - `UT`: テスト `2`, OMITTED `0`
- 実装参照:
  - `domain-rule-003-impl` at `examples\traceability-pass\src\domain\user\user-id-format.ts:2`
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `FORMAT-VALID` | `PASS` | `domain-rule-003-FORMAT-VALID-001` |
| `FORMAT-INVALID` | `PASS` | `domain-rule-003-FORMAT-INVALID-001` |
| `FORMAT-EDGE` | `PASS` | `domain-rule-003-FORMAT-EDGE-001` |
- 確認済みテスト観点:
  - 観点 `FORMAT-VALID`
    - テスト `domain-rule-003-FORMAT-VALID-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:3`
  - 観点 `FORMAT-INVALID`
    - テスト `domain-rule-003-FORMAT-INVALID-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:7`
  - 観点 `FORMAT-EDGE`
    - テスト `domain-rule-003-FORMAT-EDGE-001` at `examples\traceability-pass\test\it\user-format.integration.spec.ts:3`
- 不足テスト観点: なし
- 不正テスト観点: なし
- ルール Issues: なし

### `domain-rule-004` user-display-name-min-length

- 結果: `OK`
- ルール状態: `OK`
- 要約: domain-rule-004: 実装注釈と必須テスト観点がすべて揃っています。
- 実装 ID: `domain-rule-004-impl`
- カバレッジ: 実装 `100%`, テスト観点 `100%`, テストレイヤ `100%`, トレーサビリティ `100%`
- 観点別件数: PASS `3`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
- 必須テストレイヤ: `UT`
- レイヤ集計:
  - `UT`: テスト `3`, OMITTED `0`
- 実装参照:
  - `domain-rule-004-impl` at `examples\traceability-pass\src\domain\user\display-name.ts:2`
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `LOWER-OUT` | `PASS` | `domain-rule-004-LOWER-OUT-001` |
| `LOWER-IN` | `PASS` | `domain-rule-004-LOWER-IN-001` |
| `VALID-IN` | `PASS` | `domain-rule-004-VALID-IN-001` |
- 確認済みテスト観点:
  - 観点 `LOWER-OUT`
    - テスト `domain-rule-004-LOWER-OUT-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:11`
  - 観点 `LOWER-IN`
    - テスト `domain-rule-004-LOWER-IN-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:15`
  - 観点 `VALID-IN`
    - テスト `domain-rule-004-VALID-IN-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:19`
- 不足テスト観点: なし
- 不正テスト観点: なし
- ルール Issues: なし

### `domain-rule-005` user-bio-max-length

- 結果: `OK`
- ルール状態: `OK`
- 要約: domain-rule-005: 実装注釈と必須テスト観点がすべて揃っています。
- 実装 ID: `domain-rule-005-impl`
- カバレッジ: 実装 `100%`, テスト観点 `100%`, テストレイヤ `100%`, トレーサビリティ `100%`
- 観点別件数: PASS `3`, OMITTED-ACCEPTED `0`, INVALID `0`, MISSING `0`
- 必須テストレイヤ: `UT`
- レイヤ集計:
  - `UT`: テスト `3`, OMITTED `0`
- 実装参照:
  - `domain-rule-005-impl` at `examples\traceability-pass\src\domain\user\bio.ts:2`
- 期待テストマトリクス:

| 観点 | 状態 | 根拠 |
| --- | --- | --- |
| `VALID-IN` | `PASS` | `domain-rule-005-VALID-IN-001` |
| `UPPER-IN` | `PASS` | `domain-rule-005-UPPER-IN-001` |
| `UPPER-OUT` | `PASS` | `domain-rule-005-UPPER-OUT-001` |
- 確認済みテスト観点:
  - 観点 `VALID-IN`
    - テスト `domain-rule-005-VALID-IN-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:23`
  - 観点 `UPPER-IN`
    - テスト `domain-rule-005-UPPER-IN-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:27`
  - 観点 `UPPER-OUT`
    - テスト `domain-rule-005-UPPER-OUT-001` at `examples\traceability-pass\test\ut\user-format.unit.spec.ts:31`
- 不足テスト観点: なし
- 不正テスト観点: なし
- ルール Issues: なし

## 全体 Issues

### ERROR

- なし

### WARNING

- なし

### INFO

- なし

