# import sqlite3
# sqlite3_db.py->mysql_db.py
import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(current_app.config['DATABASE'],
        #                        detect_types=sqlite3.PARSE_DECLTYPES)
        g.db = pymysql.connect("localhost", "root", "12345678", "catcat")
        # g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schemal.sql') as f:
        print('init db > ' + f.read().decode('utf-8'))
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
