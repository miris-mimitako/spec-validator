using Microsoft.Extensions.DependencyInjection;

namespace Sample.Bootstrap;

public static class DependencyInjection
{
    public static IServiceCollection AddOrders(this IServiceCollection services)
    {
        return services;
    }
}
