import sqlite3
from datetime import date

DB_PATH = "data/raus.db"
db_version = 1


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                action TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        actual_version = int(conn.execute("""PRAGMA user_version""").fetchone()[0])
        if actual_version < db_version:
            migrate_db(conn, actual_version, db_version)



def migrate_db(conn, from_version, to_version):
    if from_version < 1 <= to_version:
        # Example migration for version 1
        conn.execute("""
            ALTER TABLE items ADD COLUMN quantity INTEGER DEFAULT 0
        """)
        conn.commit()
        conn.execute(f"PRAGMA user_version = {to_version}")
        conn.commit()

def get_db_version():
    with get_connection() as conn:
        result = conn.execute(
            """
            PRAGMA user_version
            """
        ).fetchone()

    return result[0]


def add_item(quantity, name, action):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO items (quantity, name, action, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (quantity, name, action, date.today().isoformat()),
        )

        conn.commit()

def update_item(item_id, quantity, name, action):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE items
            SET quantity = ?, name = ?, action = ?
            WHERE id = ?
            """,
            (quantity, name, action, item_id),
        )
        conn.commit()


def get_today_count():
    with get_connection() as conn:
        result = conn.execute(
            """
            SELECT COUNT(quantity) AS total
            FROM items
            WHERE created_at = ?
            """,
            (date.today().isoformat(),),
        ).fetchone()

    return result[0]


def get_items():
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT quantity, name, action, created_at, id
            FROM items
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()

def get_item(item_id):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT quantity, name, action, created_at, id
            FROM items
            WHERE id = ?
            """, (item_id,),
        ).fetchone()
    

