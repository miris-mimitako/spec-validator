using Microsoft.Extensions.Logging;
using System.Diagnostics;

namespace Sample.Application.Orders;

public sealed class OrderQueryService
{
    private readonly ILogger<OrderQueryService> logger;
    private readonly string tableName = "Orders";

    public OrderQueryService(ILogger<OrderQueryService> logger)
    {
        this.logger = logger;
    }

    public void Execute(string userId, string password, string token)
    {
        var sql = "SELECT * FROM Orders WHERE UserId = '" + userId + "'";
        var deleteSql = $"DELETE FROM Orders WHERE UserId = '{userId}'";
        string apiKey = "hard-coded-secret";
        logger.LogInformation("login password={password} token={token}", password, token);
        Console.WriteLine($"authorization token: {token}");
        Process.Start("cmd.exe", "/c whoami");
        _ = new { sql, deleteSql, apiKey, tableName };
    }
}
