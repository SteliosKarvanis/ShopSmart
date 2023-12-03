from flask import current_app, g
import click
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text


def get_db():
    if "db" not in g:
        engine = create_engine("postgresql://postgres:postgres@localhost/shopsmart")
        Session = sessionmaker(bind=engine)
        g.db = Session()
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def clear_db():
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
    db = get_db()
    with current_app.open_resource("../../database/schema/init.sql") as f:
        sql_script = f.read().decode("utf8")
        sql_statements = sql_script.split(";")

        for sql_statement in sql_statements:
            if sql_statement.strip():
                db.execute(text(sql_statement))

        db.commit()


def fill_db():
    db = get_db()
    with current_app.open_resource("../../database/schema/schema.sql") as f:
        sql_script = f.read().decode("utf8")
        sql_statements = sql_script.split(";")

        for sql_statement in sql_statements:
            if sql_statement.strip():
                db.execute(text(sql_statement))

        db.commit()


@click.command("init-db")
def init_db_command():
    """Create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("clear-db")
def clear_db_command():
    """Clear the existing data."""
    clear_db()
    click.echo("Cleared the database.")


@click.command("fill-db")
def fill_db_command():
    """Fill the existing data and create new tables."""
    fill_db()
    click.echo("Filled the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(clear_db_command)
    app.cli.add_command(fill_db_command)
