from flask import current_app, g
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from . import config as CONFIG


def get_db():
    """
    Get a database session.

    If a session does not exist in the current application context (g),
    it creates a new session using the SQLAlchemy engine specified in the configuration.

    Returns:
        sqlalchemy.orm.Session: A database session.
    """
    if "db" not in g:
        engine = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine)
        g.db = Session()
    return g.db


def close_db(e=None):
    """
    Close the database session.

    Parameters:
        e: Unused parameter (used by Flask).

    Notes:
        If a session exists in the current application context (g), it is closed.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def clear_db():
    """
    Clear all data from specified tables.

    Truncates and restarts the identity columns for the specified tables.

    Notes:
        This function does not drop tables; it only removes all data from them.
    """
    db = get_db()

    tables_to_clear = [
        "especificacao",
        "instancia_produto",
        "mercado",
        "tipo_dimensao",
        "tipo_produto",
        "unidades_si",
    ]

    for table_name in tables_to_clear:
        truncate_statement = f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"
        db.execute(text(truncate_statement))

    db.commit()


def init_db():
    """
    Initialize the database with the schema from the specified SQL file.

    Reads the SQL file and executes the statements to create tables.

    Notes:
        This function assumes that the SQL file contains valid schema creation statements.
    """
    db = get_db()
    with current_app.open_resource(CONFIG.SCHEMA_INIT_PATH) as f:
        sql_script = f.read().decode("utf8")
        sql_statements = sql_script.split(";")

        for sql_statement in sql_statements:
            if sql_statement.strip():
                db.execute(text(sql_statement))

        db.commit()


def fill_db():
    """
    Fill the database with data from the specified SQL file.

    Reads the SQL file and executes the statements to insert data into tables.

    Notes:
        This function assumes that the SQL file contains valid data insertion statements.
    """
    db = get_db()
    with current_app.open_resource(CONFIG.SCHEMA_FILL_PATH) as f:
        sql_script = f.read().decode("utf8")
        sql_statements = sql_script.split(";")

        for sql_statement in sql_statements:
            if sql_statement.strip():
                db.execute(text(sql_statement))

        db.commit()


@click.command("init-db")
def init_db_command():
    """
    Click command to create new tables.
    """
    init_db()
    click.echo("Initialized the database.")


@click.command("clear-db")
def clear_db_command():
    """
    Click command to clear the existing data.
    """
    clear_db()
    click.echo("Cleared the database.")


@click.command("fill-db")
def fill_db_command():
    """
    Click command to fill the existing data and create new tables.
    """
    fill_db()
    click.echo("Filled the database.")


def init_app(app):
    """
    Initialize the Flask app with teardown and CLI commands.

    Parameters:
        app (Flask): The Flask application.

    Notes:
        - Registers a teardown function to close the database session when the app context is popped.
        - Adds CLI commands for initializing, clearing, and filling the database.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(clear_db_command)
    app.cli.add_command(fill_db_command)
