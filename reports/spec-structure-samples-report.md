# 仕様構造検証レポート

- 生成日時: `2026-04-09T12:44:20.842215+00:00`
- ステータス: `失敗`
- 総ドキュメント数: `9`
- 総ルール数: `54`
- 総参照数: `9`
- 総 implemented_in 数: `170`
- 総 Issue 数: `7`
- 対象ルート: `samples`

## Issue 集計

| 重要度 | 件数 |
| --- | --- |
| `ERROR` | `7` |
| `WARNING` | `0` |
| `INFO` | `0` |

## コード別集計

- `ERROR` `MISSING_REF_TARGET`: 4
- `ERROR` `MIXED_RULE_ENTRY_TYPE`: 3

## ドキュメント一覧

| ドメイン | 種別 | ファイル | ルール数 | 参照数 |
| --- | --- | --- | --- | --- |
| `auth` | `screens` | `samples\auth\screens\login.yaml` | `15` | `5` |
| `auth` | `terms` | `samples\auth\terms\admin_flag.yaml` | `4` | `1` |
| `auth` | `terms` | `samples\auth\terms\csrf_module.yaml` | `4` | `0` |
| `auth` | `terms` | `samples\auth\terms\employee_code.yaml` | `3` | `1` |
| `auth` | `terms` | `samples\auth\terms\employee_password.yaml` | `2` | `1` |
| `auth` | `terms` | `samples\auth\terms\jwt_validation.yaml` | `4` | `0` |
| `auth` | `terms` | `samples\auth\terms\login_action.yaml` | `15` | `1` |
| `auth` | `terms` | `samples\auth\terms\quick_new_item_action.yaml` | `3` | `0` |
| `auth` | `terms` | `samples\auth\terms\session_expired_banner.yaml` | `4` | `0` |

## ルール一覧

### `samples\auth\screens\login.yaml`

- `auth.screens.login.INVARIANT-001`
  - local id: `INVARIANT-001`
  - 説明: 認証成功時、employee_team にレコードがない場合は trans_org_to_team から自動割当する
  - implemented_in: `5`
- `auth.screens.login.INVARIANT-002`
  - local id: `INVARIANT-002`
  - 説明: User ID は半角英数字4〜20文字の必須入力
  - implemented_in: `3`
- `auth.screens.login.INVARIANT-003`
  - local id: `INVARIANT-003`
  - 説明: Password は必須入力（最大72文字）
  - implemented_in: `3`
- `auth.screens.login.INV-001`
  - local id: `INV-001`
  - 説明: ログイン成功後の補助 API 呼び出し（user-preferences 取得等）が失敗しても、handleUnauthorized() による強制ログアウトは発生しない
  - implemented_in: `4`
- `auth.screens.login.INV-002`
  - local id: `INV-002`
  - 説明: ログインページ上での 401 レスポンスは handleUnauthorized() をトリガーしない
  - implemented_in: `5`
- `auth.screens.login.INV-003`
  - local id: `INV-003`
  - 説明: ログイン画面の API タイムアウトは Lambda cold start（最大 30 秒）を考慮した値に設定し、タイムアウト時にはユーザーが理解できる日本語メッセージを表示すること
  - implemented_in: `5`
- `auth.screens.login.INV-004`
  - local id: `INV-004`
  - 説明: CSRF トークン取得（GET /auth/csrf-token）は補助処理であり、取得失敗時はリトライを試み、リトライ後も失敗した場合のみユーザーへのガイドメッセージを表示する。ログインフロー自体をブロックしてはならない
  - implemented_in: `3`
- `auth.screens.login.INV-005`
  - local id: `INV-005`
  - 説明: ログイン試行回数がレートリミット（5回/15分）に達した場合は、技術的な HTTP ステータスコードではなく待機時間を含む日本語メッセージを表示すること
- `auth.screens.login.INV-006`
  - local id: `INV-006`
  - 説明: CSRF 検証機能（CsrfGuard + CsrfService）は独立した CsrfModule として提供され、認証以外のドメインモジュール（ControlMasterModule 等）でも再利用可能でなければならない
  - implemented_in: `4`
- `auth.screens.login.INV-007`
  - local id: `INV-007`
  - 説明: ログインレスポンスの user オブジェクトには admin_flag を含めること。admin_flag はフロントエンドの管理者判定に必要であり、VER-014 機密フィールド除外の対象外とする
  - implemented_in: `4`
- `auth.screens.login.INV-008`
  - local id: `INV-008`
  - 説明: JWT トークンは HttpOnly Cookie でのみ管理し、フロントエンドの JavaScript から直接アクセスできないこと（XSS 対策）
