from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm, ContactForm
from database import DatabaseHelper
from User import User

app = Flask(__name__)
app.secret_key = "any_random_string"

db = DatabaseHelper()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contactUs", methods=["GET", "POST"])
def contact_us():
    form = ContactForm(request.form)
    submitted = False

    if request.method == "POST" and form.validate():
        # Keep it simple: show success message.
        # If you want to store enquiries in DB later, we can add a table.
        submitted = True

    return render_template("contactUs.html", form=form, submitted=submitted)


@app.route("/createUser", methods=["GET", "POST"])
def create_user():
    form = CreateUserForm(request.form)

    if request.method == "POST" and form.validate():
        db.insert_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            membership=form.membership.data,
            status=form.status.data,
            remarks=form.remarks.data or ""
        )
        return redirect(url_for("retrieve_users"))

    return render_template("createUser.html", form=form)


@app.route("/retrieveUsers")
def retrieve_users():
    rows = db.get_all_users()
    users_list = [User.from_database_row(r) for r in rows]
    return render_template("retrieveUsers.html", users_list=users_list)


@app.route("/updateUser/<int:id>/", methods=["GET", "POST"])
def update_user(id):
    form = CreateUserForm(request.form)

    if request.method == "POST" and form.validate():
        db.update_user(
            user_id=id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            membership=form.membership.data,
            status=form.status.data,
            remarks=form.remarks.data or ""
        )
        return redirect(url_for("retrieve_users"))

    row = db.get_user_by_id(id)
    if not row:
        return redirect(url_for("retrieve_users"))

    user = User.from_database_row(row)
    form.first_name.data = user.get_first_name()
    form.last_name.data = user.get_last_name()
    form.gender.data = user.get_gender()
    form.membership.data = user.get_membership()
    form.status.data = user.get_status()
    form.remarks.data = user.get_remarks()

    return render_template("updateUser.html", form=form, user=user)


@app.route("/deleteUser/<int:id>", methods=["POST"])
def delete_user(id):
    db.delete_user(id)
    return redirect(url_for("retrieve_users"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
