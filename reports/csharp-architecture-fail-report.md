# Architecture Validation Report

- Generated At: `2026-04-09T13:17:27.064932+00:00`
- Status: `failure`
- Total Files: `6`
- Total Types: `6`
- Total Contracts: `0`
- Total Issues: `7`
- Paths: `examples\csharp-architecture-fail\src`

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
| `ERROR` | `7` |
| `WARNING` | `0` |
| `INFO` | `0` |

- `ERROR` `CONCRETE_CROSS_LAYER_DEPENDENCY`: 2
- `ERROR` `FORBIDDEN_LAYER_DEPENDENCY`: 3
- `ERROR` `MANUAL_CROSS_LAYER_INSTANTIATION`: 1
- `ERROR` `PROVIDER_OWNED_INTERFACE`: 1

## Contracts

- None

## Issues

- `ERROR` `FORBIDDEN_LAYER_DEPENDENCY`: Layer dependency direction is forbidden by architecture policy: application -> infrastructure.
  - consumer: `GetOrderQueryService`
  - consumer layer: `application`
  - dependency: `IOrderReader`
  - dependency layer: `infrastructure`
  - source: `examples\csharp-architecture-fail\src\Application\Orders\Queries\GetOrderQueryService.cs`
- `ERROR` `PROVIDER_OWNED_INTERFACE`: Cross-layer interface must be owned by the consuming layer.
  - consumer: `GetOrderQueryService`
  - consumer layer: `application`
  - interface: `IOrderReader`
  - interface layer: `infrastructure`
  - source: `examples\csharp-architecture-fail\src\Application\Orders\Queries\GetOrderQueryService.cs`
- `ERROR` `FORBIDDEN_LAYER_DEPENDENCY`: Layer dependency direction is forbidden by architecture policy: application -> infrastructure.
  - consumer: `PlaceOrderUseCase`
  - consumer layer: `application`
  - dependency: `SqlOrderReader`
  - dependency layer: `infrastructure`
  - source: `examples\csharp-architecture-fail\src\Application\Orders\UseCases\PlaceOrderUseCase.cs`
- `ERROR` `CONCRETE_CROSS_LAYER_DEPENDENCY`: Cross-layer dependency must not reference a concrete class.
  - consumer: `PlaceOrderUseCase`
  - consumer layer: `application`
  - dependency: `SqlOrderReader`
  - dependency layer: `infrastructure`
  - source: `examples\csharp-architecture-fail\src\Application\Orders\UseCases\PlaceOrderUseCase.cs`
- `ERROR` `MANUAL_CROSS_LAYER_INSTANTIATION`: Cross-layer dependency must not be created with manual instantiation.
  - consumer: `PlaceOrderUseCase`
  - consumer layer: `application`
  - dependency: `SqlOrderReader`
  - dependency layer: `infrastructure`
  - source: `examples\csharp-architecture-fail\src\Application\Orders\UseCases\PlaceOrderUseCase.cs`
- `ERROR` `FORBIDDEN_LAYER_DEPENDENCY`: Layer dependency direction is forbidden by architecture policy: domain -> application.
  - consumer: `OrderPolicy`
  - consumer layer: `domain`
  - dependency: `GetOrderQueryService`
  - dependency layer: `application`
  - source: `examples\csharp-architecture-fail\src\Domain\Orders\OrderPolicy.cs`
- `ERROR` `CONCRETE_CROSS_LAYER_DEPENDENCY`: Cross-layer dependency must not reference a concrete class.
  - consumer: `OrderPolicy`
  - consumer layer: `domain`
  - dependency: `GetOrderQueryService`
  - dependency layer: `application`
  - source: `examples\csharp-architecture-fail\src\Domain\Orders\OrderPolicy.cs`
