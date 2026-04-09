using Microsoft.Extensions.DependencyInjection;
using Sample.Application.Orders.Ports;
using Sample.Infrastructure.Orders;

namespace Sample.Bootstrap;

public static class DependencyInjection
{
    public static IServiceCollection AddOrders(this IServiceCollection services)
    {
        services.AddScoped<IOrderReader, SqlOrderReader>();
        return services;
    }
}