- `auth.screens.login.INV-009`
  - local id: `INV-009`
  - 説明: ログアウト時にサーバー側で hozen_jwt HttpOnly Cookie がクリアされること
- `auth.screens.login.INV-011`
  - local id: `INV-011`
  - 説明: レート制限はログイン失敗（認証エラー）のみをカウント対象とし、ログイン成功時はカウンターをリセットまたは加算対象外とする。正規ユーザーが繰り返しログインしても HTTP 429 によるロックアウトが発生しないこと
  - implemented_in: `1`
- `auth.screens.login.INV-010`
  - local id: `INV-010`
  - 説明: FE の EmployeeCookie / UserInfo 型定義は BE の UserInfoSecure 型定義と同一のフィールドセットを持つこと。BE で除外されたフィールド（del_flag / department_code / employee_flag）は FE 型からも削除すること
  - implemented_in: `7`
- `auth.screens.login.INV-012`
  - local id: `INV-012`
  - 説明: 標準ログイン成功時は CSRF 保護付きで POST /auth/login を完了し、hozen_jwt HttpOnly Cookie と canonical user 情報を同期したうえで /{default_slug}/hikitsugi-menu へ遷移する
  - implemented_in: `7`
- 参照:
  - `../terms/employee_code.yaml` -> `D:\application\spec-validator\samples\auth\terms\employee_code.yaml` (OK)
  - `../terms/employee_password.yaml` -> `D:\application\spec-validator\samples\auth\terms\employee_password.yaml` (OK)
  - `../terms/login_action.yaml` -> `D:\application\spec-validator\samples\auth\terms\login_action.yaml` (OK)
  - `../terms/quick_new_item_action.yaml` -> `D:\application\spec-validator\samples\auth\terms\quick_new_item_action.yaml` (OK)
  - `../terms/session_expired_banner.yaml` -> `D:\application\spec-validator\samples\auth\terms\session_expired_banner.yaml` (OK)

### `samples\auth\terms\admin_flag.yaml`

- `auth.terms.admin_flag.RULE-001`
  - local id: `RULE-001`
  - 説明: admin_flag は管理者権限の有無を示すフラグであり、UI 表示制御（管理者メニューの出し分け、管理者専用操作ボタンの表示）に使用される非機密情報である。ログインレスポンスから除外してはならない。VER-014 の機密フィールド除外対象には含めないこと
  - implemented_in: `1`
- `auth.terms.admin_flag.RULE-002`
  - local id: `RULE-002`
  - 説明: FE の EmployeeCookie interface と BE の UserInfoSecure interface のフィールドセットは常に一致させること。BE で除外されたフィールドは FE の型定義からも削除し、saveTokens() のマッピングからも除去すること。型の乖離はサイレントに undefined を Cookie に保存する原因となる
  - implemented_in: `2`
- `auth.terms.admin_flag.RULE-003`
  - local id: `RULE-003`
  - 説明: JWT ペイロードには admin_flag を必ず含めること。AdminGuard は JWT 由来の user オブジェクトから adminFlag を取得して管理者判定を行う。DB の m_employee.admin_flag → TokenScopeInfo.adminFlag → JWT payload.adminFlag → JwtStrategy validate() 戻り値.adminFlag → AdminGuard のフローでデータが伝搬すること。
  - implemented_in: `4`
- `auth.terms.admin_flag.RULE-004`
  - local id: `RULE-004`
  - 説明: adminFlag / admin_flag の truthy 判定では legacy 文字列表現 'true' を後方互換入力として受け入れてよい。ただし canonical な返却値は backend 正規化済みの is_admin（boolean）を正本とし、front は admin_flag 文字列を独自業務解釈してはならない
  - implemented_in: `5`
- 参照:
  - `../../ddl/employee_inf.prisma#employee_inf.admin_flag` -> `D:\application\spec-validator\samples\ddl\employee_inf.prisma#employee_inf.admin_flag` (MISSING)

### `samples\auth\terms\csrf_module.yaml`

- `auth.terms.csrf_module.RULE-001`
  - local id: `RULE-001`
  - 説明: CsrfService および CsrfGuard は専用の CsrfModule に集約し、CSRF 検証が必要なすべてのモジュールで CsrfModule を imports すること。AuthModule に直接 CsrfService を登録してはならない
  - implemented_in: `2`
