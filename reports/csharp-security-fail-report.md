# Security Validation Report

- Generated At: `2026-04-10T12:15:29.202413+00:00`
- Status: `failure`
- Total Files: `1`
- Total Issues: `8`
- Paths: `examples\csharp-security-fail\src`

## Issue Counts

| Severity | Count |
| --- | --- |
| `ERROR` | `7` |
| `WARNING` | `1` |
| `INFO` | `0` |

- `WARNING` `FORBIDDEN_DANGEROUS_API`: 1
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: 3
- `ERROR` `SENSITIVE_DATA_LOGGING`: 2
- `ERROR` `SQL_INJECTION_RISK`: 2

## Issues

- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\csharp-security-fail\src\Application\Orders\OrderQueryService.cs:9`
  - line: `private readonly string tableName = "Orders";`
- `ERROR` `SQL_INJECTION_RISK`: Potential SQL injection risk: avoid SQL string concatenation or interpolation.
  - source: `examples\csharp-security-fail\src\Application\Orders\OrderQueryService.cs:18`
  - line: `var sql = "SELECT * FROM Orders WHERE UserId = '" + userId + "'";`
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\csharp-security-fail\src\Application\Orders\OrderQueryService.cs:18`
  - line: `var sql = "SELECT * FROM Orders WHERE UserId = '" + userId + "'";`
- `ERROR` `SQL_INJECTION_RISK`: Potential SQL injection risk: avoid SQL string concatenation or interpolation.
  - source: `examples\csharp-security-fail\src\Application\Orders\OrderQueryService.cs:19`
  - line: `var deleteSql = $"DELETE FROM Orders WHERE UserId = '{userId}'";`
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\csharp-security-fail\src\Application\Orders\OrderQueryService.cs:20`
  - line: `string apiKey = "hard-coded-secret";`
- `ERROR` `SENSITIVE_DATA_LOGGING`: Sensitive data must not be logged.
  - source: `examples\csharp-security-fail\src\Application\Orders\OrderQueryService.cs:21`
  - line: `logger.LogInformation("login password={password} token={token}", password, token);`
- `ERROR` `SENSITIVE_DATA_LOGGING`: Sensitive data must not be logged.
  - source: `examples\csharp-security-fail\src\Application\Orders\OrderQueryService.cs:22`
  - line: `Console.WriteLine($"authorization token: {token}");`
- `WARNING` `FORBIDDEN_DANGEROUS_API`: Forbidden dangerous API detected.
  - source: `examples\csharp-security-fail\src\Application\Orders\OrderQueryService.cs:23`
  - line: `Process.Start("cmd.exe", "/c whoami");`
