from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
from db.config import get_connection
from services.exceptions import AccountNotFoundError

def create_transaction(account_id, amount):
    """Insert a transaction record"""
    con = get_connection()
    cursor = con.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "INSERT INTO transactions (account_id, amount, created_at) VALUES (%s, %s, %s);",
            (account_id, amount, datetime.now(timezone.utc))
        )
        con.commit()
    except Exception as e:
        print("Error creating transaction:", e)
    finally:
        cursor.close()
        con.close()


def list_transactions(account_id):
    con = get_connection()
    cursor = con.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            SELECT t.amount, t.created_at, u.name AS user_name
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            JOIN users u ON a.user_id = u.id
            WHERE t.account_id = %s
            ORDER BY t.created_at DESC;
        """, (account_id,))
        transactions = cursor.fetchall()
        if not transactions:
            raise AccountNotFoundError(
                f"\nAccount with ID {account_id} does not exist."
            )

        pretty_list = []
        for tx in transactions:
            timestamp = tx["created_at"].astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            amount = tx["amount"]
            sign = "+" if float(amount) > 0 else "-"
            pretty_amount = f"{sign}£{abs(float(amount)):.2f}"
            pretty_list.append(f"{timestamp} | {tx['user_name']} | Amount: {pretty_amount}")
        return pretty_list
    finally:
        cursor.close()
        con.close()
