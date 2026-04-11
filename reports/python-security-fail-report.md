# Security Validation Report

- Generated At: `2026-04-10T12:20:53.244063+00:00`
- Status: `failure`
- Total Files: `1`
- Total Issues: `8`
- Paths: `examples\python-security-fail\src`

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
  - source: `examples\python-security-fail\src\order_query_service.py:7`
  - line: `table_name = "orders"`
- `ERROR` `SQL_INJECTION_RISK`: Potential SQL injection risk: avoid SQL string concatenation or interpolation.
  - source: `examples\python-security-fail\src\order_query_service.py:8`
  - line: `sql = "SELECT * FROM orders WHERE user_id = '" + user_id + "'"`
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\python-security-fail\src\order_query_service.py:8`
  - line: `sql = "SELECT * FROM orders WHERE user_id = '" + user_id + "'"`
- `ERROR` `SQL_INJECTION_RISK`: Potential SQL injection risk: avoid SQL string concatenation or interpolation.
  - source: `examples\python-security-fail\src\order_query_service.py:9`
  - line: `delete_sql = f"DELETE FROM orders WHERE user_id = '{user_id}'"`
- `ERROR` `FORBIDDEN_DIRECT_LITERAL_ASSIGNMENT`: Literal values must be assigned through a const declaration, not directly.
  - source: `examples\python-security-fail\src\order_query_service.py:10`
  - line: `api_key = "hard-coded-secret"`
- `ERROR` `SENSITIVE_DATA_LOGGING`: Sensitive data must not be logged.
  - source: `examples\python-security-fail\src\order_query_service.py:11`
  - line: `logging.info("password=%s token=%s", password, token)`
- `ERROR` `SENSITIVE_DATA_LOGGING`: Sensitive data must not be logged.
  - source: `examples\python-security-fail\src\order_query_service.py:12`
  - line: `print(f"authorization token: {token}")`
- `WARNING` `FORBIDDEN_DANGEROUS_API`: Forbidden dangerous API detected.
  - source: `examples\python-security-fail\src\order_query_service.py:13`
  - line: `subprocess.run("whoami", shell=True)`
