# Architecture Validation Report

- Generated At: `2026-04-09T13:17:27.064932+00:00`
- Status: `success`
- Total Files: `4`
- Total Types: `4`
- Total Contracts: `1`
- Total Issues: `0`
- Paths: `examples\csharp-architecture-pass\src`

## Layer Dependency Policy

| Source Layer | Allowed Target Layers |
| --- | --- |
| `application` | `domain` |
| `composition_root` | `application`, `domain`, `infrastructure`, `presentation` |
| `domain` | `(none)` |
| `infrastructure` | `application`, `domain` |
| `presentation` | `application`, `domain` |

## Issue Counts

| Severity | Count |
| --- | --- |
| `ERROR` | `0` |
| `WARNING` | `0` |
| `INFO` | `0` |

- None

## Contracts

| Consumer | Interface | Implementation |
| --- | --- | --- |
| `PlaceOrderUseCase (application)` | `IOrderReader (application)` | `SqlOrderReader (infrastructure)` |

## Issues

- None
