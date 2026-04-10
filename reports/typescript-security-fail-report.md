# Security Validation Report

- Generated At: `2026-04-10T12:20:29.890481+00:00`
- Status: `failure`
- Total Files: `1`
- Total Issues: `9`
- Paths: `examples\typescript-security-fail\src`

## Issue Counts

| Severity | Count |
| --- | --- |
| `ERROR` | `8` |
| `WARNING` | `1` |
| `INFO` | `0` |

- `WARNING` `FORBIDDEN_DANGEROUS_API`: 1
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: 4
- `ERROR` `SENSITIVE_DATA_LOGGING`: 2
- `ERROR` `SQL_INJECTION_RISK`: 2

## Issues

- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\typescript-security-fail\src\orders.service.ts:4`
  - line: `private tableName = "orders";`
- `ERROR` `SQL_INJECTION_RISK`: Potential SQL injection risk: avoid SQL string concatenation or interpolation.
  - source: `examples\typescript-security-fail\src\orders.service.ts:7`
  - line: `let sql = "SELECT * FROM orders WHERE user_id = '" + userId + "'";`
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\typescript-security-fail\src\orders.service.ts:7`
  - line: `let sql = "SELECT * FROM orders WHERE user_id = '" + userId + "'";`
- `ERROR` `SQL_INJECTION_RISK`: Potential SQL injection risk: avoid SQL string concatenation or interpolation.
  - source: `examples\typescript-security-fail\src\orders.service.ts:8`
  - line: `let deleteSql = `DELETE FROM orders WHERE user_id = '${userId}'`;`
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\typescript-security-fail\src\orders.service.ts:8`
  - line: `let deleteSql = `DELETE FROM orders WHERE user_id = '${userId}'`;`
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\typescript-security-fail\src\orders.service.ts:9`
  - line: `let apiKey = "hard-coded-secret";`
- `ERROR` `SENSITIVE_DATA_LOGGING`: Sensitive data must not be logged.
  - source: `examples\typescript-security-fail\src\orders.service.ts:10`
  - line: `console.log(`password=${password} token=${token}`);`
- `ERROR` `SENSITIVE_DATA_LOGGING`: Sensitive data must not be logged.
  - source: `examples\typescript-security-fail\src\orders.service.ts:11`
  - line: `console.error("authorization", token);`
- `WARNING` `FORBIDDEN_DANGEROUS_API`: Forbidden dangerous API detected.
  - source: `examples\typescript-security-fail\src\orders.service.ts:12`
  - line: `child_process.exec("whoami");`
