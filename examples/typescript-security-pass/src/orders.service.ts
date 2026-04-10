const ACTIVE_STATUS = "ACTIVE";
const FIND_ORDERS_SQL = "SELECT * FROM orders WHERE user_id = $1 AND status = $2";

export class OrdersService {
  private readonly serviceName = ACTIVE_STATUS;

  fetch(userId: string) {
    const sql = FIND_ORDERS_SQL;
    console.log("fetching orders for authenticated user");
    return { userId, sql, serviceName: this.serviceName };
  }
}