- `auth.terms.csrf_module.RULE-002`
  - local id: `RULE-002`
  - 説明: CsrfGuard を @UseGuards() で使用するモジュールは、必ず CsrfModule を imports に含めること。CsrfModule を imports せずに CsrfGuard を使用すると NestJS の DI 解決が失敗し UnknownDependenciesException が発生する
  - implemented_in: `3`
- `auth.terms.csrf_module.RULE-003`
  - local id: `RULE-003`
  - 説明: フロントエンドの mutation リクエスト（POST/PUT/PATCH/DELETE）を実装する API 関数は、getCsrfToken() で csrf_token Cookie を読み取り、X-CSRF-Token ヘッダーとして付与すること。auth.ts の login() 関数のパターン（...(csrfToken ? { 'X-CSRF-Token': csrfToken } : {})）を踏襲する
  - implemented_in: `3`
- `auth.terms.csrf_module.RULE-004`
  - local id: `RULE-004`
  - 説明: GET /auth/csrf-token は csrf_token Cookie と同じ値をレスポンスボディ token に返し、トークン生成不能時は 500 ではなく 503 Service Unavailable を返す。POST /auth/login の CSRF 検証失敗時は 403 と reason（csrf_missing / csrf_invalid）を返して OpenAPI と一致させる
  - implemented_in: `4`

### `samples\auth\terms\employee_code.yaml`

- `auth.terms.employee_code.RULE-001`
  - local id: `RULE-001`
  - 説明: 社員コードは必須入力とする
  - implemented_in: `2`
- `auth.terms.employee_code.RULE-002`
  - local id: `RULE-002`
  - 説明: 社員コードは4〜20文字であること
  - implemented_in: `4`
- `auth.terms.employee_code.RULE-003`
  - local id: `RULE-003`
  - 説明: 社員コードは半角英数字のみを許可し、ハイフン・記号・全角文字を受け付けてはならない
  - implemented_in: `5`
- 参照:
  - `../../ddl/employee_inf.prisma#employee_inf.employee_code` -> `D:\application\spec-validator\samples\ddl\employee_inf.prisma#employee_inf.employee_code` (MISSING)

### `samples\auth\terms\employee_password.yaml`

- `auth.terms.employee_password.RULE-001`
  - local id: `RULE-001`
  - 説明: パスワードは必須入力とする
  - implemented_in: `1`
- `auth.terms.employee_password.RULE-002`
  - local id: `RULE-002`
  - 説明: パスワードは最大72文字であること
  - implemented_in: `1`
- 参照:
  - `../../ddl/employee_inf.prisma#employee_inf.employee_password` -> `D:\application\spec-validator\samples\ddl\employee_inf.prisma#employee_inf.employee_password` (MISSING)

### `samples\auth\terms\jwt_validation.yaml`

- `auth.terms.jwt_validation.RULE-001`
  - local id: `RULE-001`
  - 説明: GET /auth/jwt は Authorization: Bearer {token} と hozen_jwt HttpOnly Cookie の両方を認証入力として受け入れ、どちらでも同一の検証結果を返さなければならない
  - implemented_in: `2`
- `auth.terms.jwt_validation.RULE-002`
  - local id: `RULE-002`
  - 説明: GET /auth/jwt のレスポンスは認証確認に必要な最小ペイロード（sub, userId, iat, exp）のみを返し、teamCodes・factoryCode・adminFlag など追加クレームをそのまま露出してはならない
  - implemented_in: `4`
- `auth.terms.jwt_validation.RULE-003`
  - local id: `RULE-003`
  - 説明: JWT が欠落・形式不正・署名不正・期限切れ・ブラックリスト済みのいずれであっても、GET /auth/jwt は 401 Unauthorized を返し、詳細な失敗理由をレスポンスボディに露出しない
  - implemented_in: `3`
- `auth.terms.jwt_validation.RULE-004`
  - local id: `RULE-004`
  - 説明: JWT の exp は '現在時刻 < exp' の間だけ有効とし、現在時刻が exp と同値になった時点で期限切れ（401 Unauthorized）として扱う
  - implemented_in: `2`

### `samples\auth\terms\login_action.yaml`

- `auth.terms.login_action.RULE-001`
  - local id: `RULE-001`
  - 説明: ログインフロー中（login API 成功直後〜画面遷移完了まで）の補助 API 呼び出し（user-preferences 等）が失敗しても、ログインフロー自体を中断してはならない。失敗時はデフォルト値で続行する
  - implemented_in: `1`
