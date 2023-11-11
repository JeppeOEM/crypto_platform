import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('database/trading.sql') as f:
        db.executescript(f.read().decode('utf8'))
    with current_app.open_resource('database/insertdata.sql') as f:
        db.executescript(f.read().decode('utf8'))


def enable_fk():
    db = get_db()


# functions need to be registered with the application instance;


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# creates command line argument = flask --app flaskr init-db


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    enable_fk()
    print("what the fuck")
    click.echo('Initialized the database. with FK constraint')
