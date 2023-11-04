import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from . import server


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:postgres@localhost/postgres"

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprint to organize views
    app.register_blueprint(server.bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
