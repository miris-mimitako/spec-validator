using Microsoft.Extensions.Logging;

namespace Sample.Application.Orders;

public sealed class OrderQueryService
{
    private const string ActiveStatus = "ACTIVE";
    private const string QueryText = "SELECT * FROM Orders WHERE UserId = @userId AND Status = @status";

    private readonly ILogger<OrderQueryService> logger;

    public OrderQueryService(ILogger<OrderQueryService> logger)
    {
        this.logger = logger;
    }

    public void Execute(string userId)
    {
        var status = ActiveStatus;
        var sql = QueryText;
        logger.LogInformation("Fetching orders for authenticated user.");
        _ = new { userId, status, sql };
    }
}
