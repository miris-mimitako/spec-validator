using Sample.Application.Orders.Ports;

namespace Sample.Application.Orders.UseCases;

public sealed class PlaceOrderUseCase
{
    private readonly IOrderReader orderReader;

    public PlaceOrderUseCase(IOrderReader orderReader)
    {
        this.orderReader = orderReader;
    }
}
