from flask import current_app, g
import click
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text


def get_db():
    if "db" not in g:
        engine = create_engine("postgresql://postgres:postgres@localhost/flask")
        Session = sessionmaker(bind=engine)
        g.db = Session()
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("../../database/schema/init.sql") as f:
        # Read the SQL script from the file
        sql_script = f.read().decode("utf8")

        # Split the script into individual SQL statements
        sql_statements = sql_script.split(";")

        # Execute each SQL statement using the session
        for sql_statement in sql_statements:
            if sql_statement.strip():  # Check if the statement is not empty
                db.execute(text(sql_statement))

        # Commit the changes to the database (if necessary)
        db.commit()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
