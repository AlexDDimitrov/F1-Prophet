import mysql.connector
from flask import current_app, g

def get_db():
    if 'db' not in g:
        cfg = current_app.config
        g.db = mysql.connector.connect(
            host=cfg['MYSQL_HOST'],
            port=cfg['MYSQL_PORT'],
            user=cfg['MYSQL_USER'],
            password=cfg['MYSQL_PASSWORD'],
            database=cfg['MYSQL_DATABASE'],
            autocommit=False,
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)