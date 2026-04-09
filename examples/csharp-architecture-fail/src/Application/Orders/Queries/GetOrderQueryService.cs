using Sample.Infrastructure.Orders;

namespace Sample.Application.Orders.Queries;

public sealed class GetOrderQueryService
{
    private readonly IOrderReader orderReader;

    public GetOrderQueryService(IOrderReader orderReader)
    {
        this.orderReader = orderReader;
    }
}
