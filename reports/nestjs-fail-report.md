# Naming Validation Report

- Generated At: `2026-04-08T13:38:36.890766+00:00`
- Status: `failure`
- Scope: `file`
- Total: `4`
- Passed: `0`
- Failed: `4`
- Scanned Path: `examples/nestjs-fail/src/orders`

## Error Counts

- `DISALLOWED_ROLE_SUFFIX`: 1
- `FORBIDDEN_DOMAIN_ALIAS`: 1
- `FORBIDDEN_GENERIC_TERM`: 2
- `MISSING_DOMAIN_TERM`: 1
- `UNKNOWN_DOMAIN_TERM`: 1

## Files

### `common-helper.ts`

- Result: `NG`
- Path: `examples\nestjs-fail\src\orders\common-helper.ts`
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

### `order-manager.ts`

- Result: `NG`
- Path: `examples\nestjs-fail\src\orders\order-manager.ts`
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

### `settlement-service.ts`

- Result: `NG`
- Path: `examples\nestjs-fail\src\orders\settlement-service.ts`
- Normalized Name: `SettlementService`
- File Errors:
  - `UNKNOWN_DOMAIN_TERM`: Domain term is not registered in the dictionary.
- Declarations:
  - `SettlementService`: `NG`
    - `UNKNOWN_DOMAIN_TERM`: Domain term is not registered in the dictionary.

### `user-repository.ts`

- Result: `NG`
- Path: `examples\nestjs-fail\src\orders\user-repository.ts`
- Normalized Name: `UserRepository`
- Role Suffixes: `Repository`
- File Errors:
  - `FORBIDDEN_DOMAIN_ALIAS`: Forbidden alias detected for domain term.
- Declarations:
  - `UserRepository`: `NG`
    - Role Suffixes: `Repository`
    - `FORBIDDEN_DOMAIN_ALIAS`: Forbidden alias detected for domain term.

