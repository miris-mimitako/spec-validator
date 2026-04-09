using Sample.Infrastructure.Orders;

namespace Sample.Application.Orders.UseCases;

public sealed class PlaceOrderUseCase
{
    private readonly SqlOrderReader orderReader;

    public PlaceOrderUseCase(SqlOrderReader orderReader)
    {
        this.orderReader = orderReader;
    }

    public void Warmup()
    {
        var local = new SqlOrderReader();
    }
}
