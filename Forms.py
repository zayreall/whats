from wtforms import Form, StringField, SelectField, TextAreaField, validators


class CreateUserForm(Form):
    first_name = StringField("First Name", [
        validators.Length(min=1, max=50),
        validators.DataRequired()
    ])
    last_name = StringField("Last Name", [
        validators.Length(min=1, max=50),
        validators.DataRequired()
    ])
    gender = SelectField("Gender", [
        validators.DataRequired()
    ], choices=[
        ("", "Select"),
        ("F", "Female"),
        ("M", "Male")
    ], default="")

    membership = SelectField("Membership", [
        validators.DataRequired()
    ], choices=[
        ("F", "Fellow"),
        ("S", "Senior"),
        ("P", "Professional")
    ], default="F")

    status = SelectField("Status", [
        validators.DataRequired()
    ], choices=[
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("warning", "Warning"),
        ("danger", "Danger")
    ], default="active")

    remarks = TextAreaField("Remarks", [validators.Optional()])


class ContactForm(Form):
    name = StringField("Your Name", [
        validators.Length(min=1, max=80),
        validators.DataRequired()
    ])
    email = StringField("Email", [
        validators.Email(message="Please enter a valid email."),
        validators.DataRequired()
    ])
    topic = SelectField("Topic", [validators.DataRequired()], choices=[
        ("", "Select"),
        ("general", "General"),
        ("support", "Support"),
        ("feedback", "Feedback")
    ], default="")

    message = TextAreaField("Message", [
        validators.Length(min=5, max=1000),
        validators.DataRequired()
    ])