- `auth.terms.login_action.RULE-002`
  - local id: `RULE-002`
  - 説明: ログイン API リクエストのタイムアウト値は Lambda cold start（最大 30 秒）を考慮した値（FETCH_TIMEOUT_MS ≥ 30,000ms）に設定しなければならない。タイムアウト発火時は技術的なエラーメッセージではなく日本語の分かりやすいメッセージを表示すること
  - implemented_in: `1`
- `auth.terms.login_action.RULE-003`
  - local id: `RULE-003`
  - 説明: AbortController.abort() を引数なしで呼ぶと 'signal is aborted without reason' が表示される。必ず abort(reason) の形で理由を渡すか、catch ブロックで ApiError に変換すること
  - implemented_in: `1`
- `auth.terms.login_action.RULE-004`
  - local id: `RULE-004`
  - 説明: NestJS の @Injectable() Guard が constructor で DI 依存を持つ場合、その Guard を使用するモジュールは依存プロバイダーを含むモジュールを必ず imports すること。DI 依存のないGuard（例: AdminGuard）とは異なり、モジュール境界を越えた利用にはexports + imports が必須である
  - implemented_in: `1`
- `auth.terms.login_action.RULE-005`
  - local id: `RULE-005`
  - 説明: ログインレスポンスの UserInfoSecure に含めるフィールドは、フロントエンドの Cookie（hozen_employee）に保存される EmployeeCookie 型と一致させること。フロントエンドが参照するフィールドを UserInfoSecure から除外すると、サイレントに undefined となりバグの原因となる
  - implemented_in: `1`
- `auth.terms.login_action.RULE-006`
  - local id: `RULE-006`
  - 説明: 認証成功時の JWT は HttpOnly; Secure; SameSite=Strict の Set-Cookie ヘッダで返却し、document.cookie による JS アクセスを禁止する
  - implemented_in: `3`
- `auth.terms.login_action.RULE-007`
  - local id: `RULE-007`
  - 説明: ログアウト時は認証に使われた source（Authorization / hozen_jwt Cookie）に関わらず同一 JWT をサーバー側ブラックリストへ登録し、あわせて hozen_jwt HttpOnly Cookie をクリアする。logout 後に同一 JWT を再利用した GET /auth/jwt は 401 Unauthorized で拒否しなければならない
  - implemented_in: `6`
- `auth.terms.login_action.RULE-008`
  - local id: `RULE-008`
  - 説明: ログインレスポンス user オブジェクトの型は BE UserInfoSecure と FE UserInfo / EmployeeCookie の間で Single Source of Truth（SSoT）を維持すること。BE の型変更時は FE の型定義を必ず同期更新し、OpenAPI スキーマとの三者一致を保証する
  - implemented_in: `6`
- `auth.terms.login_action.RULE-009`
  - local id: `RULE-009`
  - 説明: returnTo パラメータを経由するリダイレクト先は ALLOWED_RETURN_PREFIXES（'/hozen/' 等）の allowlist で検証すること。'/' 始まり・'//' 不含・'..' 不含・許可プレフィックス適合の4条件を満たすもののみ許可し、オープンリダイレクト攻撃を防ぐ
  - implemented_in: `2`
- `auth.terms.login_action.RULE-010`
  - local id: `RULE-010`
  - 説明: intent パラメータはサーバーサイドではなくフロントエンドのルーティング制御に使用するため、ALLOWED_INTENTS（'new-item' 等）の allowlist で検証し、未知の intent 値は無視すること
  - implemented_in: `2`
- `auth.terms.login_action.RULE-011`
  - local id: `RULE-011`
  - 説明: レート制限カウンターはログイン失敗（HTTP 401/403）時のみ加算し、ログイン成功（HTTP 200）時はカウンターをリセットまたは加算しないこと。正規ユーザーが正しい認証情報で複数回ログインしてもロックアウトされてはならない
  - implemented_in: `2`
- `auth.terms.login_action.RULE-012`
  - local id: `RULE-012`
  - 説明: 認証済み current user の最新 UserInfoSecure は employee_team 由来の最新 teams[] と canonical is_admin / default_slug を含めて返し、front が hozen_employee cookie を再構築するための単一ソースとする
  - implemented_in: `7`
- `auth.terms.login_action.RULE-013`
  - local id: `RULE-013`
  - 説明: POST /auth/login の OpenAPI は、CSRF 不備による 403（reason 付き）とログイン失敗レート制限による 429（Retry-After + 待機時間を含む日本語メッセージ）を、実装および front のエラーハンドリングと一致する形で記述しなければならない
  - implemented_in: `5`
