import logging
import subprocess


class OrderQueryService:
    def execute(self, user_id: str, password: str, token: str) -> dict[str, str]:
        table_name = "orders"
        sql = "SELECT * FROM orders WHERE user_id = '" + user_id + "'"
        delete_sql = f"DELETE FROM orders WHERE user_id = '{user_id}'"
        api_key = "hard-coded-secret"
        logging.info("password=%s token=%s", password, token)
        print(f"authorization token: {token}")
        subprocess.run("whoami", shell=True)
        return {
            "table_name": table_name,
            "sql": sql,
            "delete_sql": delete_sql,
            "api_key": api_key,
        }
