from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
from db.config import get_connection
from db.transactions import create_transaction
from services.exceptions import AccountNotFoundError, InvalidAmountError

def create_account(user_id, initial_balance):
    if initial_balance < 0:
        raise InvalidAmountError(
            "\nInitial balance cannot be negative."
        )

    con = get_connection()
    cursor = con.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(
            "INSERT INTO accounts (user_id, balance) VALUES (%s, %s) RETURNING id;",
            (user_id, initial_balance)
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    else:
        account_id = cursor.fetchone()["id"]
        # Record initial deposit as transaction
        create_transaction(account_id, initial_balance)
        return account_id
    finally:
        cursor.close()
        con.close()

def get_balance(account_id):
    con = get_connection()
    cursor = con.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "SELECT balance FROM accounts WHERE id = %s;",
            (account_id,)
        )
        balance = cursor.fetchone()
        if not balance:
            raise AccountNotFoundError(
                f"\nAccount with ID {account_id} does not exist."
            )
        return balance["balance"]
    finally:
        cursor.close()
        con.close()