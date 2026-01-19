import sqlite3


class DatabaseHelper:
    def __init__(self, db_name="app.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                membership TEXT NOT NULL,
                status TEXT NOT NULL,
                remarks TEXT
            )
        """)
        conn.commit()
        conn.close()

    def insert_user(self, first_name, last_name, gender, membership, status, remarks):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (first_name, last_name, gender, membership, status, remarks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, gender, membership, status, remarks))
        conn.commit()
        conn.close()

    def get_all_users(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY user_id")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_user_by_id(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def update_user(self, user_id, first_name, last_name, gender, membership, status, remarks):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET first_name=?, last_name=?, gender=?, membership=?, status=?, remarks=?
            WHERE user_id=?
        """, (first_name, last_name, gender, membership, status, remarks, user_id))
        conn.commit()
        conn.close()

    def delete_user(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()
