# Naming Validation Report

- Generated At: `2026-04-09T13:04:01.415212+00:00`
- Status: `failure`
- Scope: `file`
- Total: `5`
- Passed: `0`
- Failed: `5`
- Scanned Path: `examples/csharp-fail/src/Orders`

## Error Counts

- `DISALLOWED_ROLE_SUFFIX`: 2
- `FORBIDDEN_DOMAIN_ALIAS`: 2
- `FORBIDDEN_GENERIC_TERM`: 3
- `MISSING_DOMAIN_TERM`: 1

## Files

### `CommonHelper.cs`

- Result: `NG`
- Path: `examples\csharp-fail\src\Orders\CommonHelper.cs`
- Normalized Name: `CommonHelper`
- Role Suffixes: `Common`, `Helper`
- File Errors:
  - `FORBIDDEN_GENERIC_TERM`: Forbidden generic term detected.
  - `MISSING_DOMAIN_TERM`: A name must include at least one registered domain term.
- Declarations:
  - `CommonHelper`: `NG`
    - Role Suffixes: `Common`, `Helper`
    - `FORBIDDEN_GENERIC_TERM`: Forbidden generic term detected.
    - `MISSING_DOMAIN_TERM`: A name must include at least one registered domain term.

### `OrderInfo.cs`

- Result: `NG`
- Path: `examples\csharp-fail\src\Orders\OrderInfo.cs`
- Normalized Name: `OrderInfo`
- Domain Terms: `Order`
- Role Suffixes: `Info`
- File Errors:
  - `FORBIDDEN_GENERIC_TERM`: Forbidden generic term detected.
  - `DISALLOWED_ROLE_SUFFIX`: Role suffix is not allowed for this domain term.
- Declarations:
  - `OrderInfo`: `NG`
    - Domain Terms: `Order`
    - Role Suffixes: `Info`
    - `FORBIDDEN_GENERIC_TERM`: Forbidden generic term detected.
    - `DISALLOWED_ROLE_SUFFIX`: Role suffix is not allowed for this domain term.

### `OrderManager.cs`

- Result: `NG`
- Path: `examples\csharp-fail\src\Orders\OrderManager.cs`
- Normalized Name: `OrderManager`
- Domain Terms: `Order`
- Role Suffixes: `Manager`
- File Errors:
  - `FORBIDDEN_GENERIC_TERM`: Forbidden generic term detected.
  - `DISALLOWED_ROLE_SUFFIX`: Role suffix is not allowed for this domain term.
- Declarations:
  - `OrderManager`: `NG`
    - Domain Terms: `Order`
    - Role Suffixes: `Manager`
    - `FORBIDDEN_GENERIC_TERM`: Forbidden generic term detected.
    - `DISALLOWED_ROLE_SUFFIX`: Role suffix is not allowed for this domain term.

### `SettlementService.cs`

- Result: `NG`
- Path: `examples\csharp-fail\src\Orders\SettlementService.cs`
- Normalized Name: `SettlementService`
- Role Suffixes: `Service`
- File Errors:
  - `FORBIDDEN_DOMAIN_ALIAS`: Forbidden alias detected for domain term.
- Declarations:
  - `SettlementService`: `NG`
    - Role Suffixes: `Service`
    - `FORBIDDEN_DOMAIN_ALIAS`: Forbidden alias detected for domain term.

### `UserRepository.cs`

- Result: `NG`
- Path: `examples\csharp-fail\src\Orders\UserRepository.cs`
- Normalized Name: `UserRepository`
- Role Suffixes: `Repository`
- File Errors:
  - `FORBIDDEN_DOMAIN_ALIAS`: Forbidden alias detected for domain term.
- Declarations:
  - `UserRepository`: `NG`
    - Role Suffixes: `Repository`
    - `FORBIDDEN_DOMAIN_ALIAS`: Forbidden alias detected for domain term.

