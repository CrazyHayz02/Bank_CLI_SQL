import psycopg2
from psycopg2.extras import RealDictCursor
from db.config import get_connection
from services.exceptions import DuplicateUserError

def create_user(name, email):
    con = get_connection()
    cursor = con.cursor(cursor_factory=RealDictCursor)

    if "@" not in email:
        raise ValueError("Invalid email format.")

    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
            (name, email)
        )
        con.commit()
    except psycopg2.errors.UniqueViolation:
        con.rollback()
        raise DuplicateUserError(
            f"A user with email '{email}' already exists."
        )
    except Exception as e:
        con.rollback()
        print("Error creating user:", e)
    else:
        user_id = cursor.fetchone()["id"]
        return user_id
    finally:
        cursor.close()
        con.close()

def get_user(user_id):
    con = get_connection()
    if not con:
        return None
    cursor = con.cursor()
    try:
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print("Error fetching user:", e)
    else:
        return None
    finally:
        cursor.close()
        con.close()