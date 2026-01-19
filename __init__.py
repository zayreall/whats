from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import database

app = Flask(__name__)
app.secret_key = "secretkey"

# Initialise DB
database.create_tables()
database.seed_roles()


# -------------------------
# Helper functions
# -------------------------
def require_login():
    return session.get("logged_in") is True


def require_admin():
    return session.get("role") == "Admin"


# -------------------------
# Login
# -------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return redirect("/")

        # Prototype login (admin only)
        session["logged_in"] = True
        session["role"] = "Admin"
        session["email"] = email

        database.update_last_login(email)
        database.add_log("LOGIN", email)

        flash("Logged in successfully.", "success")
        return redirect("/dashboard")

    return render_template("login.html")


@app.route("/logout")
def logout():
    if session.get("email"):
        database.add_log("LOGOUT", session.get("email"))

    session.clear()
    flash("You have been logged out.", "secondary")
    return redirect("/")


# -------------------------
# Dashboard
# -------------------------
@app.route("/dashboard")
def dashboard():
    if not require_login():
        return redirect("/")

    stats = database.get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)


# -------------------------
# Users (RETRIEVE)
# -------------------------
@app.route("/users")
def users():
    if not require_login():
        return redirect("/")

    if not require_admin():
        flash("Access denied. Admins only.", "danger")
        return redirect("/dashboard")

    # Get filters from query string
    search_query = request.args.get("q", "").lower()
    role_filter = request.args.get("role", "")

    users_list = database.get_users()
    roles = database.get_roles()

    # BUSINESS LOGIC (FILTERING) — NOT IN TEMPLATE
    if search_query:
        users_list = [
            u for u in users_list
            if search_query in u["name"].lower()
            or search_query in u["email"].lower()
        ]

    if role_filter:
        users_list = [
            u for u in users_list
            if u["role_name"] == role_filter
        ]

    return render_template(
        "users.html",
        users=users_list,
        roles=roles
    )


# -------------------------
# CREATE USER
# -------------------------
@app.route("/add_user", methods=["POST"])
def add_user():
    if not require_login() or not require_admin():
        return redirect("/")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    role_id = request.form.get("role_id", "").strip()

    if not name or not email or not role_id:
        flash("All fields are required.", "danger")
        return redirect("/users")

    try:
        database.add_user(name, email, role_id)
        database.add_log("CREATE USER", email)
        flash("User added successfully.", "success")
    except sqlite3.IntegrityError:
        flash("Email already exists.", "danger")

    return redirect("/users")


# -------------------------
# UPDATE USER ROLE
# -------------------------
@app.route("/update_user_role/<int:user_id>", methods=["POST"])
def update_user_role(user_id):
    if not require_login() or not require_admin():
        return redirect("/")

    role_id = request.form.get("role_id", "").strip()

    if not role_id:
        flash("Role is required.", "danger")
        return redirect("/users")

    database.update_user_role(user_id, role_id)
    database.add_log("UPDATE USER ROLE", f"User ID {user_id}")
    flash("User role updated.", "success")

    return redirect("/users")


# -------------------------
# DEACTIVATE USER
# -------------------------
@app.route("/deactivate_user/<int:user_id>")
def deactivate_user(user_id):
    if not require_login() or not require_admin():
        return redirect("/")

    database.update_user_status(user_id, "Inactive")
    database.add_log("DEACTIVATE USER", f"User ID {user_id}")
    flash("User deactivated.", "warning")

    return redirect("/users")


# -------------------------
# DELETE USER
# -------------------------
@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    if not require_login() or not require_admin():
        return redirect("/")

    database.delete_user(user_id)
    database.add_log("DELETE USER", f"User ID {user_id}")
    flash("User deleted.", "danger")

    return redirect("/users")


# -------------------------
# Audit Logs
# -------------------------
@app.route("/audit")
def audit():
    if not require_login() or not require_admin():
        return redirect("/")

    logs = database.get_logs()
    return render_template("audit.html", logs=logs)


# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
