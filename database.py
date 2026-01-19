import sqlite3

DB_NAME = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS role (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active',
            last_login TEXT,
            FOREIGN KEY (role_id) REFERENCES role(role_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            target TEXT NOT NULL,
            timestamp TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)

    conn.commit()
    conn.close()


def seed_roles():
    conn = get_db_connection()
    cur = conn.cursor()

    if cur.execute("SELECT COUNT(*) FROM role").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO role (role_name) VALUES (?)",
            [
                ("Admin",),
                ("Sales Rep",),
                ("Support Agent",),
                ("Manager",)
            ]
        )

    conn.commit()
    conn.close()


def get_roles():
    conn = get_db_connection()
    roles = conn.execute("SELECT * FROM role ORDER BY role_name").fetchall()
    conn.close()
    return roles


def get_users():
    conn = get_db_connection()
    users = conn.execute("""
        SELECT u.user_id, u.name, u.email, u.status, u.last_login,
               r.role_id, r.role_name
        FROM user u
        JOIN role r ON u.role_id = r.role_id
        ORDER BY u.name
    """).fetchall()
    conn.close()
    return users


def add_user(name, email, role_id):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO user (name, email, role_id, status, last_login)
        VALUES (?, ?, ?, 'Active', NULL)
    """, (name, email, int(role_id)))
    conn.commit()
    conn.close()


def update_user_role(user_id, role_id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE user SET role_id=? WHERE user_id=?",
        (int(role_id), int(user_id))
    )
    conn.commit()
    conn.close()


def update_user_status(user_id, status):
    conn = get_db_connection()
    conn.execute(
        "UPDATE user SET status=? WHERE user_id=?",
        (status, int(user_id))
    )
    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM user WHERE user_id=?", (int(user_id),))
    conn.commit()
    conn.close()


def update_last_login(email):
    # If the email exists in user table, update last_login. Otherwise do nothing.
    conn = get_db_connection()
    conn.execute(
        "UPDATE user SET last_login=datetime('now','localtime') WHERE email=?",
        (email,)
    )
    conn.commit()
    conn.close()


def add_log(action, target):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO audit_log (action, target) VALUES (?, ?)",
        (action, target)
    )
    conn.commit()
    conn.close()


def get_logs():
    conn = get_db_connection()
    logs = conn.execute("""
        SELECT action, target, timestamp
        FROM audit_log
        ORDER BY timestamp DESC
    """).fetchall()
    conn.close()
    return logs


def get_dashboard_stats():
    conn = get_db_connection()

    total_users = conn.execute("SELECT COUNT(*) FROM user").fetchone()[0]
    active_users = conn.execute("SELECT COUNT(*) FROM user WHERE status='Active'").fetchone()[0]
    total_roles = conn.execute("SELECT COUNT(*) FROM role").fetchone()[0]

    conn.close()
    return {"total_users": total_users, "active_users": active_users, "roles": total_roles}
