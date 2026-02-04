from db.transactions import create_transaction
from db.config import get_connection
from db.account import get_balance
import psycopg2
from psycopg2.extras import RealDictCursor 


from services.exceptions import (
    InvalidAmountError,
    InsufficientFundsError,
    AccountNotFoundError
)

def transfer_money(account_from, account_to, amount):
    if amount <= 0:
        raise InvalidAmountError(
            "Transfer amount must be greater than zero."
        )

    if account_from == account_to:
        raise InvalidAmountError(
            "Source and destination accounts must be different."
        )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - %s
            WHERE id = %s AND balance >= %s
            RETURNING balance
            """,
            (amount, account_from, amount)
        )
        if cursor.rowcount == 0:
            raise InsufficientFundsError(
                f"Transfer failed: insufficient funds or "
                f"source account {account_from} does not exist."
            )
        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + %s
            WHERE id = %s
            RETURNING balance
            """,
            (amount, account_to)
        )
        if cursor.rowcount == 0:
            raise AccountNotFoundError(
                f"Transfer failed: destination account {account_to} not found."
            )
        cursor.execute(
            """
            INSERT INTO transactions (account_id, amount)
            VALUES (%s, %s), (%s, %s)
            """,
            (account_from, -amount, account_to, amount)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    else:
        return "Successful"
    finally:
        cursor.close()
        conn.close()

def deposit(account_id, amount):
    if amount <= 0:
        raise InvalidAmountError(
            "Deposit amount must be greater than zero."
        )
    
    con = get_connection()
    cursor = con.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE id = %s RETURNING balance;",
            (amount, account_id)
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    else:
        new_balance = cursor.fetchone()["balance"]
        create_transaction(account_id, amount)
        
        return new_balance
    finally:
        cursor.close()
        con.close()


def withdraw(account_id, amount):
    if amount <= 0:
        raise InvalidAmountError(
            "Withdrawal amount must be greater than zero."
        )

    balance = get_balance(account_id)
    print (balance)
    if (float(balance) - float(amount)) < 0:
        raise ValueError("Insufficient funds")
    
    con = get_connection()
    cursor = con.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE id = %s RETURNING balance;",
            (amount, account_id)
        )
        result = cursor.fetchone()
        con.commit()
    except Exception:
        con.rollback()
        raise
    else:
        new_balance = result["balance"]
        create_transaction(account_id, -amount)
        return new_balance
    finally:
        cursor.close()
        con.close()


def transfer_money(account_from, account_to, amount):
    # business logic using db layer
    withdraw(account_from, amount)
    deposit(account_to, amount)
    create_transaction(account_from, -amount)
    create_transaction(account_to, amount)
