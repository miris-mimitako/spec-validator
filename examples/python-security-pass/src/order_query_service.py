from typing import Final


ACTIVE_STATUS: Final[str] = "ACTIVE"
FIND_ORDERS_SQL: Final[str] = "SELECT * FROM orders WHERE user_id = %s AND status = %s"


class OrderQueryService:
    def execute(self, user_id: str) -> dict[str, str]:
        status = ACTIVE_STATUS
        sql = FIND_ORDERS_SQL
        print("fetching orders for authenticated user")
        return {"user_id": user_id, "status": status, "sql": sql}
