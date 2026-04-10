import child_process from "child_process";

export class OrdersService {
  private tableName = "orders";

  fetch(userId: string, password: string, token: string) {
    let sql = "SELECT * FROM orders WHERE user_id = '" + userId + "'";
    let deleteSql = `DELETE FROM orders WHERE user_id = '${userId}'`;
    let apiKey = "hard-coded-secret";
    console.log(`password=${password} token=${token}`);
    console.error("authorization", token);
    child_process.exec("whoami");
    return { sql, deleteSql, apiKey, tableName: this.tableName };
  }
}
