from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Register Packages
login = LoginManager()

# Database Manager
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # INITIALIZING SECTION
    app = Flask(__name__)

    #link to our config
    app.config.from_object(Config)

    #register packages
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure Settings
    login.login_view = 'auth.login'
    login.login_message = 'You must log in to access this page'
    login.login_message_category = 'warning'

    #importing blueprints
    from .blueprints.main import main
    from .blueprints.auth import auth

    # registering blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app