- `auth.terms.login_action.RULE-014`
  - local id: `RULE-014`
  - 説明: Playwright E2E からのログインは、front が付与する専用ヘッダーを使って login 失敗回数レート制限をバイパスできること。通常リクエストや backend 直叩きのレート制限検証には影響を与えてはならない
  - implemented_in: `7`
- `auth.terms.login_action.RULE-015`
  - local id: `RULE-015`
  - 説明: admin 判定と canonical slug 解決は backend が正規化した is_admin / default_slug を正本とし、front は admin_flag や teams[] を独自解釈して再実装してはならない
  - implemented_in: `10`
- 参照:
  - `../../ddl/employee_inf.prisma#employee_inf.employee_code` -> `D:\application\spec-validator\samples\ddl\employee_inf.prisma#employee_inf.employee_code` (MISSING)

### `samples\auth\terms\quick_new_item_action.yaml`

- `auth.terms.quick_new_item_action.RULE-001`
  - local id: `RULE-001`
  - 説明: 認証済みユーザーが「すぐに引継ぎを書く」を押した場合、hozen_employee Cookie に保持した canonical defaultSlug（backend が teams から正規化した値）を用いて /{slug}/new-item へ直接遷移できる href を提示すること
  - implemented_in: `3`
- `auth.terms.quick_new_item_action.RULE-002`
  - local id: `RULE-002`
  - 説明: 未認証ユーザーが「すぐに引継ぎを書く」を押した場合、URL に intent=new-item を保持し、ログインフォームへ focus / scroll させると同時に、ログインが必要であることを視覚的に案内する。intent=new-item が既に付与済みでも no-op にしてはならない
  - implemented_in: `3`
- `auth.terms.quick_new_item_action.RULE-003`
  - local id: `RULE-003`
  - 説明: intent=new-item でログイン成功した場合、遷移先はデフォルトの hikitsugi-menu ではなく /{slug}/new-item でなければならない
  - implemented_in: `3`

### `samples\auth\terms\session_expired_banner.yaml`

- `auth.terms.session_expired_banner.RULE-TEXT-001`
  - local id: `RULE-TEXT-001`
  - 説明: URL パラメータまたはセッション状態から期限切れを検出した場合のみ表示する
  - implemented_in: `3`
- `auth.terms.session_expired_banner.RULE-TEXT-002`
  - local id: `RULE-TEXT-002`
  - 説明: 通常時は非表示（hidden）を維持する
  - implemented_in: `1`
- `auth.terms.session_expired_banner.RULE-001`
  - local id: `RULE-001`
  - 説明: ログインページ上で handleUnauthorized() は発動しない。ログインページでの 401 応答はセッション切れではなく、未認証状態として静かに処理する
  - implemented_in: `1`
- `auth.terms.session_expired_banner.RULE-002`
  - local id: `RULE-002`
  - 説明: ThrottlerGuard から返される 429 TooManyRequests は AllExceptionsFilter で適切にフォーマットし、フロントエンドの 429 ハンドラーで待機時間を含むメッセージを表示すること。500 に変換してはならない
  - implemented_in: `2`

## Issues 詳細

- `ERROR` `MIXED_RULE_ENTRY_TYPE`: ルール配列に文字列などの不正な要素が含まれています。
  - source: `samples\auth\screens\login.yaml`
- `ERROR` `MISSING_REF_TARGET`: $ref の参照先ファイルが存在しません。
  - source: `samples\auth\terms\admin_flag.yaml`
  - ref: `../../ddl/employee_inf.prisma#employee_inf.admin_flag`
- `ERROR` `MISSING_REF_TARGET`: $ref の参照先ファイルが存在しません。
  - source: `samples\auth\terms\employee_code.yaml`
  - ref: `../../ddl/employee_inf.prisma#employee_inf.employee_code`
- `ERROR` `MISSING_REF_TARGET`: $ref の参照先ファイルが存在しません。
  - source: `samples\auth\terms\employee_password.yaml`
  - ref: `../../ddl/employee_inf.prisma#employee_inf.employee_password`
- `ERROR` `MIXED_RULE_ENTRY_TYPE`: ルール配列に文字列などの不正な要素が含まれています。
  - source: `samples\auth\terms\login_action.yaml`
- `ERROR` `MIXED_RULE_ENTRY_TYPE`: ルール配列に文字列などの不正な要素が含まれています。
  - source: `samples\auth\terms\login_action.yaml`
- `ERROR` `MISSING_REF_TARGET`: $ref の参照先ファイルが存在しません。
  - source: `samples\auth\terms\login_action.yaml`
  - ref: `../../ddl/employee_inf.prisma#employee_inf.employee_code`
