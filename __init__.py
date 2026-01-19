from flask import Flask
from User import faq_blueprint
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey123'  # REQUIRED for forms to work (CSRF)

    csrf = CSRFProtect(app)  # Enables CSRF protection

    app.register_blueprint(faq_blueprint)


    return app





