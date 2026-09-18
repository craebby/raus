import sqlite3
from datetime import date

DB_PATH = "data/raus.db"


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


def add_item(name, action):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO items (name, action, created_at)
            VALUES (?, ?, ?)
            """,
            (name, action, date.today().isoformat()),
        )

        conn.commit()


def get_today_count():
    with get_connection() as conn:
        result = conn.execute(
            """
            SELECT COUNT(*)
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
            SELECT name, action, created_at
            FROM items
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()
