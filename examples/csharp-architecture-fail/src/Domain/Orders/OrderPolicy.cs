using Sample.Application.Orders.Queries;

namespace Sample.Domain.Orders;

public sealed class OrderPolicy
{
    private readonly GetOrderQueryService queryService;

    public OrderPolicy(GetOrderQueryService queryService)
    {
        this.queryService = queryService;
    }
}
