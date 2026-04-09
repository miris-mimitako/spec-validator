# _Specs

このディレクトリは、実プロジェクトの仕様書を配置する正本です。

基本構成は次です。

- `_docs/_Specs/{domain}/screens/*.yaml`
- `_docs/_Specs/{domain}/logics/*.yaml`
- `_docs/_Specs/{domain}/terms/*.yaml`

既存の `samples` は参照用の実例として残し、validator は今後 `_docs/_Specs` を優先して読みます。

## ID 方針

仕様書のファイル内では、既存形式に合わせて local id を使ってよいです。

- `RULE-001`
- `INVARIANT-001`
- `INV-004`

ただし validator の内部では、これらを canonical id に正規化して扱います。

- `auth.terms.employee_code.RULE-001`
- `auth.screens.login.INVARIANT-001`
- `auth.screens.login.INV-004`

正規化ルールの詳細は [`20_spec-structure.yaml`](/D:/application/spec-validator/_docs/_GroundRules/20_spec-structure.yaml) を参照します。

## sample との関係

`samples/auth` は実案件で使われていた仕様の実例です。
今後は次の対応で `_docs/_Specs` に補完していきます。

1. `samples/{domain}` の `screens / terms / logics` を `_docs/_Specs/{domain}` に配置する
2. `$ref` を維持したまま canonical id を導出する
3. 実装・テスト・OpenAPI への参照を traceability の対象にする

## 次の validator 対応

次段階では、以下を静的に検証できるようにします。

- spec file の構造妥当性
- local id から canonical id への正規化
- `$ref` の解決可否
- `implemented_in` の収集
- spec 間の ID 一意性
