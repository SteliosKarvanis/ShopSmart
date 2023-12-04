import os
from flask import Flask
from . import server
from . import db
from . import config as CONFIG


def create_app(test_config=None):
    """
    Create and configure the Flask application.

    Parameters:
        test_config (dict or None): Optional test configuration to override default configuration.

    Returns:
        Flask: The configured Flask application.

    Configuration:
        - SECRET_KEY: Secret key for Flask app.
        - SQLALCHEMY_DATABASE_URI: Database URI for SQLAlchemy.

    Example:
        app = create_app()
        app.run()

    If the module is run directly:
        - Creates the app.
        - Initializes the database.
        - Registers blueprints for organizing views.

    Note:
        - The instance folder is created if it does not exist.
        - The app can be run using `app.run()` when the module is executed directly.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")
    app.config["SQLALCHEMY_DATABASE_URI"] = CONFIG.SQLALCHEMY_DATABASE_URI

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(server.bp)

    return app


# Run the app
if __name__ == "__main__":
    app = create_app()
    app.run()
