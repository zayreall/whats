from wtforms import Form, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])


class CreateUserForm(Form):
    name = StringField("Full Name", [DataRequired()])
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField("Temporary Password", [DataRequired()])
    role = SelectField("Role", choices=[("Admin", "Admin"), ("Sales Rep", "Sales Rep")])
